from django.shortcuts import render
from base.models import *
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


def index(request):
    ps = Periodo.objects.all()
    return render(request, "/home/templates/home/index.html")


def registro(request):
    if request.method == 'GET':
        return render(request, "contable/registro.html")
    else:
        d = {'empresa': request.POST.get('empresa', ''), 'ruc': request.POST.get('ruc', ''),
                'username': request.POST.get('username', ''), 'email': request.POST.get('email', ''),
                'password': request.POST.get('password', '')
                }
        if Empresa.objects.filter(ruc=d['ruc']).count() > 0 or Empresa.objects.filter(nombre=d['empresa']).count() > 0:
            d['error'] = 'Esta empresa ya se encuentra registrada'
        else:
            if User.objects.filter(username=d['username']).count() == 0:
                e, created = Empresa.objects.get_or_create(nombre=d['empresa'], ruc=d['ruc'])
                u = User.objects.create_user(d['username'], d['email'], d['password'])
                u.empresa = e
                u.save()
                if not request.user.is_authenticated():
                    login(request, u)
                return HttpResponseRedirect('/contable')
            else:
                d['error'] = 'Ya existe el usuario %s' % d['username']
        return render(request, "contable/registro.html", d)

@login_required
def dashboard(request):
    return render(request, "contable/dashboard.html")

@login_required
def completar_perfil(request):
    pass

@login_required
def completar_empresa(request):
    u = request.user
    e = request.user.empresa
    d = {}
    if not e:
        e = Empresa(nombre=u.username, ruc="")
        e.save()
    u.empresa = e
    u.save()
    if request.method == 'GET':
        d['empresa'] = e
        d['tipos_empresa'] = TipoEmpresa.objects.all().order_by('codigo')
        return render(request, "contable/perfilEmpresa/completar_perfil_empresa.html", d)
    else:
        if not e.perfil_complato:
            tipo_id = request.POST.get('tipo_id', None)
            if tipo_id:
                t = TipoEmpresa.objects.get(id=tipo_id)
                f = request.POST.get('fecha_apertura', '').split('-')
                fecha = datetime(year=int(f[0]), month=int(f[1]), day=int(f[2]))
                p = Periodo().crear(fecha, e)
                p.save()
                for cb in t.cuentas():
                    c = Cuenta(empresa=e, codigo=cb.codigo, nombre=cb.nombre, padre=cb.buscar_padre(e), operativa=cb.operativa)
                    c.save()
                    b = Balanza(cuenta=c, periodo=p)
                    b.save()
                e.perfil_complato = True
                e.save()
                d['result'] = 'Perfil Completado!'
                return JsonResponse(d)
            else:
                d['result'] = 'Tipo Id es requerido'
                return JsonResponse(d)
        else:
            d['error'] = 'El perfil de la empresa ya se encuentra completo'
            return JsonResponse(d)


@login_required
def editar_empresa(request):
    if request.method == 'GET':
        return render(request, "contable/perfilEmpresa/editar_perfil_empresa.html")
    elif request.method == 'POST' :
        response_data = {}
        nombre = request.POST.get('name', '')
        ruc    = request.POST.get('ruc', '')
        imagen = request.FILES['imagen']
        if nombre != '' and ruc != '':
           e = request.user.empresa
           e.nombre = nombre
           e.ruc = ruc
           if imagen:
              e.imagen = imagen
           e.save();
        response_data['result'] = ''
        return JsonResponse(response_data)

@login_required
def perfil(request):
    if request.method == 'GET':
        return render(request, "contable/perfilEmpleado/editar_perfil.html")
    else:
        response_data = {}
        usuario = request.user
        usuario.username = request.POST.get('name', '')
        usuario.email = request.POST.get('email', '')
        usuario.save()
        response_data['result'] = 'Registro exitoso'
        return JsonResponse(response_data)




@login_required
def cuenta(request):
    if request.method == 'GET':
        return render(request, "contable/cuenta/cuentas.html")
    """else :
        d = {'codigo': request.POST.get('codigo', ''), 'nombre': request.POST.get('nombre', ''),
            'operativa': request.POST.get('operativa', ''), 'padre': request.POST.get('padre', '')
            }
        if Cuenta.objects.filter(codigo=d['codigo']).count() > 0 or Cuenta.objects.filter(nombre=d['nombre']).count() > 0:
            d['error'] = 'Esta cuenta ya se encuentra registrada'
        else :
            if d['padre'] != '':
               padre = Cuenta.objects.get(id=d['padre'])
               if padre :
                  try:
                     cuenta = Cuenta.objects.get_or_create(codigo=d['codigo'], nombre=d['nombre'],operativa=d['operativa'],padre=padre,empresa=request.user.empresa)
                  except Exception:
                     d['error'] = 'Error al crear cuenta con padre'
               else :
                  d['error'] = 'El padre no se encontro en las cuentas'
                  return JsonResponse(d)
            else :
               try :
                  cuenta = Cuenta.objects.get_or_create(codigo=d['codigo'], nombre=d['nombre'],operativa=d['operativa'],empresa=request.user.empresa)
                  d['result'] = 'Registro exitoso'
               except Exception:
                  d['error'] = 'Error al crear cuenta con padre'
        return JsonResponse(d)"""


@login_required
def comprobantes(request):
    if request.method == 'GET':
        return render(request, 'contable/comprobantes.html', {'data': request.user.empresa.comprobantes()})


@login_required
def reporte(request):
    return render(request, 'contable/reporte.html')

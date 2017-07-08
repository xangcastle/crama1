from __future__ import unicode_literals
from .base import Base
from django.db import models
from datetime import datetime
import calendar
from django.contrib.auth.models import User


MESES = ['ERROR', 'ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO',
'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']


class Periodo(Base):
    empresa = models.ForeignKey('Empresa', null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    cerrado = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s %s %s' % (self.empresa,
        MESES[int(self.fecha_inicio.month)],
        str(self.fecha_inicio.year))

    class Meta:
        ordering = ['empresa', 'fecha_inicio']

    @staticmethod
    def crear(fecha, empresa):
        p, created = Periodo.objects.get_or_create(
        fecha_inicio=datetime(fecha.year, fecha.month, 1),
        fecha_fin=datetime(fecha.year, fecha.month,
        calendar.monthrange(fecha.year, fecha.month)[1]),
        empresa=empresa)
        return p

    @staticmethod
    def periodo_actual(empresa):
        hoy = datetime.now()
        try:
            return Periodo.objects.get(
                empresa=empresa,
                fecha_inicio=datetime(
                    year=hoy.year, month=hoy.month, day=1))
        except:
            return Periodo().crear(hoy, empresa)


class BaseCuenta(Base):
    codigo = models.CharField(max_length=65)
    nombre = models.CharField(max_length=255)
    operativa =  models.BooleanField(default=True)
    padre = models.ForeignKey('self', null=True, blank=True, related_name="%(app_label)s_%(class)s_padre")

    class Meta:
        abstract = True

    def __unicode__(self):
        return '%s %s' % (self.codigo, self.nombre)

class TipoEmpresa(Base):
    codigo = models.CharField(max_length=65, default="")
    nombre = models.CharField(max_length=200)

    def cuentas(self):
        return CuentaTipo.objects.filter(tipo=self).order_by('codigo')

    def __unicode__(self):
        return '%s' % self.nombre

    class Meta:
        verbose_name_plural = 'modelos de catalogos para empresas'


class CuentaTipo(BaseCuenta):
    tipo = models.ForeignKey(TipoEmpresa, null=True)

    def buscar_padre(self, empresa):
        try:
            return Cuenta.objects.get(codigo=self.padre.codigo, empresa=empresa)
        except:
            return None


class Cuenta(BaseCuenta):
    empresa = models.ForeignKey('Empresa', null=True)

    @property
    def auxiliar(self):
        if self.padre:
            return self.codigo.replace(padre.codigo, '')
        else:
            return None

    def __unicode__(self):
        return '%s %s %s' % (self.empresa, self.codigo, self.nombre)

    class Meta:
        ordering = ['empresa', 'codigo']
        verbose_name_plural = 'catalogos de cuenta de empresas'

    def subcuentas(self):
        return Cuenta.objects.filter(padre=self)

    def agregarSubCuenta(self, cuenta):
        c = Cuenta(empresa=self.empresa, padre=self, nombre=cuenta.nombre, codigo=cuenta.codigo, operativa=True)
        c.save()
        return c

    def reclacificarCuenta(self, origen, destino):
        '''
        reclacificar auxiliar de una cuenta de mayor a otra...
        '''
        pass

    def es_operativa(self):
        if self.subcuentas().count() == 0:
            return True
        else:
            return False

    def saldo(self):
        if self.es_operativa():
            return 0.0 # remplazar por una funcion que busque el saldo apartir de la balanza y los movimientos
        else:
            return 0.0 # remplazr por la suma del saldo de todas las subcuentas

    def css_class(self):
        if self.es_operativa():
            return 'file'
        else:
            return 'folder'


class Comprobante(Base):
    periodo = models.ForeignKey(Periodo)
    fecha = models.DateField()
    concepto = models.TextField(max_length=400)

    def save(self, *args, **kwargs):
        p = Periodo.by_date(self.fecha)
        if p.cerrado:
            raise "Este periodo ya se encuentra cerrado"
        else:
            self.periodo = p
        super(Comprobante, self).save()

    class Meta:
        verbose_name_plural = 'comprobantes y movimientos'


class Movimiento(Base):
    comprobante = models.ForeignKey(Comprobante)
    cuenta = models.ForeignKey(Cuenta)
    credito = models.FloatField(default=0.0)
    debito = models.FloatField(default=0.0)


class Balanza(Base):
    periodo = models.ForeignKey(Periodo)
    cuenta = models.ForeignKey(Cuenta)
    saldo_inicial = models.FloatField(default=0.0)
    saldo_final = models.FloatField(default=0.0)

    def __unicode__(self):
        return '%s - %s - %s - %s' % (self.cuenta.codigo, self.cuenta.nombre,
        str(self.saldo_inicial), str(self.saldo_final))


class Empresa(Base):
    nombre = models.CharField(max_length=255)
    ruc = models.CharField(max_length=14)
    perfil_complato = models.BooleanField(default=False)
    cuentas_montadas = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to="imagen_empresas", blank=True)

    class Meta:
        verbose_name_plural = 'empresas afiliadas'

    def __unicode__(self):
        return '%s %s' % (self.ruc, self.nombre)

    def cuentas(self):
        return Cuenta.objects.filter(empresa=self)

    def comprobantes(self):
        periodo = Periodo.periodo_actual(self)
        return Comprobante.objects.filter(
            periodo=periodo)

    def balanza(self, periodo=None):
        if not periodo:
            periodo = Periodo.periodo_actual(self)
        return Balanza.objects.filter(periodo=periodo)

User.add_to_class('empresa', models.ForeignKey(Empresa, null=True))

from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

class periodo_admin(admin.ModelAdmin):
    list_display = ('empresa', 'fecha_inicio', 'fecha_fin', 'cerrado')
    list_filter = ('cerrado', 'empresa')

admin.site.register(Periodo, periodo_admin)


class cuenta_admin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'operativa')
    list_filter = ('empresa', 'operativa', 'padre')
    search_fields = ('codigo', 'nombre')

admin.site.register(Cuenta, cuenta_admin)


admin.site.register(Empresa)
class cuentas_default(admin.TabularInline):
    model = CuentaTipo
    extra = 0
    
class tipos_empresa(admin.ModelAdmin):
    inlines = [cuentas_default,]
admin.site.register(TipoEmpresa, tipos_empresa)

class detalle(admin.TabularInline):
    model = Movimiento
    extra = 0

class comprobante_admin(admin.ModelAdmin):
    fields = ('fecha', 'concepto')
    inlines = [detalle, ]

admin.site.register(Comprobante, comprobante_admin)
admin.site.unregister(User)
class UserAdmin_m(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (('first_name', 'last_name'),
            ('email', 'empresa'))}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
admin.site.register(User, UserAdmin_m)

from django.contrib import admin
from .models import Presente, Convidado, Pedido, PedidoItem


class ConvidadoAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'presenca_confirmada')
    list_filter = ('presenca_confirmada', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0


class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'convidado', 'data_compra', 'pago')
    list_filter = ('pago', 'data_compra')
    search_fields = ('convidado__username', 'convidado__email')
    inlines = [PedidoItemInline]


admin.site.register(Presente)
admin.site.register(Convidado, ConvidadoAdmin)
admin.site.register(Pedido, PedidoAdmin)

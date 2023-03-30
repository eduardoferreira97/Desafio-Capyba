from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .models import Post


class MeuFiltro(admin.SimpleListFilter):
    title = _('Meu Filtro')
    parameter_name = 'meu_filtro'

    def lookups(self, request, model_admin):
        return (
            ('filtro1', _('Filtro 1')),
            ('filtro2', _('Filtro 2')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'filtro1':
            return queryset.filter(Q(meu_campo__icontains='filtro1'))
        elif self.value() == 'filtro2':
            return queryset.filter(Q(meu_campo__icontains='filtro2'))
        else:
            return queryset
    
class MeuModeloAdmin(admin.ModelAdmin):
    list_filter = (MeuFiltro,)

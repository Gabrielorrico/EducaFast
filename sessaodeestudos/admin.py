from django.contrib import admin
from .models import Materia, SessaoDeEstudos


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('icone', 'nome', 'cor')
    search_fields = ('nome',)


@admin.register(SessaoDeEstudos)
class SessaoDeEstudosAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'materia', 'duracao_formatada', 'iniciada_em')
    list_filter = ('materia', 'iniciada_em')
    search_fields = ('usuario__username', 'materia__nome')
    readonly_fields = ('duracao_formatada',)

    def duracao_formatada(self, obj):
        return obj.duracao_formatada
    duracao_formatada.short_description = 'Duração'

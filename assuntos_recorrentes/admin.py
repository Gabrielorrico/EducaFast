from django.contrib import admin
from .models import Materia, Topico, TopicoMarcado


class TopicoInline(admin.TabularInline):
    model = Topico
    extra = 1
    fields = ("nome", "ordem")
    ordering = ("ordem",)


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ("ordem", "icone", "nome", "classe_css", "total_topicos")
    list_editable = ("ordem",)
    list_display_links = ("nome",)
    ordering = ("ordem",)
    inlines = [TopicoInline]


@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ("materia", "nome", "ordem")
    list_filter = ("materia",)
    ordering = ("materia__ordem", "ordem")


@admin.register(TopicoMarcado)
class TopicoMarcadoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "topico", "marcado_em")
    list_filter = ("topico__materia",)
    readonly_fields = ("marcado_em",)
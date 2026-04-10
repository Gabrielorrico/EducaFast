from django.contrib import admin
from .models import Assunto, Flashcard


class FlashcardInline(admin.TabularInline):
    model = Flashcard
    extra = 1
    fields = ('ordem', 'frente', 'verso')
    ordering = ('ordem',)


@admin.register(Assunto)
class AssuntoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'materia', 'total_flashcards', 'ordem')
    list_filter = ('materia',)
    search_fields = ('nome', 'resumo')
    ordering = ('materia__nome', 'ordem', 'nome')
    inlines = [FlashcardInline]

    @admin.display(description='Flashcards')
    def total_flashcards(self, obj):
        return obj.flashcards.count()


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'assunto', 'ordem')
    list_filter = ('assunto__materia', 'assunto')
    search_fields = ('frente', 'verso')
    ordering = ('assunto__materia__nome', 'assunto__nome', 'ordem')
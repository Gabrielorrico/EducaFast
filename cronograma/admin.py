from django.contrib import admin
from .models import Disciplina, Cronograma, SessaoEstudo

admin.site.register(Disciplina)
admin.site.register(Cronograma)
admin.site.register(SessaoEstudo)
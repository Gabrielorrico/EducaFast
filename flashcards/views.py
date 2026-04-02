from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def lista_flashcards(request):
    return HttpResponse("App flashcards funcionando!")
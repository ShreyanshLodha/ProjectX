from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render_to_response

# Create your views here.
def call(request):
    return render_to_response("about.html")
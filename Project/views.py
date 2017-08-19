from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render_to_response

# Create your views here.
def about(request):
    return render_to_response("about.html")

def contact(request):
    return render_to_response("contact.html")
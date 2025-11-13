from django.shortcuts import render, HttpResponse

# Create your views here.
def menu(request):
    html = """
    <p>sALOM</p>
    """
    return HttpResponse(html)
from django.shortcuts import render

# Create your views here.
def masker(req):
    template = 'masker.html'
    context = {}

    return render(req, template, context)

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'addtwo/index.html')

def compute(request):
    a = int(request.POST['num_a'])
    b = int(request.POST['num_b'])
    return HttpResponse(a + b)

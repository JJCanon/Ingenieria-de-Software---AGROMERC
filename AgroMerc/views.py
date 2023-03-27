from django.shortcuts import render

#index
def index(request):
    return render(request,'index.html')
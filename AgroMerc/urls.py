"""AgroMerc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AgroMerc.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('AgroMerc/',AgroMerc, name="AgroMerc"),
    path('signUp/', signUp,name="signUp" ),
    path('signIn/', signIn, name="signIn"),
    path('main/', main, name="main"),
    path('main/producto/', producto, name='producto'),
    path('main/misProductos/', misProductos, name='misProductos'),
    path('main/Compra',compra,name='compra'),
    path('main/Compra/CompraRealizada',realizarCompra,name='realizarCompra')
]

#configuración Url para imagenes
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Mongo
from pymongo import MongoClient

#django
from django.shortcuts import render,redirect
from .forms import *
from django.template import loader


#conexion al cliente de MongoDb server
client = MongoClient(
    "mongodb+srv://AgroMerc:AgroMerc2023@cluster0.5elomeg.mongodb.net/?retryWrites=true&w=majority")
#Base de datos
db = client['AgroMerc']
#Colecciones
colClientes = db['Clientes']
colProductos = db['Productos']
print(client.list_database_names())

#AgroMerc
def AgroMerc(request):
    return render(request, 'AgroMerc.html')

#signIn
def signIn(request):
    if request.method == 'POST':
        nameUser=str(request.POST["nameUser"])
        password=str(request.POST["password"])
        print(nameUser,password)
    return render(request,'signIn.html')

#signUp
def signUp(request):
    if request.method == 'POST':
        name=str(request.POST["name"])
        surnames=str(request.POST["surnames"])
        cedula=str(request.POST["cedula"])
        phoneNumber=str(request.POST["phoneNumber"])
        email=str(request.POST["email"])
        userName=str(request.POST["username"])
        password=str(request.POST["password"])
        typeUser=str(request.POST["typeUser"])
        print(name,surnames,cedula,phoneNumber,email,userName,password,typeUser)
    return render(request, 'signUp.html')


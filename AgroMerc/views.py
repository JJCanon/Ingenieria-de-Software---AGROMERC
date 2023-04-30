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
colClients = db['Clientes']
colProducts = db['Productos']
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
    #boolean data
    existCedula,existEmail,existUserName=False
    registered=False
    context={"exist":False,"registered":registered}
    if request.method == 'POST':
        name=str(request.POST["name"])
        surnames=str(request.POST["surnames"])
        cedula=str(request.POST["cedula"])
        phoneNumber=str(request.POST["phoneNumber"])
        email=str(request.POST["email"])
        userName=str(request.POST["username"])
        password=str(request.POST["password"])
        typeUser=str(request.POST["typeUser"])
        for nombre in colClients.find():
            if(nombre['NameUser']==userName):
                existUserName=True
                break
            elif(nombre['Cedula']==cedula):
                existCedula=True
                break
            elif(nombre['Email']==email):
                existEmail=True
                break
            else:
                registered=True
                """guardar datos en Base de Datos"""
        if(existUserName):
            context={"errorUserName":"el usuario "+userName+" ya existe, intente uno diferente","exist":True,"registered":registered}
        if(existEmail):
            context={"erroEmail":"el email "+cedula+" ya está registrado a otro usuario, intente uno diferente","exist":True,"registered":registered}
        if(existCedula):
            context={"errorCedula":"la cedula ya se encuentra registrada", "exist":True,"registered":registered}
    return render(request, 'signUp.html', context)


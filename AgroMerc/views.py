# Mongo
from pymongo import MongoClient

from django.shortcuts import render

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
    return render(request,'signIn.html')

#signUp
def signUp(request):
    return render(request, 'signUp.html')


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

#header
def header(request):
    return render(request, 'header.html')

# index
def index(request):
    return render(request, 'index.html')


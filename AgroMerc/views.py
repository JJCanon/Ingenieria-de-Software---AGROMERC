# Mongo
from pymongo import MongoClient

# django
from django.shortcuts import render, redirect
from .forms import *
from django.template import loader


# conexion al cliente de MongoDb server
client = MongoClient(
    "mongodb+srv://AgroMerc:AgroMerc2023@cluster0.5elomeg.mongodb.net/?retryWrites=true&w=majority")
# Base de datos
db = client['AgroMerc']
# Colecciones
colClients = db['Clientes']
colProducts = db['Productos']
print(client.list_database_names())

# user
userOnline = {}


# AgroMerc
def AgroMerc(request):
    return render(request, 'AgroMerc.html')

# signIn


def signIn(request):
    exist = False
    correctPassword = False
    ingreso = False
    intento = False
    if request.method == 'POST':
        intento = True
        nameUser = str(request.POST["nameUser"])
        password = str(request.POST["password"])
        # verificar si existe el usuario y ver que es correcta la contraseña
        for users in colClients.find():
            # verificar usuario o correo
            if (nameUser == users['UserName'] or nameUser == users['Email']):
                exist = True
                # verificar contraseña
                if (password == users['Password']):
                    # print("verificando")
                    correctPassword = True
                    ingreso = True
                    userActive(users)
                    break
        # ingreso exitoso
        if (ingreso):
            ingreso = True
    context = {"existCount": exist, "correctPassword": correctPassword,
               "Ingreso": ingreso, "intento": intento}
    return render(request, 'signIn.html', context)

# signUp


def signUp(request):
    # boolean data
    existCedula = False
    existEmail = False
    existUserName = False
    registered = False
    textUsername = ""
    textCedula = ""
    textEmail = ""
    if request.method == 'POST':
        name = str(request.POST["name"])
        surnames = str(request.POST["surnames"])
        cedula = str(request.POST["cedula"])
        phoneNumber = str(request.POST["phoneNumber"])
        email = str(request.POST["email"])
        userName = str(request.POST["username"])
        password = str(request.POST["password"])
        userType = str(request.POST.get('typeUser'))
        # print(name,surnames,cedula,phoneNumber,email,password,userType)
        for nombre in colClients.find():
            if (nombre['UserName'] == userName):
                existUserName = True
            if (nombre['Cedula'] == cedula):
                existCedula = True
            if (nombre['Email'] == email):
                existEmail = True
        if (not existUserName and not existEmail and not existEmail):
            registered = True
            # guardar datos en Base de Datos
            datos = {"Name": name, "Surnames": surnames, "Cedula": cedula,
                     "PhoneNumber": phoneNumber, "Email": email,
                     "UserName": userName, "Password": password,
                     "TypeUser": userType}
            colClients.insert_one(datos)
        if (existUserName):
            textUsername = " el usuario "+userName+" ya existe, intente uno diferente"
            print(existUserName, textUsername)
        if (existEmail):
            textEmail = " el email "+email + \
                " ya está registrado a otro usuario, intente uno diferente"
        if (existCedula):
            textCedula = "la cedula ya se encuentra registrada"
    context = {"textUsername": textUsername, "textEmail": textEmail, "textCedula": textCedula,
               "existUserName": existUserName, "existEmail": existEmail, "existCedula": existCedula,
               "registered": registered}
    return render(request, 'signUp.html', context)

# main : pagina pricipal


def main(request):
    global userOnline
    user = userOnline
    listaProductos = []
    seller = False
    if (user["TypeUser"] == "Seller"):
        seller = True
    # buscar lista de productos
    for producto in colProducts.find():
        # agregar producto a la lista para mostrar
        listaProductos.append(producto)
    context = {"Name": user['Name'], "Surnames": user['Surnames'],
               "Cedula": user['Cedula'], "PhoneNumber": user['PhoneNumber'],
               "Email": user['Email'], "UserName": user['UserName'],
               "Password": user['Password'], "TypeUser": user['TypeUser'], "Productos": listaProductos, "Seller": seller}
    return render(request, 'main.html', context)

# producto


def producto(request):
    global userOnline
    user = userOnline
    productoAgregado = False
    if request.method == 'POST':
        producto = str(request.POST.get("ProductName"))
        nameProduct = str(request.POST["specificName"])
        maxQuantity = str(request.POST['cantidadMax'])
        minQuantity = str(request.POST['cantidadMin'])
        # unit = unidad de medida
        unit = str(request.POST.get('unit'))
        # Json para agregar a la base de datos
        datos = {"Name": producto, "specificName": nameProduct,
                 "maxQuantity": maxQuantity, "minQuantity": minQuantity,
                 "unit": unit, "seller": user['Name']+' '+user['Surnames'], "id": user['Cedula']}
        # agregar a la base de datos
        colProducts.insert_one(datos)
        productoAgregado = True
    context = {"ProductoAgregado": productoAgregado}
    return render(request, 'producto.html', context)

# userActive asignará al usuario que está haciendo uso de la plataforma


def userActive(user):
    global userOnline
    userOnline = user

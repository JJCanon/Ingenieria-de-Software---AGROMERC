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
colCompras = db['Compras']

# user
userOnline = {}


# AgroMerc
def AgroMerc(request):
    return render(request, 'AgroMerc.html')

# signIn
def signIn(request):
    print(client.list_database_names())
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
    nombreListaProductos = []
    seller = False
    #verificar si es vendedor
    if (user["TypeUser"] == "Seller"):
        seller = True
    # buscar lista de productos
    for producto in colProducts.find():
        # agregar producto a la lista para mostrar
        nombreListaProductos.append(producto)
    context = {"Name": user['Name'], "Surnames": user['Surnames'],
               "Cedula": user['Cedula'], "PhoneNumber": user['PhoneNumber'],
               "Email": user['Email'], "UserName": user['UserName'],
               "Password": user['Password'], "Seller": seller,
               "nombreProductos": nombreListaProductos}
               
    return render(request, 'main.html', context)

# producto
def producto(request):
    global userOnline
    user = userOnline
    print(user)
    productoAgregado = False
    if request.method == 'POST':
        productoAgregado = True
        producto = str(request.POST.get("ProductName"))
        nameProduct = str(request.POST["specificName"])
        maxQuantity = str(request.POST['cantidadMax'])
        minQuantity = str(request.POST['cantidadMin'])
        # unit = unidad de medida
        unit = str(request.POST.get('unit'))
        id2=id2(user['id'])
        # Json para agregar a la base de datos
        datos = {"Name": producto, "specificName": nameProduct,
                 "maxQuantity": maxQuantity, "minQuantity": minQuantity,
                 "unit": unit, "seller": user['Name']+' '+user['Surnames'], "id": user['Cedula'],"id2":id2}
        # agregar a la base de datos
        colProducts.insert_one(datos)
        context = {"ProductoAgregado": productoAgregado}
        return render(request, 'productos.html', context)
    context = {"ProductoAgregado": productoAgregado}
    print(productoAgregado)
    return render(request, 'productos.html', context)

#MisProductos
def misProductos(request):
    global  userOnline
    user = userOnline
    misProductos=[]
    for producto in colProducts.find():
        if producto['Cedula'] == user['Cedula']:
            misProductos.append(producto)
    context={"misProductos":misProductos}
    return render(request,'misProductos.html',context)
        
#Compra
def compra(request):
    compraRealizada=False
    global userOnline
    user=userOnline
    if request.method=='POST':
        for key, value in request.POST.items():
           if key.startswith('quantityOrdered_'):
               valores = key.split('_')
               producto=buscarProducto(valores[1],valores[4])
               seller=searchSeller(str(valores[1]))
               try:
                   quantityOrdered = int(value)
                   #print(producto)
                   context={"buyed":compraRealizada,"producto":producto,"cantidad":quantityOrdered,"user":user,"seller":seller}
                   return render(request,'compra.html',context)
               except ValueError:
                   return redirect('main')
    context={"buyed":compraRealizada}
    return render(request,'compra.html',context)

#views para mostrar mientras se completa la compra
def realizarCompra(request):
    global userOnline
    user=userOnline
    purchaseMade=False
    purchaseCancel=False
    if request.method=='POST':
        for key, value in request.POST.items():
            print(key)
            if key.startswith('purchaseMade_'):
                purchaseMade=True
                valores = key.split('_')
                quantityOrdered=int(valores[1])
                producto=buscarProducto(valores[3],valores[2])
                seller=searchSeller(valores[3])
                print(seller['Name']+" "+seller['Surnames'],producto['id'],producto['id2'],user['Name']+" "+user['Surnames'],quantityOrdered)
                datos={"Seller":seller['Name'],"CedulaSeller":producto['id'],"ProductName":producto['Name']+" "+producto['specificName'],"id2Product":producto['id2'],"Buyer":user['Name']+" "+user['Surnames'],"quantitySold":quantityOrdered}
                posibleCompra(producto['id2'],str(int(producto['maxQuantity'])-quantityOrdered),seller['Cedula'])
            else:
                purchaseCancel=True
    
    context={"purchaseMade":purchaseMade,"purchaseCancel":purchaseCancel}
    return render(request,'comprarealizada.html',context)

    """ 
    Funciones hechas con el fin de que las funciones que implementen vistas hagan uso de estas, para así no saturar las funciones y sea mas rapido el tiempo de respuesta

    """

# userActive asignará al usuario que está haciendo uso de la plataforma
def userActive(user):
    global userOnline
    userOnline = user

#busca producto que está comprando
def buscarProducto(id,id2):
    producto=colProducts.find({"id":id,"id2":id2})
    return(producto[0])

def id2(id):
    valorid2 = 0
    for producto in colProducts.find({"id":id}):
        valorid2=producto['id2']
    valorid2=str(int(valorid2)+1)
    return valorid2

#si el usuario confirma la compra
def posibleCompra(id2,newValue,idseller):
    result=colProducts.update_one({"id":idseller,"id2":id2},{'$set':{'maxQuantity':newValue}})
    
#busca el vendedor del producto
def searchSeller(id):
    busqueda = colClients.find({"Cedula":id})
    for seller in busqueda:
        return seller
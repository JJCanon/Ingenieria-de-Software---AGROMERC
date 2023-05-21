lista= ["hola","adios"]

dic = {"hola":"hola","adios":"adios"}




# Mongo
from pymongo import MongoClient
# conexion al cliente de MongoDb server
client = MongoClient(
    "mongodb+srv://AgroMerc:AgroMerc2023@cluster0.5elomeg.mongodb.net/?retryWrites=true&w=majority")
# Base de datos
db = client['AgroMerc']
# Colecciones
colClients = db['Clientes']
colProducts = db['Productos']
a=0

result=colProducts.find({'id':'1000252272'})
for item in result:
    a=item['id2']
    print(item)
print(a)
    
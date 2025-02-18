from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import linked_list
import bstree

app = FastAPI()

# Se definen los nombres de los ficheros con los datos
path_products = 'productos.json'
path_orders = 'pedidos.json'
# TODO ID

# Se define el modelo de los productos
class Product(BaseModel):
    id: int
    name: str
    price: float

# Se define tambien el modelo para los pedidos
class Order(BaseModel):
    id: int
    # El listado de productos de un pedido es un diccionario clave valor donde la clave es el id del producto y el valor la cantidad que se pide
    products: dict

productTree = bstree.BST()
orderList = linked_list.LinkedList()


def orderDeserializer():
    """
        Lee un archivo json con la información de los pedidos y lo devuelve en una linked list
    """
    try:
        with open(path_orders, 'r') as file:
            orderJson = json.load(file)
    except FileNotFoundError:
        orderJson = []

    for order in orderJson:
        orderList.add(order['id'], order['products'])
    
def orderSerializer():
    """
        Escribe los contenidos de una linked list con los pedidos a un fichero de formato json
    """
    orderJson = list_orders()
    with open(path_orders, "w") as file:
            json.dump(orderJson, file, indent=4)

def productDeserializer():
    """
        Lee un archivo json con la información de los productos y lo devuelve en un árbol binario de busqueda
    """
    try:
        with open(path_products, 'r') as file:
            productJson = json.load(file)
    except FileNotFoundError:
        productJson = []
    
    for product in productJson:
        value = {'name': product['name'], 'price': product['price']}
        productTree.insert(product['id'], value)

def productSerializer():
    """
        Escribe los contenidos de un árbol binario de búsqueda con los productos a un fichero de formato json
    """
    productJson = productTree.list_tree()
    with open(path_products, "w") as file:
            json.dump(productJson, file, indent=4)

orderDeserializer()
productDeserializer()


# Crear producto
@app.post('/api/productos', status_code=201)
def add_product(product: Product):
    """
        Añadir un producto al arbol de busqueda de productos
    """
    if productTree.search(product.id):
        return {"error": f"Producto con id {product.id} ya existente"}
    
    productTree.insert(product.id, {'name': product.name, 'price': product.price})
    productSerializer()

    return {"message": "Producto creado con exito"}

# Consultar productos
@app.get('/api/productos')
def list_products():
    """
        Mostrar un listado de todos los productos
    """
    return productTree.list_tree()

# Consultar productos por id
@app.get('/api/productos/{id}')
def show_product(id: int):
    """
        Mostrar el producto correspondiente a un id
    """
    product = productTree.search(id)
    if product:
        return {'id': id, 'name': product['name'], 'price': product['price']}
    else:
        return {"message": f"Producto con id {id} no encontrado"}

# Crear pedidio
@app.post('/api/pedidos', status_code=201)
def add_order(order: Order):
    """
        Crear un nuevo pedido
    """
    # Primero se comprueba que todos los productos en el pedido existen
    for product in order.products:
        if not productTree.search(int(product)):
            return {"error": f"Producto con id {product} no existe"}
    
    # Tambien se comprueba que no exista un pedido con el mismo id
    if orderList.find(order.id):
        return {"error": f"Pedido con id {order.id} ya existente"}

    orderList.add(order.id, order.products)
    orderSerializer()

    return {"message": "Pedido añadido con exito"}

# Listar todos los pedidos
@app.get('/api/pedidos')
def list_orders():
    """
        Listar todos los pedido
    """
    orders = []
    current = orderList.head
    while current:
        orders.append({'id': current.id, 'products': current.data})
        current = current.next
    return orders

# Consultar pedido por id
@app.get('/api/pedidos/{id}')
def show_order(id: int):
    """
        Mostrar el pedido correspondiente a un id
    """
    order = orderList.find(id)
    if order:
        # Se calcula el precio total del pedido, cogiendo el precio de cada producto del arbol de productos y multiplicandolo por la cantidad
        totalPrice = 0
        for product in order:
            totalPrice += productTree.search(int(product))['price']*order[product]

        return {"id": id, "products": order, "total_price": totalPrice}
    else:
        return {"message": f"Pedido con id {id} no encontrado"}


# Actualizar pedido
@app.put('/api/pedidos/{id}', status_code=201)
def update_order(id: int, order: Order):
    """
        Actualizar el contenido de un pedido
    """
    
    current = orderList.head
    while current:
        if current.id == id:
            # Se comprueba que todos los productos del pedido actualizado existen
            for product in order.products:
                if not productTree.search(int(product)):
                    return {"error": f"Producto con id {product} no existe"}
            current.data = order.products
            orderSerializer()
            return {"message": f"Pedido con id {id} actualizado con exito", "order": order}
        current = current.next
    
    return {"message": f"Pedido con id {id} no encontrado"}


# Eliminar pedido
@app.delete('/api/pedidos/{id}', status_code=201)
def delete_order(id: int):
    """
        Eliminar un pedido dado su id
    """
    order = orderList.find(id)
    if order:
        orderList.delete(id)
        orderSerializer()
        return {"message": f"Pedido con id {id} eliminado"}
    else:
        return {"message": f"Pedido con id {id} no encontrado"}


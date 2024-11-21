from models.client import Cliente
from models.cajero import Cajero
from models.movimiento import Movimiento
from utils.algoritmos import quicksort_clientes, mergesort_cajeros, busqueda_binaria

import json


class SistemaCajero:
    def __init__(self):
        self.clientes = {}  ### Diccionario con ID del cliente como clave y objeto Cliente como valor
        self.cajeros = {}   ### Diccionario con ID del cajero como clave y objeto Cajero como valor
        self.movimientos = []  ### Lista de objetos Movimiento

    
    def agregar_cliente(self, id_cliente, nombre, saldo, contraseña):
        if id_cliente in self.clientes:
            return "El cliente ya existe."
        self.clientes[id_cliente] = Cliente(id_cliente, nombre, saldo, contraseña)
        return f"Cliente {nombre} agregado con éxito."

    def modificar_cliente(self, id_cliente, nuevo_nombre=None, nuevo_saldo=None):
        cliente = self.clientes.get(id_cliente)
        if not cliente:
            return "Cliente no encontrado."
        if nuevo_nombre:
            cliente.nombre = nuevo_nombre
        if nuevo_saldo is not None:
            cliente.saldo = nuevo_saldo
        return f"Cliente {id_cliente} modificado con éxito."

    def eliminar_cliente(self, id_cliente):
        if id_cliente not in self.clientes:
            return "Cliente no encontrado."
        del self.clientes[id_cliente]
        return f"Cliente {id_cliente} eliminado con éxito."

    def consultar_clientes(self):
        if not self.clientes:
            return "No hay clientes registrados."
        resultado = "ID | Nombre | Saldo\n"
        for cliente in self.clientes.values():
            resultado += f"{cliente.id_cliente} | {cliente.nombre} | {cliente.saldo}\n"
        return resultado

    # gestion de cajeros
    def agregar_cajero(self, id_cajero, ubicacion, billetes):
        if id_cajero in self.cajeros:
            return "El cajero ya existe."
        self.cajeros[id_cajero] = Cajero(id_cajero, ubicacion, billetes)
        return f"Cajero en {ubicacion} agregado con éxito."

    def modificar_cajero(self, id_cajero, nueva_ubicacion=None, nuevos_billetes=None):
        cajero = self.cajeros.get(id_cajero)
        if not cajero:
            return "Cajero no encontrado."
        if nueva_ubicacion:
            cajero.ubicacion = nueva_ubicacion
        if nuevos_billetes:
            cajero.billetes.update(nuevos_billetes)
        return f"Cajero {id_cajero} modificado con éxito."

    def eliminar_cajero(self, id_cajero):
        if id_cajero not in self.cajeros:
            return "Cajero no encontrado."
        del self.cajeros[id_cajero]
        return f"Cajero {id_cajero} eliminado con éxito."

    def consultar_cajeros(self):
        if not self.cajeros:
            return "No hay cajeros registrados."
        resultado = "ID | Ubicación | Billetes Disponibles\n"
        for cajero in self.cajeros.values():
            resultado += f"{cajero.id_cajero} | {cajero.ubicacion} | {cajero.billetes}\n"
        return resultado

# operaciones
    def retirar(self, id_cliente, id_cajero, monto):
        cliente = self.clientes.get(id_cliente)
        cajero = self.cajeros.get(id_cajero)
        if not cliente:
            return "Cliente no encontrado."
        if not cajero:
            return "Cajero no encontrado."
        mensaje, desglose = cajero.desglosar_monto(monto)
        if desglose:
            cliente.saldo -= monto
            movimiento = Movimiento(None, "Retiro", monto, cliente_origen=cliente)
            self.registrar_movimiento(movimiento)
            return f"Retiro exitoso. Nuevo saldo: {cliente.saldo}\n{mensaje}\nDesglose: {desglose}"
        return mensaje

    def depositar(self, id_cliente, id_cajero, monto):
        cliente = self.clientes.get(id_cliente)
        cajero = self.cajeros.get(id_cajero)
        if not cliente:
            return "Cliente no encontrado."
        if not cajero:
            return "Cajero no encontrado."
        cliente.saldo += monto
        cajero.actualizar_billetes(200, monto // 200)  # Ejemplo simple de actualización
        movimiento = Movimiento(None, "Depósito", monto, cliente_origen=cliente)
        self.registrar_movimiento(movimiento)
        return f"Depósito exitoso. Nuevo saldo: {cliente.saldo}"

    def transferir(self, id_cliente_origen, id_cliente_destino, monto):
        cliente_origen = self.clientes.get(id_cliente_origen)
        cliente_destino = self.clientes.get(id_cliente_destino)
        if not cliente_origen:
            return "Cliente origen no encontrado."
        if not cliente_destino:
            return "Cliente destino no encontrado."
        if cliente_origen.saldo < monto:
            return "Saldo insuficiente para la transferencia."
        cliente_origen.saldo -= monto
        cliente_destino.saldo += monto
        movimiento = Movimiento(None, "Transferencia", monto, cliente_origen=cliente_origen, cliente_destino=cliente_destino)
        self.registrar_movimiento(movimiento)
        return f"Transferencia realizada con éxito. Saldo restante: {cliente_origen.saldo}"

    def pagar_servicio(self, id_cliente, monto):
        cliente = self.clientes.get(id_cliente)
        if not cliente:
            return "Cliente no encontrado."
        if cliente.saldo < monto:
            return "Saldo insuficiente para pagar el servicio."
        cliente.saldo -= monto
        movimiento = Movimiento(None, "Pago de servicios", monto, cliente_origen=cliente)
        self.registrar_movimiento(movimiento)
        return f"Pago de servicio realizado con éxito. Nuevo saldo: {cliente.saldo}"

    # movimientos
    def registrar_movimiento(self, movimiento):
        self.movimientos.append(movimiento)
        return "Movimiento registrado con éxito."

    def consultar_movimientos(self):
        if not self.movimientos:
            return "No hay movimientos registrados."
        return "\n".join(str(mov) for mov in self.movimientos)

    def consultar_movimientos_por_cliente(self, id_cliente):
        cliente = self.clientes.get(id_cliente)
        if not cliente:
            return "Cliente no encontrado."
        movimientos_cliente = [mov for mov in self.movimientos if mov.cliente_origen == cliente or mov.cliente_destino == cliente]
        if not movimientos_cliente:
            return "No hay movimientos para este cliente."
        return "\n".join(str(mov) for mov in movimientos_cliente)

    def consultar_movimientos_por_tipo(self, tipo):
        movimientos_tipo = [mov for mov in self.movimientos if mov.tipo == tipo]
        if not movimientos_tipo:
            return f"No hay movimientos del tipo '{tipo}'."
        return "\n".join(str(mov) for mov in movimientos_tipo)

    # realizamos persistencia de datos
    def guardar_datos(self, ruta):
        datos = {
            "clientes": {id: cliente.__dict__ for id, cliente in self.clientes.items()},
            "cajeros": {id: cajero.__dict__ for id, cajero in self.cajeros.items()},
            "movimientos": [mov.to_dict() for mov in self.movimientos]
        }
        with open(ruta, "w") as archivo:
            json.dump(datos, archivo)
        return "Datos guardados con éxito."

    def cargar_datos(self, ruta):
        with open(ruta, "r") as archivo:
            datos = json.load(archivo)
        for id, cliente in datos["clientes"].items():
            self.clientes[id] = Cliente(**cliente)
        for id, cajero in datos["cajeros"].items():
            self.cajeros[id] = Cajero(**cajero)
        self.movimientos = [Movimiento(**mov) for mov in datos["movimientos"]]
        return "Datos cargados con éxito."
    

    def ordenar_clientes(self, clave):
        """
        Ordena la lista de clientes por clave ('id_cliente' o 'nombre').
        """
        lista_clientes = list(self.clientes.values())
        self.clientes = {cliente.id_cliente: cliente for cliente in quicksort_clientes(lista_clientes, clave)}
        return f"Clientes ordenados por {clave}."

    def buscar_cliente(self, id_cliente):
        """
        Busca un cliente por ID usando búsqueda binaria.
        :param id_cliente: ID del cliente a buscar.
        :return: Cliente encontrado o mensaje de error.
        """
        lista_clientes = list(self.clientes.values())
        lista_ordenada = quicksort_clientes(lista_clientes, 'id_cliente')
        cliente = busqueda_binaria(lista_ordenada, 'id_cliente', id_cliente)
        return cliente if cliente else "Cliente no encontrado."

    def ordenar_cajeros(self, clave):
        """
        Ordena la lista de cajeros por clave ('id_cajero' o 'ubicacion').
        """
        lista_cajeros = list(self.cajeros.values())
        self.cajeros = {cajero.id_cajero: cajero for cajero in mergesort_cajeros(lista_cajeros, clave)}
        return f"Cajeros ordenados por {clave}."


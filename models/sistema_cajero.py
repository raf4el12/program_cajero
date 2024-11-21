from utils.colors_alert import EXITO, RESET, INFO, FALLA
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
            return f"{INFO}El cliente ya existe.{RESET}"
        self.clientes[id_cliente] = Cliente(id_cliente, nombre, saldo, contraseña)
        return f"{EXITO}Cliente {nombre} agregado con éxito.{RESET}"

    def modificar_cliente(self, id_cliente, nuevo_nombre=None, nuevo_saldo=None):
        cliente = self.clientes.get(id_cliente)
        if not cliente:
            return F"{FALLA}Cliente no encontrado.{RESET}"
        if nuevo_nombre:
            cliente.nombre = nuevo_nombre
        if nuevo_saldo is not None:
            cliente.saldo = nuevo_saldo
        return f"{EXITO}Cliente {id_cliente} modificado con éxito.{RESET}"

    def eliminar_cliente(self, id_cliente):
        if id_cliente not in self.clientes:
            return F"{FALLA}Cliente no encontrado.{RESET}"
        del self.clientes[id_cliente]
        return f"{EXITO}Cliente {id_cliente} eliminado con éxito.{RESET}"

    def consultar_clientes(self):
        if not self.clientes:
            return F"{FALLA}No hay clientes registrados.{RESET}"
        resultado = F"{INFO}ID | Nombre | Saldo\n{RESET}"
        for cliente in self.clientes.values():
            resultado += f"{INFO}{cliente.id_cliente} | {cliente.nombre} | {cliente.saldo}\n{RESET}"
        return resultado

    # gestion de cajeros
    def agregar_cajero(self, id_cajero, ubicacion, billetes):
        if id_cajero in self.cajeros:
          return f"{FALLA}El cajero ya existe.{RESET}"
        self.cajeros[id_cajero] = Cajero(id_cajero, ubicacion, billetes)
        return (f"{EXITO}Cajero en {ubicacion} agregado con éxito.{RESET}\n"
            f"Billetes disponibles:\n"
            + "\n".join(f"  {denominacion}: {cantidad}" for denominacion, cantidad in billetes.items()))


    def modificar_cajero(self, id_cajero, nueva_ubicacion=None, nuevos_billetes=None):
        cajero = self.cajeros.get(id_cajero)
        if not cajero:
            return F"{FALLA}Cajero no encontrado.{RESET}"
        if nueva_ubicacion:
            cajero.ubicacion = nueva_ubicacion
        if nuevos_billetes:
            cajero.billetes.update(nuevos_billetes)
        return f"{EXITO}Cajero {id_cajero} modificado con éxito.{RESET}"

    def eliminar_cajero(self, id_cajero):
        if id_cajero not in self.cajeros:
            return F"{FALLA}Cajero no encontrado.{RESET}"
        del self.cajeros[id_cajero]
        return f"{EXITO}Cajero {id_cajero} eliminado con éxito.{RESET}"

    def consultar_cajeros(self):
        if not self.cajeros:
            return F"{FALLA}No hay cajeros registrados.{RESET}"
        resultado = "ID | Ubicación | Billetes Disponibles\n"
        for cajero in self.cajeros.values():
            resultado += f"{INFO}{cajero.id_cajero} | {cajero.ubicacion} | {cajero.billetes}\n{RESET}"
        return resultado

# operaciones
    def retirar(self, id_cliente, id_cajero, monto):
        cliente = self.clientes.get(id_cliente)
        cajero = self.cajeros.get(id_cajero)
        if not cliente:
            return F"{FALLA}Cliente no encontrado.{RESET}"
        if not cajero:
            return F"{FALLA}Cajero no encontrado.{RESET}"
        mensaje, desglose = cajero.desglosar_monto(monto)
        if desglose:
            cliente.saldo -= monto
            movimiento = Movimiento(None, "Retiro", monto, cliente_origen=cliente)
            self.registrar_movimiento(movimiento)
            return f"{EXITO}Retiro exitoso. Nuevo saldo: {cliente.saldo}\n{mensaje}\nDesglose: {desglose}{RESET}"
        return mensaje

    def depositar(self, id_cliente, id_cajero, monto):
        cliente = self.clientes.get(id_cliente)
        cajero = self.cajeros.get(id_cajero)
        if not cliente:
            return F"{FALLA}Cliente no encontrado.{RESET}"
        if not cajero:
            return F"{FALLA}Cajero no encontrado.{RESET}"
        cliente.saldo += monto
        cajero.actualizar_billetes(200, monto // 200)  # Ejemplo simple de actualización
        movimiento = Movimiento(None, F"Depósito", monto, cliente_origen=cliente)
        self.registrar_movimiento(movimiento)
        return f"{EXITO}Depósito exitoso. Nuevo saldo: {cliente.saldo}{RESET}"

    def transferir(self, id_cliente_origen, id_cliente_destino, monto):
        cliente_origen = self.clientes.get(id_cliente_origen)
        cliente_destino = self.clientes.get(id_cliente_destino)
        if not cliente_origen:
            return F"{FALLA}Cliente origen no encontrado.{RESET}"
        if not cliente_destino:
            return F"{FALLA}Cliente destino no encontrado.{RESET}"
        if cliente_origen.saldo < monto:
            return F"{FALLA}Saldo insuficiente para la transferencia.{RESET}"
        cliente_origen.saldo -= monto
        cliente_destino.saldo += monto
        movimiento = Movimiento(None, "Transferencia", monto, cliente_origen=cliente_origen, cliente_destino=cliente_destino)
        self.registrar_movimiento(movimiento)
        return f"{EXITO}Transferencia realizada con éxito. Saldo restante: {cliente_origen.saldo}{RESET}"

    def pagar_servicio(self, id_cliente, monto):
        cliente = self.clientes.get(id_cliente)
        if not cliente:
            return F"{FALLA}Cliente no encontrado.{RESET}"
        if cliente.saldo < monto:
            return F"{FALLA}Saldo insuficiente para pagar el servicio.{RESET}"
        cliente.saldo -= monto
        movimiento = Movimiento(None, "Pago de servicios", monto, cliente_origen=cliente)
        self.registrar_movimiento(movimiento)
        return f"{EXITO}Pago de servicio realizado con éxito. Nuevo saldo: {cliente.saldo}{RESET}"

    # movimientos
    def registrar_movimiento(self, movimiento):
        self.movimientos.append(movimiento)
        return F"{EXITO}Movimiento registrado con éxito.{RESET}"

    def consultar_movimientos(self):
        if not self.movimientos:
            return F"{FALLA}No hay movimientos registrados.{RESET}"
        return "\n".join(str(mov) for mov in self.movimientos)

    def consultar_movimientos_por_cliente(self, id_cliente):
        cliente = self.clientes.get(id_cliente)
        if not cliente:
            return F"{FALLA}Cliente no encontrado.{RESET}"
        movimientos_cliente = [mov for mov in self.movimientos if mov.cliente_origen == cliente or mov.cliente_destino == cliente]
        if not movimientos_cliente:
            return F"{INFO}No hay movimientos para este cliente.{RESET}"
        return "\n".join(str(mov) for mov in movimientos_cliente)

    def consultar_movimientos_por_tipo(self, tipo):
        movimientos_tipo = [mov for mov in self.movimientos if mov.tipo == tipo]
        if not movimientos_tipo:
            return f"{INFO}No hay movimientos del tipo '{tipo}'.{RESET}"
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
        return F"{EXITO}Datos guardados con éxito.{RESET}"

    def cargar_datos(self, ruta):
        with open(ruta, "r") as archivo:
            datos = json.load(archivo)
        for id, cliente in datos["clientes"].items():
            self.clientes[id] = Cliente(**cliente)
        for id, cajero in datos["cajeros"].items():
            self.cajeros[id] = Cajero(**cajero)
        self.movimientos = [Movimiento(**mov) for mov in datos["movimientos"]]
        return F"{EXITO}Datos cargados con éxito.{RESET}"
    

    def ordenar_clientes(self, clave):
        """
        Ordena la lista de clientes por clave ('id_cliente' o 'nombre').
        """
        lista_clientes = list(self.clientes.values())
        self.clientes = {cliente.id_cliente: cliente for cliente in quicksort_clientes(lista_clientes, clave)}
        return f"{EXITO}Clientes ordenados por {clave}.{RESET}"

    def buscar_cliente(self, id_cliente):
        """
        Busca un cliente por ID usando búsqueda binaria.
        :param id_cliente: ID del cliente a buscar.
        :return: Cliente encontrado o mensaje de error.
        """
        lista_clientes = list(self.clientes.values())
        lista_ordenada = quicksort_clientes(lista_clientes, 'id_cliente')
        cliente = busqueda_binaria(lista_ordenada, 'id_cliente', id_cliente)
        return cliente if cliente else F"{FALLA}Cliente no encontrado.{RESET}"

    def ordenar_cajeros(self, clave):
        """
        Ordena la lista de cajeros por clave ('id_cajero' o 'ubicacion').
        """
        lista_cajeros = list(self.cajeros.values())
        self.cajeros = {cajero.id_cajero: cajero for cajero in mergesort_cajeros(lista_cajeros, clave)}
        return f"{INFO}Cajeros ordenados por {clave}.{RESET}"


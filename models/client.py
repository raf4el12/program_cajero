from utils.colors_alert import EXITO, RESET, INFO, FALLA
class Cliente:
    def __init__(self, id_cliente, nombre, saldo, contraseña):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.saldo = saldo
        self.contraseña = contraseña
        self.movimientos = []  # Lista para registrar movimientos

    def registrar_movimiento(self, tipo, monto, cuenta_destino=None):
        """
        Registra un movimiento en el historial del cliente.
        """
        from datetime import datetime
        movimiento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": tipo,
            "monto": monto,
            "destino": cuenta_destino.id_cliente if cuenta_destino else None
        }
        self.movimientos.append(movimiento)
        return f"Movimiento registrado: {movimiento}"

    def depositar(self, monto):
        if monto <= 0:
            return "El monto debe ser mayor que 0."
        self.saldo += monto
        self.registrar_movimiento("Depósito", monto)
        return f"Depósito exitoso. Nuevo saldo: {self.saldo}"

    def retirar(self, monto):
        if monto <= 0:
            return "El monto debe ser mayor que 0."
        if monto > self.saldo:
            return "Saldo insuficiente para realizar el retiro."
        self.saldo -= monto
        self.registrar_movimiento("Retiro", monto)
        return f"Retiro exitoso. Nuevo saldo: {self.saldo}"

    def transferir(self, monto, cuenta_destino):
        if monto <= 0:
            return "El monto debe ser mayor que 0."
        if monto > self.saldo:
            return "Saldo insuficiente para realizar la transferencia."
        self.saldo -= monto
        cuenta_destino.saldo += monto
        self.registrar_movimiento("Transferencia", monto, cuenta_destino)
        return f"Transferencia exitosa. Nuevo saldo: {self.saldo}"

    def consultar_saldo(self):
        """
        Devuelve el saldo actual del cliente.
        """
        return f"Saldo actual: {self.saldo}"

    def consultar_movimientos(self):
        """
        Devuelve una lista de los movimientos realizados por el cliente.
        """
        if not self.movimientos:
            return "No hay movimientos registrados."

        resultado = "Historial de movimientos:\n"
        for movimiento in self.movimientos:
            resultado += (f"Fecha: {movimiento['fecha']} | "
                          f"Tipo: {movimiento['tipo']} | "
                          f"Monto: {movimiento['monto']} | "
                          f"Destino: {movimiento['destino']}\n")
        return resultado

    def cambiar_contraseña(self, contraseña_actual, nueva_contraseña):
        """
        Permite cambiar la contraseña del cliente.
        """
        if self.contraseña != contraseña_actual:
            return "La contraseña actual no es correcta."
        self.contraseña = nueva_contraseña
        return "Contraseña actualizada con éxito."

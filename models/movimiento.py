from datetime import datetime

class Movimiento:
    TIPOS_VALIDOS = ['Depósito', 'Retiro', 'Transferencia', 'Pago de servicios']

    def __init__(self, fecha, tipo, monto, cliente_origen=None, cliente_destino=None):
        """
        tipo: 'Depósito', 'Retiro', 'Transferencia', 'Pago de servicios'
        """
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de movimiento inválido: {tipo}. Debe ser uno de {self.TIPOS_VALIDOS}.")
        if monto <= 0:
            raise ValueError("El monto debe ser mayor que 0.")
        
        self.fecha = fecha or datetime.now()
        self.tipo = tipo
        self.monto = monto
        self.cliente_origen = cliente_origen
        self.cliente_destino = cliente_destino

    def __str__(self):
        origen = f"Origen: {self.cliente_origen}" if self.cliente_origen else "Origen: N/A"
        destino = f"Destino: {self.cliente_destino}" if self.cliente_destino else "Destino: N/A"
        return f"{self.fecha.strftime('%Y-%m-%d %H:%M:%S')} - {self.tipo}: {self.monto} ({origen}, {destino})"

    def to_dict(self):
        """
        Convierte el movimiento a un diccionario para facilitar su serialización.
        """
        return {
            "fecha": self.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            "tipo": self.tipo,
            "monto": self.monto,
            "cliente_origen": self.cliente_origen,
            "cliente_destino": self.cliente_destino
        }

    @staticmethod ## metodo static !
    def filtrar_por_tipo(movimientos, tipo):
        """
        Filtra una lista de movimientos por tipo.
        """
        return [mov for mov in movimientos if mov.tipo == tipo]

    @staticmethod ## metodo static !
    def filtrar_por_cliente(movimientos, cliente):
        """
        Filtra una lista de movimientos relacionados con un cliente.
        """
        return [mov for mov in movimientos if mov.cliente_origen == cliente or mov.cliente_destino == cliente]
 
    @classmethod 
    def crear_movimiento(cls, tipo, monto, cliente_origen=None, cliente_destino=None):
        """
        Crea un nuevo movimiento con validaciones automáticas.
        """
        return cls(None, tipo, monto, cliente_origen, cliente_destino)

from datetime import datetime

class Cajero:
    def __init__(self, id_cajero, ubicacion, billetes):
        """
        billetes: diccionario con denominaciones como clave y cantidad como valor.
        """
        self.id_cajero = id_cajero
        self.ubicacion = ubicacion
        self.billetes = billetes
        self.operaciones = []  # lista para registrar las operaciones

    def actualizar_billetes(self, denominacion, cantidad):
        """
        Actualiza los billetes del cajero con validaciones.
        """
        if cantidad < 0:
            return "La cantidad no puede ser negativa."
        if denominacion not in [200, 100, 50, 20, 10]:
            return "Denominación no válida. Solo se aceptan: 200, 100, 50, 20, 10."

        if denominacion in self.billetes:
            self.billetes[denominacion] += cantidad
        else:
            self.billetes[denominacion] = cantidad
        return f"Billetes actualizados: {self.billetes}"

    def desglosar_monto(self, monto):
        """
        Devuelve un desglose del monto en billetes disponibles, si es posible.
        """
        desglose = {}
        for denominacion in sorted(self.billetes.keys(), reverse=True):
            if monto == 0:
                break
            if denominacion <= monto and self.billetes[denominacion] > 0:
                num_billetes = min(monto // denominacion, self.billetes[denominacion])
                desglose[denominacion] = num_billetes
                monto -= num_billetes * denominacion

        if monto > 0:
            return "No se puede desglosar el monto {monto_original} con los billetes disponibles.", None
           
            ## AQUI VAMOS A ACTUALIZAR LOS BILLETES DEL CAJERO
            
        for denom, cantidad in desglose.items():
            self.billetes[denom] -= cantidad

        return True, f"Desglose exitoso: {desglose}"

    def calcular_total_disponible(self):
        """
        Calcula el total de dinero disponible en el cajero.
        """
        return sum(denominacion * cantidad for denominacion, cantidad in self.billetes.items())

    def validar_fondos(self, monto):
        """
        Verifica si el cajero tiene suficientes fondos para cubrir el monto solicitado
        """
        total_disponible = self.calcular_total_disponible()
        if monto > total_disponible:
            return False, "Fondos insuficientes en el cajero."
        return True, "Fondos suficientes."

    def registrar_operacion(self, tipo, monto):
        """
        Registra una operacion realizada en el cajero
        """
        operacion = {
            "tipo": tipo,
            "monto": monto,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.operaciones.append(operacion)
        return f"Operación registrada: {operacion}"

    def mostrar_resumen(self):
        """
        Devuelve un resumen del estado actual del cajero
        """
        total_disponible = self.calcular_total_disponible()
        return (f"Cajero ID: {self.id_cajero}\n"
                f"Ubicación: {self.ubicacion}\n"
                f"Billetes Disponibles: {self.billetes}\n"
                f"Total Disponible: {total_disponible}")
    
    def agregar_billetes(self, billetes_a_agregar):
        """
        Agrega billetes al cajero.
        :param billetes_a_agregar: Diccionario con billetes a agregar.
        """
        for denominacion, cantidad in billetes_a_agregar.items():
            if cantidad <= 0:
                return f"Error: La cantidad de billetes a agregar debe ser positiva. Denominación: {denominacion}."
            if denominacion in self.billetes:
                self.billetes[denominacion] += cantidad
            else:
                self.billetes[denominacion] = cantidad
        return f"Billetes agregados: {billetes_a_agregar}"
        

    def mostrar_operaciones(self):
        """
    Devuelve un resumen de todas las operaciones realizadas en el cajero.
    """
        if not self.operaciones:
            return "No hay operaciones registradas en este cajero."

        resumen = "Operaciones registradas:\n"
        for operacion in self.operaciones:
            resumen += (f"{operacion['fecha']} - {operacion['tipo']}: "
                    f"{operacion['monto']}\n")
        return resumen



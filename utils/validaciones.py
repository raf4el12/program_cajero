### VALIDACIONES !
def validar_saldo_disponible(saldo, monto):
    """
    Verifica si el saldo es suficiente para realizar la operación.
    :param saldo: Saldo actual del cliente.
    :param monto: Monto que se desea retirar o transferir.
    :return: (bool, str) -> True si es valido, False en caso contrario, y un mensaje.
    """
    if monto <= 0:
        return False, "El monto debe ser mayor que 0."
    if monto > saldo:
        return False, "Saldo insuficiente para completar la operación."
    return True, "Saldo disponible para la operación."

def validar_contraseña(contraseña_ingresada, contraseña_real):
    """
    Verifica si la contraseña ingresada coincide con la registrada
    :param contraseña_ingresada: Contraseña proporcionada por el usuario
    :param contraseña_real: Contraseña almacenada del cliente
    :return: (bool, str) -> True si coinciden, False en caso contrario, y un mensaje
    """
    if contraseña_ingresada == contraseña_real:
        return True, "Contraseña válida."
    return False, "Contraseña incorrecta."

def validar_monto(monto):
    """
    Valida que el monto ingresado sea un número positivo y múltiplo de las denominaciones permitidas.
    :param monto: Monto que se desea validar.
    :return: (bool, str) -> True si el monto es válido, False en caso contrario, y un mensaje.
    """
    if monto <= 0:
        return False, "El monto debe ser un número positivo."
    if monto % 10 != 0:
        return False, "El monto debe ser múltiplo de 10."
    return True, "Monto válido."

def validar_billetes_disponibles(monto, billetes):
    """
    Verifica si hay billetes suficientes para cubrir el monto solicitado
    :param monto: Monto que se desea retirar
    :param billetes: Diccionario con denominaciones y cantidades de billetes disponibles
    :return: (bool, str) -> True si hay suficientes billetes, False en caso contrario, y un mensaje
    """
    total_disponible = sum(denominacion * cantidad for denominacion, cantidad in billetes.items())
    if monto > total_disponible:
        return False, "El cajero no tiene suficientes billetes para este monto."
    return True, "Billetes disponibles para el monto solicitado."

def validar_cliente_existente(clientes, id_cliente):
    """
    Verifica si un cliente con un ID específico ya existe en el sistema
    :param clientes: Diccionario con los clientes registrados
    :param id_cliente: ID del cliente a validar
    :return: (bool, str) -> True si el cliente no existe, False si ya existe, y un mensaje
    """
    if id_cliente in clientes:
        return False, f"El cliente con ID {id_cliente} ya existe."
    return True, "El cliente no existe, puede ser registrado"

def validar_cajero_existente(cajeros, id_cajero):
    """
    Verifica si un cajero con un ID específico ya existe en el sistema
    :param cajeros: Diccionario con los cajeros registrado
    :param id_cajero: ID del cajero a validar
    :return: (bool, str) -> True si el cajero no existe, False si ya existe, y un mensaje.
    """
    if id_cajero in cajeros:
        return False, f"El cajero con ID {id_cajero} ya existe."
    return True, "El cajero no existe, puede ser registrado."

def validar_opcion_menu(opcion, opciones_validas):
    """
    Valida que la opción ingresada por el usuario sea válida dentro de las opciones permitidas
    :param opcion: Opción ingresada por el usuario
    :param opciones_validas: Lista o conjunto de opciones válidas
    :return: (bool, str) -> True si la opción es válida, False en cas contrario, y un mensaje
    """
    if opcion in opciones_validas:
        return True, "Opción válida."
    return False, f"Opción inválida. Por favor, elija una opción válida: {opciones_validas}."


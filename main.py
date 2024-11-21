

from models.sistema_cajero import SistemaCajero

def mostrar_menu():
    print("\n=== Sistema Cajero ===")
    print("1. Agregar cliente")
    print("2. Modificar cliente")
    print("3. Eliminar cliente")
    print("4. Consultar clientes")
    print("5. Agregar cajero")
    print("6. Modificar cajero")
    print("7. Eliminar cajero")
    print("8. Consultar cajeros")
    print("9. Retirar dinero")
    print("10. Depositar dinero")
    print("11. Transferir dinero")
    print("12. Pagar servicio")
    print("13. Consultar movimientos")
    print("14. Guardar datos")
    print("15. Cargar datos")
    print("16. Salir")
    return input("Seleccione una opción: ")


if __name__ == "__main__":
    sistema = SistemaCajero()
    while True:
        opcion = mostrar_menu()
        if opcion == "1":  # agregamos cliente
            id_cliente = input("ID del cliente: ")
            nombre = input("Nombre: ")
            saldo = float(input("Saldo inicial: "))
            contraseña = input("Contraseña: ")
            print(sistema.agregar_cliente(id_cliente, nombre, saldo, contraseña))

        elif opcion == "2":  # moficamos cliente update
            id_cliente = input("ID del cliente: ")
            nuevo_nombre = input("Nuevo nombre (deja vacío para no cambiar): ")
            nuevo_saldo = input("Nuevo saldo (deja vacío para no cambiar): ")
            nuevo_saldo = float(nuevo_saldo) if nuevo_saldo else None
            print(sistema.modificar_cliente(id_cliente, nuevo_nombre, nuevo_saldo))

        elif opcion == "3":  # eliminamos cliente
            id_cliente = input("ID del cliente: ")
            print(sistema.eliminar_cliente(id_cliente))

        elif opcion == "4":  # consultar clientes
            print(sistema.consultar_clientes())

        elif opcion == "5":  # agregamos cajero
            id_cajero = input("ID del cajero: ")
            ubicacion = input("Ubicación: ")
            billetes = eval(input("Billetes disponibles (ejemplo: {200: 10, 100: 20}): "))
            print(sistema.agregar_cajero(id_cajero, ubicacion, billetes))

        elif opcion == "6":  # Modificamos cajero
            id_cajero = input("ID del cajero: ")
            nueva_ubicacion = input("Nueva ubicación (deja vacío para no cambiar): ")
            nuevos_billetes = input("Nuevos billetes (deja vacío para no cambiar, ejemplo: {200: 5}): ")
            nuevos_billetes = eval(nuevos_billetes) if nuevos_billetes else None
            print(sistema.modificar_cajero(id_cajero, nueva_ubicacion, nuevos_billetes))

        elif opcion == "7":  # Eliminamos cajero
            id_cajero = input("ID del cajero: ")
            print(sistema.eliminar_cajero(id_cajero))

        elif opcion == "8":  # consultar cajeros
            print(sistema.consultar_cajeros())

        elif opcion == "9":  # retiramos el dinero
            id_cliente = input("ID del cliente: ")
            id_cajero = input("ID del cajero: ")
            monto = float(input("Monto a retirar: "))
            print(sistema.retirar(id_cliente, id_cajero, monto))

        elif opcion == "10":  # depositamos el dinero
            id_cliente = input("ID del cliente: ")
            id_cajero = input("ID del cajero: ")
            monto = float(input("Monto a depositar: "))
            print(sistema.depositar(id_cliente, id_cajero, monto))

        elif opcion == "11":  # transferimos el dinero que desee
            id_cliente_origen = input("ID del cliente origen: ")
            id_cliente_destino = input("ID del cliente destino: ")
            monto = float(input("Monto a transferir: "))
            print(sistema.transferir(id_cliente_origen, id_cliente_destino, monto))

        elif opcion == "12":  # pagamos los servicios
            id_cliente = input("ID del cliente: ")
            monto = float(input("Monto a pagar: "))
            print(sistema.pagar_servicio(id_cliente, monto))

        elif opcion == "13":  # consultamos lo movimientos
            print(sistema.consultar_movimientos())

        elif opcion == "14":  # guardamos los datos
            ruta = input("Ruta del archivo para guardar datos (ejemplo: datos.json): ")
            print(sistema.guardar_datos(ruta))

        elif opcion == "15":  # cargamos datos
            ruta = input("Ruta del archivo para cargar datos (ejemplo: datos.json): ")
            print(sistema.cargar_datos(ruta))

        elif opcion == "16":  # salimos del program
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

import socket

HOST = "127.0.0.1"  # Cambiar por IP del servidor en LAN
PORT = 5000
BUFFER_SIZE = 1024


def menu():
    print("\n=== MINI NUBE PERSONAL ===")
    print("1. Listar archivos")
    print("2. Subir archivo")
    print("3. Descargar archivo")
    print("4. Salir")


while True:
    menu()
    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        client = socket.socket()
        client.connect((HOST, PORT))
        client.send(b"LISTAR")
        print(client.recv(4096).decode())
        client.close()

    elif opcion == "2":
        archivo = input("Nombre del archivo a subir: ")
        try:
            client = socket.socket()
            client.connect((HOST, PORT))
            client.send(f"SUBIR {archivo}".encode())
            with open(archivo, "rb") as f:
                for chunk in iter(lambda: f.read(BUFFER_SIZE), b""):
                    client.send(chunk)
            client.send(b"FIN")
            print(client.recv(1024).decode())
            client.close()
        except FileNotFoundError:
            print("Archivo no encontrado en tu PC")

    elif opcion == "3":
        archivo = input("Nombre del archivo a descargar: ")
        client = socket.socket()
        client.connect((HOST, PORT))
        client.send(f"DESCARGAR {archivo}".encode())
        with open("descargado_" + archivo, "wb") as f:
            while True:
                data = client.recv(BUFFER_SIZE)
                if data == b"FIN":
                    break
                elif data.startswith(b"ERROR"):
                    print(data.decode())
                    break
                f.write(data)
        client.close()
        print("Archivo descargado")

    elif opcion == "4":
        print("Saliendo de la nube")
        break

    else:
        print("Opción inválida")

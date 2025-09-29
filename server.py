import socket
import os

# Configuración del servidor
HOST = "0.0.0.0"  # Escucha en todas las interfaces
PORT = 5000

BUFFER_SIZE = 1024
FOLDER = "nube_files"

# Crear carpeta si no existe
if not os.path.exists(FOLDER):
    os.makedirs(FOLDER)

# Crear socket TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"Servidor de nube iniciado en {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print(f"Conectado con {addr}")

    opcion = conn.recv(BUFFER_SIZE).decode()

    if opcion == "LISTAR":
        archivos = os.listdir(FOLDER)
        conn.send("\n".join(archivos).encode() if archivos else b"(Nube vacia)")

    elif opcion.startswith("SUBIR"):
        _, filename = opcion.split(" ")
        with open(os.path.join(FOLDER, filename), "wb") as f:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if data == b"FIN":
                    break
                f.write(data)
        conn.send(b"Archivo subido con exito")

    elif opcion.startswith("DESCARGAR"):
        _, filename = opcion.split(" ")
        filepath = os.path.join(FOLDER, filename)
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(BUFFER_SIZE), b""):
                    conn.send(chunk)
            conn.send(b"FIN")
        else:
            conn.send(b"ERROR: Archivo no encontrado")

    conn.close()

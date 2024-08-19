import psutil
import platform
import requests
import subprocess
import os

def obtener_usuarios():
    usuarios = []
    sistema_operativo = platform.system()
    
    if sistema_operativo == "Windows":
        # Obtener usuarios en Windows
        resultado = subprocess.run(['net', 'user'], capture_output=True, text=True)
        usuarios = resultado.stdout.splitlines()
        # Filtrar la salida para obtener solo los nombres de usuario
        usuarios = [line.strip() for line in usuarios if line.strip() and not line.startswith("-------------------------------------------------------------------------------")]
    
    elif sistema_operativo == "Linux":
        # Obtener usuarios en Linux
        with open('/etc/passwd') as f:
            for line in f:
                partes = line.split(':')
                usuarios.append(partes[0])
    
    return usuarios

def obtener_informacion():
    info = {
        "procesador": platform.processor(),
        "procesos": [
            proc.info 
            for proc in psutil.process_iter(['pid', 'name', 'status']) 
            if proc.info['status'] == psutil.STATUS_RUNNING
        ],
        "usuarios_activos": psutil.users(),  # Usuarios actualmente conectados
        "todos_los_usuarios": obtener_usuarios(),  # Todos los usuarios en la máquina
        "sistema_operativo": platform.system(),
        "version_sistema": platform.version()
    }
    return info

print(obtener_informacion())

def enviar_informacion(info, url):
    response = requests.post(url, json=info)
    return response.status_code

if __name__ == "__main__":
    url_api = ""  # Especifica aquí la URL de la API a la que enviar la información
    info = obtener_informacion()
    status = enviar_informacion(info, url_api)
    print(f"Envio completado con estado: {status}")
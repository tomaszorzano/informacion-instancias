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
        "usuarios_activos": [user._asdict() for user in psutil.users()],  # Convertir a dict
        "todos_los_usuarios": obtener_usuarios(),  # Todos los usuarios en la máquina
        "sistema_operativo": platform.system(),
        "version_sistema": platform.version()
    }
    return info

def enviar_informacion(info, url):
    response = requests.post(url, json=info)
    return response.status_code

if __name__ == "__main__":
    base_url = "https://t3jxqxig0f.execute-api.us-east-1.amazonaws.com/dev"
    endpoint_guardar = f"{base_url}/guardar"
    
    # Obtener información de la instancia
    info = obtener_informacion()
    
    # Enviar información a la API
    status = enviar_informacion(info, endpoint_guardar)
    print(f"Envío completado con estado: {status}")
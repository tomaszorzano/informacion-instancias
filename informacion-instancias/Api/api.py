from flask import Flask, request, jsonify
import csv
import os
import boto3
from io import StringIO
from datetime import datetime

app = Flask(__name__)

S3_BUCKET = os.environ.get('S3_BUCKET') 
s3_client = boto3.client('s3')

@app.route('/guardar', methods=['POST'])
def guardar_informacion():
    data = request.json
    ip_cliente = request.remote_addr
    fecha = datetime.now().strftime("%Y-%m-%d")
    filename = f"{ip_cliente}_{fecha}.csv"
    
    keys = data.keys()

    csv_buffer = StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=keys)
    writer.writeheader()
    writer.writerow(data)
   
    try:
        s3_client.put_object(Bucket=S3_BUCKET, Key=filename, Body=csv_buffer.getvalue())
        return "Información guardada en S3", 200
    except Exception as e:
        return f"Error al guardar en S3: {str(e)}", 500

@app.route('/consultar/<ip>', methods=['GET'])
def consultar_informacion(ip):
    fecha = datetime.now().strftime("%Y-%m-%d")
    filename = f"{ip}_{fecha}.csv"
    
    try:
    
        s3_object = s3_client.get_object(Bucket=S3_BUCKET, Key=filename)
        csv_content = s3_object['Body'].read().decode('utf-8')
        
        csv_buffer = StringIO(csv_content)
        reader = csv.DictReader(csv_buffer)
        data = list(reader)
        
        return jsonify(data), 200
    except Exception as e:
        return f"No se encontró información: {str(e)}", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
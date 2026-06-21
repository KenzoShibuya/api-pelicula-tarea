import boto3
import uuid
import os
import json # Importante para formatear el log para CloudWatch

def lambda_handler(event, context):
    try:
        # Log de entrada estandarizado (INFO)
        log_entrada = {
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Iniciando lambda CrearPelicula",
                "evento_recibido": event
            }
        }
        print(json.dumps(log_entrada))
        
        # Extracción de datos
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]
        
        # Proceso
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)
        
        # Log de éxito estandarizado (INFO)
        log_exito = {
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Película insertada exitosamente en DynamoDB",
                "registro": pelicula
            }
        }
        print(json.dumps(log_exito))
        
        # Salida exitosa (json)
        return {
            'statusCode': 200,
            'pelicula': pelicula
        }
        
    except Exception as e:
        # Log de error estandarizado (ERROR)
        log_error = {
            "tipo": "ERROR",
            "log_datos": {
                "mensaje": "Fallo en la ejecución del Lambda",
                "detalle_error": str(e)
            }
        }
        print(json.dumps(log_error))
        
        # Salida de error (json)
        return {
            'statusCode': 500,
            'error': 'Ocurrió un error interno en el servidor.'
        }
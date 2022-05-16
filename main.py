#!/usr/bin/env python3

# Imports
import boto3
from botocore.client import ClientError
import os

# Credenciales de acceso a S3
KEY = 'AKIA2NU5TZR6RVMXSOKK'
SECRET_KEY = '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'
S3 = boto3.resource('s3', aws_access_key_id=KEY, aws_secret_access_key=SECRET_KEY)


def listar_bucket(bucket='desafio-rkd'):
    """Funcion para listar los archivos de un S3.
    
    Keyword arguments:
    bucket -- nombre del bucket de s3. Por defecto es desafio-rkd.
    Return: lista de archivos dentro del bucket.
    """
    
    try:
        # Recorre e imprime los archivos del bucket.
        print('\n---- Archivos del bucket ----')
        for object in S3.Bucket(bucket).objects.all():
            print(f'- {object.key}')
            
    # Arroja un error en caso de que el bucket no exista.
    except ClientError:
        raise SystemExit('\n---- ERROR ----\nEl bucket no existe o no tenes acceso.')


def chequear_directorio(download_path):
    """Funcion para chequear si el directorio de descarga existe.
        Si existe, no hace nada.
        Si no existe, lo crea.
    
    Keyword arguments:
    download_path (string) -- ruta donde se almacenara el archivo. Si es una cadena vacia, tomara el valor 'data'.
    
    Return: ruta del directorio de descarga.
    """
    
    if download_path == '':
        os.mkdir('data') if not os.path.exists('data') else None
        return './data'
    else:
        os.makedirs(download_path) if not os.path.exists(download_path) else None
        return download_path


def descargar_datos(filename, download_path, bucket='desafio-rkd'):
    """Funcion para descargar datos desde un S3. Permite cambiar el repositorio de datos y la ruta de descarga. Se permite la descarga de archivos como csv.
    
    Keyword arguments:
    filename (string) -- nombre del archivo que se desea descargar.
    bucket (string) -- nombre del bucket de s3. Por defecto es desafio-rkd.
    download_path (string) -- ruta donde se almacenara el archivo. Por defecto se almacena en la carpeta data.
    
    Return: archivo descargado.
    """
    download_path = chequear_directorio(download_path)
    
    try:
        # Si no recibe ningun parametro, recorre todos los archivos del bucket y los descarga.
        if filename == '':
            for filename in S3.Bucket(bucket).objects.all():
                S3.Bucket(bucket).download_file(filename.key, f'{download_path}/{filename.key}')
        # Si recibe un parametro, descarga el archivo especificado.
        else:
            S3.Bucket(bucket).download_file(filename, f'{download_path}/{filename}')
            
        print('\nDESCARGA COMPLETA.')
    
    # Arroja un error en caso de que el archivo no exista.
    except ClientError:
        raise SystemExit('\n---- ERROR ----\nEl archivo no existe o no tenes acceso.')


def ingresar_datos():
    """Funcion que lee los datos ingresados por el usuario y en base a estos datos, descarga archivos de un bucket de S3."""
    
    bucket = input('Ingrese el nombre del bucket.\
        \nPresione ENTER para dejar el bucket por defecto (desafio-rkd): ')
    listar_bucket(bucket) if bucket != "" else listar_bucket()
    
    filename = input('\nIngrese el nombre del archivo que desea descargar.\
                     \nPresione ENTER para descargar todos los archivos: ')
    
    ruta = input('\nIngrese la ruta donde se almacenaran los archivos.\
                 \n  - «./nombreRuta» para el directorio actual.\
                 \n  - «/ruta1/ruta2/...» para rutas absolutas.\
                 \nPresione ENTER para dejar la ruta por defecto (./data): ')
    
    respuesta = input('\nChequee los datos ingresados anteriormente.\
                        \n¿Desea iniciar la descarga? (s/n): ') 
    
    descargar_datos(filename, ruta) if respuesta == 's' or respuesta == 'S' else print('DESCARGA CANCELADA.')
    
    
if(__name__ == '__main__'):
    ingresar_datos()
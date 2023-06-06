import subprocess
from itertools import product
import threading
import os
from siamese_operations import execute_index_siamese
import shutil
import pandas as pd
from siamese_operations import format_siamese_output
from confusion_matrix import generate_confusion_matrix
import os

def check_siamese_execution(process):
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        print('Process executed successfully')
    else:
        print('Error during process execution')

def most_recent_file(directory):
    files = os.listdir(directory)
    paths = [os.path.join(directory, file) for file in files]
    most_recent = max(paths, key=os.path.getctime)
    most_recent_name = os.path.basename(most_recent)
    return most_recent_name

def get_config_path(parms):
    clonesSize = f'cloneSize-{parms["minCloneSize"]}_'
    qrNorm = f'qrNorm-{parms["QRPercentileNorm"]}_'
    qrT2 = f'qrT2-{parms["QRPercentileT2"]}_'
    qrT1 = f'qrT1-{parms["QRPercentileT1"]}_'
    qrOrig = f'qrOrig-{parms["QRPercentileOrig"]}_'
    normBoost = f'normBoost-{parms["normBoost"]}_'
    t2Boost = f't2Boost-{parms["t2Boost"]}_'
    t1Boost = f't1Boost-{parms["t1Boost"]}_'
    origBoost = f'origBoost-{parms["origBoost"]}'
    config_name = clonesSize + qrNorm + qrT2 + qrT1 + qrOrig + t2Boost + t1Boost + origBoost
    destination_file = './configurations_hyperparameters'
    return f'{destination_file}/{config_name}.properties'

def generate_config_file(parms):
    config = open('search-config.properties', 'r').read()
    config = config.replace('minCloneSize=6', f'minCloneSize={parms["minCloneSize"]}')
    config = config.replace('QRPercentileNorm=10', f'QRPercentileNorm={parms["QRPercentileNorm"]}')
    config = config.replace('QRPercentileT2=10', f'QRPercentileT2={parms["QRPercentileT2"]}')
    config = config.replace('QRPercentileT1=10', f'QRPercentileT1={parms["QRPercentileT1"]}')
    config = config.replace('QRPercentileOrig=10', f'QRPercentileOrig={parms["QRPercentileOrig"]}')
    config = config.replace('normBoost=4', f'normBoost={parms["normBoost"]}')
    config = config.replace('t2Boost=4', f't2Boost={parms["t2Boost"]}')
    config = config.replace('t1Boost=4', f't1Boost={parms["t1Boost"]}')
    config = config.replace('origBoost=1', f'origBoost={parms["origBoost"]}')
    
    properties_path = get_config_path(parms)
    open(properties_path, 'w').write(config)
    return properties_path

def execute_siamese_search(**parms):
    project = 'stackoverflow_dump'
    output_path = '/home/denis/Hyperparameter-Optimization-Siamese/Siamese-main/output'
    properties_path = generate_config_file(parms)
    command = f'cd Siamese-main && java -jar siamese-0.0.6-SNAPSHOT.jar -c search -i ./my_index/{project}/ -o ./output -cf ../{properties_path}'
    process = subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    process.wait()
    check_siamese_execution(process)
    print("NOOOOOOOOOOOOO")
    most_recent_siamese_output = most_recent_file(output_path)
    df_siamese = format_siamese_output(output_path, most_recent_siamese_output)
    df_clones = pd.read_csv('clones.csv')
    return generate_confusion_matrix(df_siamese, df_clones)

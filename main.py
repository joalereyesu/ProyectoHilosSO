import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import os
import time
import shutil
import sys

# EN NUESTRO CODIGO SE CREA UNA NUEVA IMAGEN EN DOCKER CADA VEZ QUE SE CORREN LOS COMANDOS

def compute_statistics(data, num_workers=1, parallel=False):
    stats = {}
    columns = [col for col in data.columns if col != 'dates'] 
    # Si es paralelo se inicializa la ThreadPool para procesar en paralelo las estadisticas de los archivos
    if parallel:
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            results = list(executor.map(lambda col: (col, {
                'mean': np.mean(data[col]),
                'std': np.std(data[col]),
                'count': len(data[col]),
                'min': np.min(data[col]),
                'max': np.max(data[col])
            }), columns))
            for col, result in results:
                stats[col] = result
    #Si no es en paralelo, las estadisticas se generan sencuencialmente. 
    else:
        for column in columns:
            stats[column] = {
                'mean': np.mean(data[column]),
                'std': np.std(data[column]),
                'count': len(data[column]),
                'min': np.min(data[column]),
                'max': np.max(data[column])
            }
    return stats

# Funcion para decidir si los archivos se van a procesar, ya sea secuencial o en paralelo
def process_files_sequentially(data_folder, stats_function, num_workers=1, parallel_stats=False):
    start_time = time.time()
    files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith('.csv')]
    if parallel_stats:
        # Si es en paralelo, se utilizo ThreadPoolExecutor para manejar el procesamiento de los datos
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            results = list(executor.map(lambda file_path: process_file(file_path, stats_function, num_workers, parallel_stats), files)) # Se manda a llamar la funcion de abajo
                                                                                                                    # para procesar los archivos
    else:
        # Si no es paralelo se procesan los archivos uno por uno (secuencialmente)
        for file_path in files:
            process_file(file_path, stats_function, num_workers, parallel_stats)
    return time.time() - start_time

# En esta funcion es donde se procesan los archivos
def process_file(file_path, stats_function, num_workers, parallel_stats):
    print(f"Processing file: {file_path}")
    data = pd.read_csv(file_path)
    stats = stats_function(data, num_workers, parallel_stats)
    # Convert the nested dictionary to a DataFrame
    output_df = pd.DataFrame.from_dict({(i, j): stats[i][j] 
                                        for i in stats.keys() 
                                        for j in stats[i].keys()},
                                       orient='index')
    if isinstance(output_df.index, pd.MultiIndex):
        output_df = output_df.unstack().transpose()
        output_df.columns = output_df.columns.droplevel(0)
    output_df.reset_index(inplace=True, drop=True)
    output_path = os.path.join('so_output', os.path.basename(file_path).replace('.csv', '_output.csv'))
    output_df.to_csv(output_path, header=True, index=False)

def main(num_workers):
   # Vacio el folder so_output si existen archivos ya creados
    output_dir = 'so_output'
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    else:
        os.makedirs(output_dir)
    
    # Medir tiempos para diferentes modos de paralelismo
    start_time = time.time()
    sequential_time = process_files_sequentially('so_data', compute_statistics, 1, parallel_stats=False)
    end_time = time.time()
    total_sequential_time = end_time - start_time

    start_time = time.time()
    parallel_files_time = process_files_sequentially('so_data', compute_statistics, num_workers, parallel_stats=True)
    end_time = time.time()
    total_parallel_files_time = end_time - start_time

    start_time = time.time()
    parallel_functions_time = process_files_sequentially('so_data', compute_statistics, 1, parallel_stats=True)
    end_time = time.time()
    total_parallel_functions_time = end_time - start_time

    # Se utiliza la misma funcion process_files_sequentially, lo unico que cambia son los parametros en donde se especifican los
    # hilos (workers) y si es paralelo o no. Dentro de la funcion process_files_sequentially se condicona para ver si se realiza secuencial o
    # en paralelo. 

    # Guardar los tiempos en un archivo CSV
    times = {
        "Model": ["Sequential", "Parallel Files", "Parallel Functions"],
        "Time": [total_sequential_time, total_parallel_files_time, total_parallel_functions_time]
    }
    df_times = pd.DataFrame(times)
    # Guardar los tiempos en un archivo CSV en el directorio de salida
    df_times.to_csv(os.path.join(output_dir, "timing_results.csv"), index=False)


    print(f"Processing files with {num_workers} threads.")
    print(f"Sequential processing time: {total_sequential_time}")
    print(f"Parallel files processing time: {total_parallel_files_time}")
    print(f"Parallel functions processing time: {total_parallel_functions_time}")

if __name__ == "__main__":
    num_workers = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    main(num_workers)

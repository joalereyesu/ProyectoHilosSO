# ProyectoHilosSO

### Comandos a correr:
```
docker build -t parallel-processing-app .
chmod -R 777 so_output
docker run -m 1g --cpus=“<num_cores>” -v $(pwd)/so_output:/app/so_output parallel-processing-app python main.py <num_hilos>
```
## Preguntas
#### 1.	¿Cuál es el modelo de paralelismo más rápido en los 6 escenarios?
De acuerdo a los datos recolectados en nuestras iteraciones, el modelo de paralelismo que paraleliza los archivos con 2 cores y 2 hilos muestra el menor tiempo de procesamiento. Este resultado se puede explicar a través de la Ley de Amdahl, que dice que la mejora en el rendimiento debido al paralelismo está limitada por la parte del proceso que debe ser secuencial. En este caso, parece que el balance entre la parte paralelizable y la secuencial del trabajo es óptimo en 2 cores - 2 hilos, donde la sobrecarga de la gestión del paralelismo no supera el beneficio obtenido de la ejecución en paralelo.

#### 2. ¿Cuál opción de modelo de paralelismo tomaría usted y por qué?
Tomariamos la opcion de paralelizar archivos con 2 cores y 2 hilos, porque es el escenario que que ofrece el mejor tiempo sin agregar complejidad o sobrecarga adicional. La ley de Amdahl dice que aumentar el numero de hilos y cores mas alla de cierto punto no siempre resulta en una mejora. Las demas opciones a pesar de tener mas cores y mas hilos no tuvieron un tiempo tan bueno como el que mencionamos. 

#### 3. ¿Recomendaría paralelizar tanto archivos como funciones al mismo tiempo?
Basándome en los resultados, recomendaría paralelizar a nivel de archivo en lugar de funciones, ya que no parece haber una mejora significativa al paralelizar las funciones. La paralelizacion de archivos demuestra ser mas eficaz en los resultados obtenidos. 

#### 4. ¿Cuál es el factor de mejora de pasar de 1 Core a 2 Core para el proceso que paraleliza los archivos?
El factor de mejora de pasar de 1 core - 1 hilo a 2 cores - 2 hilos es de aproximadamente 1.17. Esto significa un speedup modesto.

#### 5. Determine el factor teórico de mejora para el escenario de 2 Core (Ley de Amdahl) al paralelizar por archivo y función estadística
La ley de Amdahl establece que el speedup de un programa es limitado por la fraccion del programa que no se puede paralelizar. 

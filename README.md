# ProyectoHilosSO

### Comandos a correr:
```
docker build -t parallel-processing-app .
chmod -R 777 so_output
docker run -m 1g --cpus=“<num_cores>” -v $(pwd)/so_output:/app/so_output parallel-processing-app python main.py <num_hilos>

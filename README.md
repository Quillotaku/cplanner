# cplanner
Script para sacar el máximo partido a la suscripción de Cinesa Unlimited

# Pasos previos
1. Instalar los requirements `pip3 install -r requirements.txt`

# Uso
- `python3 cplanner.py CSV [--exclude/include movie1,movie2,...,movieN]`
  - `CSV`: Nombre del fichero CSV (dentro de la ruta) para calcular la sesión máxima.
    - Formato: Movie,Duration,Session
    - Una linea por cada sesión disponible de la película.
    - Se puede usar el script de `cscraper` para conseguir el csv mas fácilmente.
  - `--exclude`: OPCIONAL. Lista de películas separadas con coma para excluir del CSV (todas menos las seleccionadas). 
  - `--include`: OPCIONAL. Lista de películas separadas con coma para incluir del CSV (solo las seleccionadas).
  - Se usa argumentos posicionales:
    - `CSV`: Posición 1.
    - `--exclude`: Posición 2. Utilizar si no se usa `--include`.
    - `--include`: Posición 2. Utilizar si no se usa `--exclude`.

Hace un print de la las películas en orden y a que sesión hay que ver. 
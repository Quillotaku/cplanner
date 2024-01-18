# cplanner
Script para sacar el máximo partido a la suscripción de Cinesa Unlimited

# Pasos previos
1. Instalar los requirements `pip3 install -r requirements.txt`

# Uso
- `python3 cplanner.py CSV`
- `CSV`: Nombre del fichero CSV (dentro de la ruta) para calcular la sesión máxima.
  - Formato: Movie,Duration,Session
  - Una linea por cada sesión disponible de la película.
  - Se puede usar el script de `cscraper` para conseguir el csv mas fácilmente.

Hace un print de la las películas en orden y a que sesión hay que ver.
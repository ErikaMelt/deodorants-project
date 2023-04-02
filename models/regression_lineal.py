import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import time

# Cargar datos
df = pd.read_csv("../data/deodorants_model.csv")

# Seleccionar columnas para predecir las ventas
cols = [
    'precio_unitario', 'stock_unidades', 'mov_year', 'punto_dist', 'zona',
    'id_cadena', 'cd_abast', 'mov_weekday', 'is_weekend',
    'mov_month', 'longitud', 'nro_prom', 'latitud',
    'id_region', 'local', 'idb', 'id_producto',
    'duracion_promo', 'tiene_promo'
]

X = df[cols]
y = df["venta_unidades"]

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print('Entrenamiento iniciado...')
start_time = time.time()
# Crear un objeto de regresión lineal y ajustar el modelo en el conjunto de entrenamiento
model = LinearRegression()
model.fit(X_train, y_train)
print(f"Tiempo de entrenamiento: {time.time() - start_time} segundos")
# Hacer predicciones en el conjunto de prueba
y_pred = model.predict(X_test)

# Calcular coeficiente de determinación (R2)
r2 = r2_score(y_test, y_pred)
print("R2 score:", r2)

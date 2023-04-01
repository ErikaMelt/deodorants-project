import pandas as pd
import pickle
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# Cargar datos
df = pd.read_csv("../data/deodorants_final_merged_v1.csv")

# Seleccionar columnas para predecir las ventas
cols = ["precio_unitario", "stock_unidades", "ventas_estimadas_promo", "duracion_promo",
        "mov_month", "mov_year", "idb",
        "punto_dist", "local", "is_weekend",
        "zona", "tiene_promo", "id_producto"]

# Seleccionar columnas numéricas y categóricas
num_cols = ["precio_unitario", "stock_unidades", "ventas_estimadas_promo", "duracion_promo"]
cat_cols = ["punto_dist", "local", "is_weekend", "zona", "tiene_promo"]

X = df[cols]
y = df["venta_unidades"]

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

num_transformer = Pipeline(steps=[
    ("scaler", StandardScaler())
])

# Transformación de columnas categóricas
cat_transformer = Pipeline(steps=[
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

# Obtener los nombres de las columnas categóricas
cat_cols = X_train.select_dtypes(include=['object']).columns.tolist()

# Definir el preprocesador con OneHotEncoder
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
    ])

# Combinar preprocesamiento y modelo en un pipeline
rf_pipeline = Pipeline(steps=[("preprocessor", preprocessor),
                              ("model", RandomForestRegressor(n_estimators=100, random_state=42))])

# Medir tiempo de entrenamiento
print('Entrenamiento iniciado...')
start_time = time.time()

# Ajustar transformaciones en conjunto de entrenamiento
cat_encoder = OneHotEncoder(handle_unknown='ignore').fit(X_train[cat_cols])
cat_onehot_features = cat_encoder.get_feature_names_out(cat_cols)
feature_names = num_cols + cat_onehot_features.tolist()

# Ajustar transformaciones en conjunto de entrenamiento
preprocessor.fit(X_train)
X_train_transformed = preprocessor.transform(X_train)

# Crear el dataframe transformado
X_train_transformed_df = pd.DataFrame(X_train_transformed, columns=feature_names)
print(X_train_transformed_df)

# Ajustar modelo en conjunto de entrenamiento
rf_pipeline.fit(X_train_transformed_df, y_train)

# Imprimir tiempo de entrenamiento
print(f"Tiempo de entrenamiento: {time.time() - start_time} segundos")

# Guardar modelo en archivo pickle
with open('rf_pipeline.pkl', 'wb') as file:
    pickle.dump(rf_pipeline, file)

# Hacer predicciones en conjunto de prueba
X_test_transformed = preprocessor.transform(X_test)
X_test_transformed_df = pd.DataFrame(X_test_transformed, columns=feature_names)
y_pred = rf_pipeline.predict(X_test_transformed_df)

# Calcular coeficiente de determinación (R2)
r2 = r2_score(y_test, y_pred)
print("R2 score:", r2)


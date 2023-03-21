from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import folium

# Load the data into a pandas DataFrame
#df = pd.read_csv('../clean_data/deodorants_final_merged.csv')

try:
    df = pd.read_csv('../clean_data/deodorants_final_merged.csv', engine='python')
except pd.errors.ParserError as e:
    print(f"An error occurred while parsing the file: {e}")

features = ['id_producto', 'latitud', 'longitud', 'tiene_promo', 'idb', 'venta_unidades']
# identifier = 'idb'

# Create a new DataFrame with the features as columns and the identifier as the index
# data = df.set_index(identifier)[features]
data = df[features]

# Normalize the data (optional)
scaler = StandardScaler()
data = scaler.fit_transform(data)

dbscan = DBSCAN(eps=0.5, min_samples=5)
# Fit the model: Fit the model to your data to identify the clusters.
clusters = dbscan.fit_predict(data)

# Analyze the results
n_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
print("Number of clusters:", n_clusters)

# Print the indices of each cluster
for i in range(n_clusters):
    print("Indices of points in cluster", i, ":")
    print(np.where(clusters == i)[0])

# Print the indices of points in the noise cluster
print("Indices of points in noise cluster:")
print(np.where(clusters == -1)[0])

# Create a map centered on the first data point
map_center = [df['latitud'][0], df['longitud'][0]]
m = folium.Map(location=map_center, zoom_start=12)

# Add markers for each data point, colored by their cluster label
for i in range(len(df)):
    cluster_label = dbscan.labels_[i]
    lat = df['latitud'][i]
    lng = df['longitud'][i]
    marker = folium.Marker(location=[lat, lng],
                           icon=folium.Icon(color='blue' if cluster_label == -1 else 'red'))
    marker.add_to(m)

# Display the map
m

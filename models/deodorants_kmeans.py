import pandas as pd
import folium
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Load the data into a pandas DataFrame
try:
    data = pd.read_csv('../clean_data/deodorants_final_merged.csv', engine='python')
except pd.errors.ParserError as e:
    print(f"An error occurred while parsing the file: {e}")

# Extract the relevant features for clustering
features = ['id_producto', 'latitud', 'longitud', 'tiene_promo', 'idb', 'venta_unidades']
X = data[features].values

# Normalize the features to have zero mean and unit variance
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Specify the number of clusters
k = 5

# Perform k-means clustering
kmeans = KMeans(n_clusters=k, random_state=0).fit(X)

# Get the cluster labels and add them to the DataFrame
labels = kmeans.labels_
data['cluster'] = labels


# Calculate inertia for a range of cluster numbers
inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=0).fit(X)
    inertias.append(kmeans.inertia_)

# Plot the elbow curve
plt.plot(range(1, 11), inertias)
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.title('Elbow method for KMeans clustering')
plt.show()



#
# # Create a map centered on the first data point
# m = folium.Map(location=[data['latitud'].iloc[0], data['longitud'].iloc[0]], zoom_start=10)
#
# # Add a marker for each data point, color-coded by cluster
# for i, row in data.iterrows():
#     folium.Marker(location=[row['latitud'], row['longitud']], popup=f"Cluster: {row['cluster']}", icon=folium.Icon(color=f"#{labels[i]*256//k:02x}")).add_to(m)
#
# # Display the map
# m

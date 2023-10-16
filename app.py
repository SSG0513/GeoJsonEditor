from flask import Flask, render_template, request, send_file
import geopandas as gpd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Get the uploaded file
    file = request.files['file']
    # Get the column name to be changed
    old_col_name = request.form['old_col_name']
    # Get the new column name
    new_col_name = request.form['new_col_name']
    # Get the new data type for the column
    new_data_type = request.form['new_data_type']

    # Read the GeoJSON file using GeoPandas
    gdf = gpd.read_file(file)

    # Rename the column
    gdf = gdf.rename(columns={old_col_name: new_col_name})

    # Change the data type of the column
    gdf[new_col_name] = gdf[new_col_name].astype(new_data_type)

    # Save the updated GeoJSON file to a temporary directory
    temp_dir = 'temp'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    temp_file_path = os.path.abspath(os.path.join(temp_dir, 'updated_file.geojson'))
    gdf.to_file(temp_file_path, driver='GeoJSON')

    # Allow the user to download the updated file
    return send_file(temp_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

    
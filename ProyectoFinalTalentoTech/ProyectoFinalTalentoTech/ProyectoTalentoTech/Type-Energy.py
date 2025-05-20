import csv
from flask import Flask, render_template, jsonify, request
import matplotlib
import matplotlib.pyplot as plt 
import io 
import pandas as pd
import os
import base64

# Set matplotlib to use a non-GUI backend (useful for server environments)
matplotlib.use('agg')

# Initialize Flask app
app = Flask(__name__)

# Dictionary mapping energy types to their respective CSV file paths
data_paths = {
    'wind': r'C:\Users\01030\OneDrive\Desktop\ProyectoFinalTalentoTech\ProyectoFinalTalentoTech\ProyectoTalentoTech\data\08 wind-generation.csv',
    'solar': r'C:\Users\01030\OneDrive\Desktop\ProyectoFinalTalentoTech\ProyectoFinalTalentoTech\ProyectoTalentoTech\data\12 solar-energy-consumption.csv'
    # 'hydrogen': r'data/03 green-hydrogen.csv'  # Placeholder path for green hydrogen if data is added later
}

# Filter out non-country entities based on specific keywords
def is_strictly_country(name):
    excluded_keywords = [
        'World', 'OECD', 'G20', 'EU', 'Ember', 'Africa', 'Asia', 'America',
        'income', 'Europe', 'Union', 'International', 'BP'
    ]
    return not any(term in name for term in excluded_keywords)

# Load CSV data based on selected energy type
def load_energy_data(energy_type):
    path = data_paths.get(energy_type)
    if path is None or not os.path.exists(path):
        return None
    return pd.read_csv(path)

# Preprocess the data: filter, aggregate, and select top countries including Colombia
def preprocess_data(df, energy_type):
    if energy_type == 'wind':
        column = "Electricity from wind (TWh)"
    elif energy_type == 'solar':
        column = "Electricity from solar (TWh)"
    # elif energy_type == 'hydrogen':
        # column = "Hydrogen production (TWh)"  # Adjust if actual column name differs
    else:
        raise ValueError("Unsupported energy type")

    # Group by country and sum the energy values
    total_by_country = (
        df.groupby("Entity")[column].sum().reset_index()
    )
    # Filter to include only actual countries
    total_by_country = total_by_country[total_by_country["Entity"].apply(is_strictly_country)]
    # Get the top 4 countries by energy production
    top_countries = total_by_country.sort_values(by=column, ascending=False).head(4)

    # Ensure Colombia is included even if not in top 4
    colombia_row = total_by_country[total_by_country["Entity"] == 'Colombia']
    if not colombia_row.empty and 'Colombia' not in top_countries["Entity"].values:
        top_countries = pd.concat([top_countries, colombia_row], ignore_index=True)

    return top_countries.drop_duplicates(subset="Entity").reset_index(drop=True), column

# Generate a chart (line, bar, pie, or scatter) and return it as a base64-encoded PNG
def create_chart(data, column, chart_type='line'):
    plt.clf()  # Clear previous plots
    countries = data["Entity"]
    values = data[column]

    # Generate chart based on selected type
    if chart_type == 'line':
        plt.plot(countries, values, marker='o', linestyle='-', color='blue', label='Line Chart')
        plt.title(f"{column} - Line Chart")
        plt.xlabel("Countries")
        plt.ylabel(column)
        plt.legend()
    elif chart_type == 'bar':
        plt.bar(countries, values, color='green')
        plt.title(f"{column} - Bar Chart")
        plt.xlabel("Countries")
        plt.ylabel(column)
    elif chart_type == 'pie':
        plt.pie(values, labels=countries, autopct='%1.1f%%', startangle=140)
        plt.title(f"{column} - Pie Chart")
    elif chart_type == 'scatter':
        plt.scatter(countries, values, color='red', label='Scatter Plot')
        plt.title(f"{column} - Scatter Plot")
        plt.xlabel("Countries")
        plt.ylabel(column)
        plt.legend()

    # Save plot to a byte buffer
    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode image to base64 so it can be sent via JSON
    encoded_img = base64.b64encode(img.getvalue()).decode('utf-8')
    img.close()
    return encoded_img

# API endpoint to generate and return a chart image based on energy type
@app.route('/get_chart/<energy_type>')
def get_chart(energy_type):
    chart_type = request.args.get('type', 'bar')
    df = load_energy_data(energy_type)
    if df is None:
        return jsonify({'error': f'Data for {energy_type} not found'})

    try:
        top_data, column = preprocess_data(df, energy_type)
        chart_img = create_chart(top_data, column, chart_type)
        return jsonify({'image': f'data:image/png;base64,{chart_img}'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Route for the main page
@app.route('/')
def index():
    return render_template('Page1-Main.html')

# Route for wind energy visualization page
@app.route('/wind')
def wind_page():
    return render_template('Page2-WindEnergy.html')

# Route for solar energy visualization page
@app.route('/solar')
def solar_page():
    return render_template('Page3-SolarEnergy.html')

# Route for green hydrogen visualization page
@app.route('/hydrogen')
def hydrogen_page():
    return render_template('Page4-GreenHydrogen.html')

# Endpoint to receive and save form data to a CSV file
@app.route("/save_data", methods=["POST"])
def save_data():
    # Get form data from the request
    previous_reading = request.form.get("previous_reading")
    current_reading = request.form.get("current_reading")
    total_consumption = request.form.get("total_consumption")

    # Ensure the 'data' folder exists; create it if it doesn't
    os.makedirs("data", exist_ok=True)

    # Save the form data to a CSV file using a relative path
    with open("data/form_data.csv", "a", encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([previous_reading, current_reading, total_consumption])
    
    # Render the main page after saving the data
    return render_template("Page1-Main.html")

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

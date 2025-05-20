https://github.com/steven010302/green_revolution.git

# 🌍 Energy Type Visualization Web App

This Flask-based web application allows users to visualize data related to different types of renewable energy—currently wind and solar energy. The app displays charts (bar, pie, line, scatter) showing the top energy-producing countries, ensuring Colombia is always included for reference.

## 📌 Features

- 🔍 Filtered data to include only countries (excludes regions, economic groups, etc.)
- 📊 Visualizations in bar, line, pie, and scatter formats
- 📁 Individual pages for Wind, Solar, and Green Hydrogen energy types
- 🇨🇴 Colombia is always displayed regardless of ranking
- 📝 Save user-submitted form data to a CSV file

## 🚀 Technologies Used

- Python 🐍  
- Flask 🌶  
- Pandas 🐼  
- Matplotlib 📈  
- HTML/CSS 🖥  
- JavaScript (optional for front-end enhancement)

## 📂 Project Structure

project/
│
├── app.py / Type-Energy.py # Main Flask application
├── templates/
│ ├── Page1-Main.html # Main home page
│ ├── Page2-WindEnergy.html # Wind energy visualization
│ ├── Page3-SolarEnergy.html # Solar energy visualization
│ ├── Page4-GreenHydrogen.html # Green hydrogen placeholder page
├── data/
│ ├── 08 wind-generation.csv
│ ├── 12 solar-energy-consumption.csv
│ ├── form_data.csv # Stores form input from users


## 📈 How It Works

1. The app loads CSV files corresponding to each energy type.
2. It processes the data to extract the top 4 producing countries and includes Colombia.
3. The user selects the energy type and chart style.
4. A base64-encoded image of the selected chart is generated and displayed via the frontend.

## 🛠 Running Locally

1. Clone this repository:
   
       git clone https://github.com/yourusername/energy-type-visualization.git

       cd energy-type-visualization

3. (Optional) Create and activate a virtual environment:

       python -m venv venv
       source venv/bin/activate  # On Windows: venv\Scripts\activate

4. Install dependencies:

       pip install flask pandas matplotlib

5. Run the application:

       python Type-Energy.py

6. Open your browser and navigate to http://127.0.0.1:5000/

📤 Endpoints
/ — Main homepage

  /wind — Wind energy visualization

  /solar — Solar energy visualization

    /hydrogen — Green hydrogen placeholder page

    /get_chart/<energy_type>?type=<chart_type> — Returns base64 chart image (types: bar, line, pie, scatter)

    /save_data — Receives form data and stores it in a CSV file

🔒 Notes

  Make sure the data folder exists and contains the correct CSV files.

  Matplotlib is configured to use a non-GUI backend (agg) for compatibility with server environments.

📬 Contact

  Created by Steven peña
  📧 is.pena01@ciaf.edu.co

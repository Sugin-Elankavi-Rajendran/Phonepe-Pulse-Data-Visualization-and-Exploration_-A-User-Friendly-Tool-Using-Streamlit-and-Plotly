# PhonePe Data Processing and Visualization

This repository contains a set of Python scripts that perform data processing and visualization tasks related to PhonePe's transaction and user data. The scripts extract information from JSON files, load the data into Pandas DataFrames, and then store the data in a MySQL database. Additionally, the repository includes a Streamlit web application for interactive data exploration and visualization.

## Contents

- `data_cloning_and_processing.py`: The main script that performs the data processing tasks.
- `Phonepe.py`: The Streamlit web application for interactive data visualization.
- `path.py`: A module containing paths to various data directories.
- `logo.png`: The logo image used in the Streamlit app.
- `geo_data.json`: GeoJSON data for mapping.
- `requirements.txt`: List of required Python packages.

## Setup

1. Clone the repository to your local machine.
2. Install the required Python packages using the following command:
   ```bash
   pip install -r requirements.txt
   ```
3. Make sure you have MySQL installed and running. Update the MySQL database connection parameters in `data_cloning_and_processing.py` and `Phonepe.py` as needed.

## Usage

### Data Processing (data_cloning_and_processing.py)

1. Run the `data_cloning_and_processing.py` script to process the PhonePe data and populate the MySQL database.
   ```bash
   data_cloning_and_processing.py
   ```

### Data Visualization (Phonepe.py)

1. Run the Streamlit app to visualize the processed data.
   ```bash
   streamlit run Phonepe.py
   ```
2. Use the interactive options in the app to explore transaction and user data.

## Streamlit App

The Streamlit web application provides various interactive visualizations of PhonePe's transaction and user data. You can select different options to visualize data across different years, quarters, states, and transaction types.

## Data Sources

The raw data for this project is expected to be stored in JSON files. These JSON files are processed to extract relevant information and create visualizations.


Please make sure to update the paths, database credentials, and other settings as needed to fit your environment before running the scripts and the Streamlit app.

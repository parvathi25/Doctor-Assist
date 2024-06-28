from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services', methods=['GET', 'POST'])
def services():
    if request.method == 'POST':
        # Check if the files are uploaded correctly
        if 'ecg_file' not in request.files:
            return render_template('services.html', error="No ECG file uploaded")
        if 'ppg_file' not in request.files:
            return render_template('services.html', error="No PPG file uploaded")
        if 'pcg_file' not in request.files:
            return render_template('services.html', error="No PCG file uploaded")

        try:
            # Read the uploaded CSV files
            ecg_file = request.files['ecg_file']
            ppg_file = request.files['ppg_file']
            pcg_file = request.files['pcg_file']
            
            print("ECG file:", ecg_file.filename)
            print("PPG file:", ppg_file.filename)
            print("PCG file:", pcg_file.filename)
            
            ecg_data = pd.read_csv(ecg_file)
            ppg_data = pd.read_csv(ppg_file)
            pcg_data = pd.read_csv(pcg_file)
            
            print("ECG data shape:", ecg_data.shape)
            print("PPG data shape:", ppg_data.shape)
            print("PCG data shape:", pcg_data.shape)
            
            # Process the data and detect arrhythmia
            x = ecg_data.iloc[1200:20000, 0]  # Assuming the first column contains the ECG data
            n = len(x)
            time = np.arange(0, n, 1)
            plt.plot(time, x)

            m = np.max(x)
            threshold = m * 0.7
            R = [0] * n
            for i in range(1, n-1):
                if x.iloc[i] > threshold:
                    if x.iloc[i] > x.iloc[i+1] and x.iloc[i] > x.iloc[i-1]:
                        R[i] = i
            R = [i for i in R if i != 0]

            interval = np.diff(R, n=1, axis=0)
            meaninterval = np.mean(interval)
            heartrate = 60 * 1000 / meaninterval
            if heartrate > 100:
                arrhythmia = "tachycardia"
            elif heartrate < 60:
                arrhythmia = "bradycardia"
            else:
                arrhythmia = "normal"
            
            # Render the results page with detected arrhythmia
            return render_template('results.html', arrhythmia=arrhythmia, heart=heartrate)

        except Exception as e:
            return render_template('services.html', error=f"Error processing data: {str(e)}")

    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
# Importing Dependencies
from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import joblib

# Starting Flask App
app = Flask(__name__)

# Standard Scaler
sc = joblib.load('./sc.joblib')

# Random Forest Model
modelRF = joblib.load("./RFModelDiseasePredictr.joblib")

# Reading in Testing.csv
df = pd.read_csv('Resources/Testing.csv', error_bad_lines= False)

# Cleaned DF by removing underscores from columns
cleanedDF = df.rename(columns=lambda name: name.replace('_', ' '))

# Identifying Features (symptoms) and dropping 'Prognosis' column
x_test = cleanedDF.iloc[:, 0:-1]

# Setting App routes
@app.route('/')
def home():
    return render_template('index.html')

# POST Request to send data to Flask API and update with 'request.form.values'
@app.route('/predict',methods=['POST'])
def predict():
    if request.method=='POST':
        symptoms=x_test.columns
        userInput = [str(x) for x in request.form.values()]
        
        # b = created list with 132 elements ex. [0,0,0,0,0]
        b=[0]*132
        for x in range(0,132):
            for y in userInput:
                if(symptoms[x]==y):
                    b[x]=1
        b=np.array(b)
        b=b.reshape(1,132)
        prediction = modelRF.predict(b)
        prediction=prediction[0]
    return render_template('index.html', 
    endPrediction="The chosen symptoms suggests it could be {}".format(prediction))


if __name__ == "__main__":
    app.run(debug=True)
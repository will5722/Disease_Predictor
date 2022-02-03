# Importing Dependencies
from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import joblib
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Starting Flask App
app = Flask(__name__)

# Standard Scaler
#sc = joblib.load('./nn.joblib')

# Random Forest Model
modelNN = load_model("NNModel.h5")
#ohe = OneHotEncoder(sparse=False)
# Reading in Testing.csv
df = pd.read_csv('Resources/Testing.csv', error_bad_lines= False)

# Identifying Features (symptoms) and dropping 'Prognosis' column
x_test = df.iloc[:, 0:-1]
y = pd.get_dummies(df, columns=['prognosis'], drop_first=True)
diseases = df['prognosis']
disDict = {}
for i, disease in enumerate(diseases):
    disDict[disease] = i

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
        #y=ohe.inverse_transform(y).ravel()
        prediction = modelNN.predict(b)
        #prediction=prediction[0]
        prediction = np.argmax(prediction)
        key_list = list(disDict)
        prediction = key_list[prediction]
    return render_template('index.html', endPrediction="The chosen symptoms suggests it could be {}".format(prediction))


if __name__ == "__main__":
    app.run(debug=True)
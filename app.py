from flask import Flask, render_template, url_for, request, jsonify
import pickle
import numpy as np
import pandas as pd
import os
import joblib


app = Flask(__name__)


sc = joblib.load('./sc.joblib')

modelRF = joblib.load("./RFModelDiseasePredictr.joblib")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods =['POST'])
def predict():
    print('hello')
    x = np.array(request.json).reshape(1, -1)
    print(x)
    x = sc.transform(x)
    print(x)
    prediction = modelRF.predict(x)[0]
    prediction = str(prediction)

    print(prediction)
    return jsonify({
        "data": prediction
        })

    



    # whatSymptoms = np.zeros(len(symptomsDict))
    # trueSymp = []
    # symptoms = request.args.get('symptoms')
    # #symptoms = symptoms.split(',')

    # for symptom in symptoms:
    #     trueSymp.append(symptomsDict[symptom])
    
    # whatSymptoms[trueSymp] = 1


    # return jsonify({"data": modelRF.predict([input_vector])[0]})
    
    # features = [str(x) for x in request.form.values()]
    # sympFeatures = [np.array(features)]
    # print(features)
    # prediction = modelRF.predict(sympFeatures)
    # print(prediction)

    # output = '{0:.{1}f}'.format(prediction[0][1], 2)

    # return render_template('index.html', prediction_text ='Your prescreen diagnosis is $ {}'.format(output))

if __name__ == "__main__":
    app.run(debug=True, port=5002)

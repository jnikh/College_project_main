from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sigup.db'
#Intialize the database 
db=SQLAlchemy(app)

#Create db model
class Signup(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable=False)
    email_id=db.Column(db.String(500),nullable=False)
    number=db.Column(db.Integer, nullable=False)
    gender=db.Column(db.String(100))
    address=db.Column(db.String(500))
    #create a function to return a string
    def _repr_(self):
        return '<Name %r>' % self.id
    

# instantiate object

#loading the different saved model for different disease
diabetes_predict=pickle.load(open('diabetes.pkl', 'rb'))
heart_predict=pickle.load(open('heart.pkl', 'rb'))
parkinsons_predict=pickle.load(open('parkinsons.pkl', 'rb'))

@app.route('/') # instancing one page (homepage)
def home():
    return render_template("home.html")
# ^^ open home.html, then see that it extends layout.
# render home page.

@app.route('/diabetes') # instancing child page
def diabetes():
    return render_template("diabetes.html")


@app.route('/parkinsons/') # instancing child page
def parkinsons():
    return render_template("parkinsons.html") 

@app.route('/heartdisease/') # instancing child page
def heartdisease():
    return render_template("heartdisease.html")

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    return render_template("sign_in.html")
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    return render_template("signin.php")
    pass



@app.route('/predictdiabetes/',methods=['POST']) 
def predictdiabetes():      #function to predict diabetes
    int_features=[x for x in request.form.values()]
    processed_feature_diabetes=[np.array(int_features,dtype=float)]
    prediction=diabetes_predict.predict(processed_feature_diabetes)
    if prediction[0]==1:
        display_text="This person has Diabetes"
    else:
        display_text="This person doesn't have Diabetes"
    return render_template('diabetes.html',output_text="Result: {}".format(display_text))

@app.route('/predictparkinson/',methods=['POST']) 
def predictparkinsons():      #function to predict parkinsons disease
    int_features=[x for x in request.form.values()]
    processed_feature_parkinsons=[np.array(int_features,dtype=float)]
    prediction=parkinsons_predict.predict(processed_feature_parkinsons)
    if prediction[0]==1:
        display_text="This person has Parkinson's"
    else:
        display_text="This person doesn't have Parkinson's"
    return render_template('parkinsons.html',output_text="Result: {}".format(display_text))

@app.route('/predictheartdisease/',methods=['POST']) 
def predictheartdisease():      #function to predict heart disease
    int_features=[x for x in request.form.values()]
    processed_feature_heart=[np.array(int_features,dtype=float)]
    prediction=heart_predict.predict(processed_feature_heart)
    if prediction[0]==1: 
        display_text="This person has Heart Disease"
    else:
        display_text="This person doesn't have Heart Disease"
    return render_template('heartdisease.html',output_text="Result: {}".format(display_text))


if __name__=="__main__":
    app.run(debug=True)
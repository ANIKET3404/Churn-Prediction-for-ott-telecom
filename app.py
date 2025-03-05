from flask import Flask, redirect, render_template, request, url_for,session,make_response
# import jsonify
import requests
import pickle
import mysql.connector
import numpy as np
import sklearn
import matplotlib
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
app.secret_key = 'mysecretkey'
db = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="ajinkya722",
    database="churn_prediction"
)
model1 = pickle.load(open('Customer_Churn_Prediction.pkl', 'rb'))
model2 = pickle.load(open('OTT_dataset.pkl', 'rb'))
@app.route('/', methods=['GET'])
def Home():
    # session.pop('user_id')
    return render_template('startpage.html')

@app.route('/prevention', methods=['GET'])
def prevention():
    # session.pop('user_id')
    return render_template('prevention.html')




@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['name']
            password = request.form['psw']
            email=request.form['email']
            number=request.form['number']
            print(username)
            cursor = db.cursor()
            cursor.execute('INSERT INTO user_table (Name, contact_no,email,password) VALUES (%s,%s,%s,%s)', (username,number,email,password))
            db.commit()
            return render_template('register.html',ans='User Created Sucesfully!!')
        except mysql.connector.Error as err:
            return render_template('register.html',ans=err)
    else:
        return render_template('register.html')
    
@app.after_request
def add_header(response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response


    
@app.route('/logout',methods=['GET'])
def logout():
    print('out')
    session.pop('user_id', None)
    # Redirect to login page
    return redirect('/')
        

@app.route('/telcomhistory',methods=['GET'])
def telcomhistory():
    try:
        user=session['user_id']
        # print(user)
        query="select * from telcom where user_id=%s"
        cursor=db.cursor()
            
        cursor.execute(query,(user,))
        print(user)
        data = cursor.fetchall()
        print(data)
        if(data):
            return render_template('telcom_history.html',data=data)
        else:
            return render_template('telcom_history.html',not_found='No data Found')
    except mysql.connector.Error as err:
        return f"An error occurred: {err}"

@app.route('/login',methods=['GET','POST'])
def login():
    if 'user_id' in session:
        return redirect('/')
    else:
        if request.method == 'POST':
            try:
                username = request.form['username']
                password = request.form['password']
                cursor = db.cursor()
                cursor.execute('SELECT * FROM user_table WHERE email = %s AND password = %s', (username, password))
                user = cursor.fetchone()
                if user:
                    session['user_id'] = user[4]
                    # session.permanent = False
                    print(session['user_id'])
                    return redirect('/')
                else:
                    return render_template('login.html',ans='Invalid username or password')
            except mysql.connector.Error as err:
                return f"An error occurred: {err}"
        else:
            return render_template('login.html')

# @app.route('/predict',methods=['GET'])
# def predict():
#     return render_template('telcom.html')

standard_to = StandardScaler()
@app.route('/telcom',methods=['POST','GET'])
def telcom(): 
    if 'user_id' in session:
        if request.method == 'POST':
            try:
                userId=session['user_id']
                MonthlyCharge = float(request.form['MonthlyCharge'])
                # Age = int(request.form['Age'])
                Tenure = int(request.form['Tenure'])
                # Balance = float(request.form['Balance'])
                # Age=int(request.form['Age'])
                Online_backup=request.form['Online_Backup']
                Active_member = request.form['Active_Member']
                Phone_service = request.form['Phone_Service']
                Streaming_Service = request.form['Streaming_service']
                Online_Security = request.form['Online_Security']
                Internet_Service=request.form['Internet_Service']
                Tech_Support=request.form['Tech_Support']
                Payment_method=request.form['Payment_Method']
                Gender = request.form['Gender_Male']
                query=('INSERT INTO telcom (MonthlyCharge,Tenure,Active_member,Streaming_service,Online_security,Online_backup,Internet_service,Tech_support,Payment_method,Gender,user_id,churn) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
                
                if(Phone_service == 'Yes'):
                    Phone_service_Yes = 1
                    Phone_service_No= 0
                    Phone_service_No_Internet = 0
                elif(Phone_service == 'No'):
                    Phone_service_Yes = 0
                    Phone_service_No= 1
                    Phone_service_No_Internet = 0
                else:
                    Phone_service_Yes = 0
                    Phone_service_No= 0
                    Phone_service_No_Internet = 1

                if(Online_Security == 'Yes'):
                    Online_Security_Yes = 1
                    Online_Security_No= 0
                    Online_Security_No_Internet = 0
                        
                elif(Online_Security == 'No'):
                    Online_Security_Yes = 0
                    Online_Security_No= 1
                    Online_Security_No_Internet = 0
                
                else:
                    Online_Security_Yes = 0
                    Online_Security_No= 0
                    Online_Security_No_Internet = 1
                    
                if(Internet_Service == 'DSL'):
                    Internet_Service_Dsl = 1
                    Internet_Service_Fiberoptic= 0
                    Internet_Service_No = 0
                        
                elif(Internet_Service == 'Fiberoptic'):
                    Internet_Service_Dsl = 0
                    Internet_Service_Fiberoptic= 1
                    Internet_Service_No = 0
                
                else:
                    Internet_Service_Dsl = 0
                    Internet_Service_Fiberoptic= 0
                    Internet_Service_No = 1

                if(Streaming_Service == 'No internet'):
                    Streaming_Service_No_Internet = 1
                    Streaming_Service_yes= 0
                else:
                    Streaming_Service_No_Internet = 0
                    Streaming_Service_yes= 1
                        
                if(Online_backup=='Yes'):
                    Online_backup_Yes=1
                else:
                    Online_backup_Yes=0
                if(Tech_Support == 'Yes'):
                    Tech_Support_Yes = 1
                    Tech_Support_No= 0
                    Tech_Support_No_Internet = 0
                        
                elif(Online_Security == 'No'):
                    Tech_Support_Yes = 0
                    Tech_Support_No= 1
                    Tech_Support_No_Internet = 0
                
                else:
                    Tech_Support_Yes = 0
                    Tech_Support_No= 0
                    Tech_Support_No_Internet = 1
                
                if(Payment_method == 'Credit Card'):
                    Payment_Method_Credit_card=1
                    Payment_Method_Electronic_check=0
                    Payment_Method_Mailed_check=0
                        
                elif(Payment_method == 'Electronic Check'):
                    Payment_Method_Credit_card=0
                    Payment_Method_Electronic_check=1
                    Payment_Method_Mailed_check=0
                else:
                    Payment_Method_Credit_card=0
                    Payment_Method_Electronic_check=0
                    Payment_Method_Mailed_check=1
                
                

                # print(Online_Security)
                if(Gender == 'Male'):
                    Gender_Male = 1
                   
                else:
                    Gender_Male = 0

                prediction = model1.predict([[Tenure,MonthlyCharge,Gender_Male,Phone_service_Yes,Internet_Service_Fiberoptic,Internet_Service_No,Online_Security_No_Internet,Online_Security_Yes,Online_backup_Yes,Tech_Support_No_Internet,Tech_Support_Yes,Streaming_Service_No_Internet,Streaming_Service_yes,Payment_Method_Credit_card,Payment_Method_Electronic_check,Payment_Method_Mailed_check]])
                if prediction==1.0:
                    text='Yes'
                else:
                    text='No'
                cursor = db.cursor()
                cursor.execute(query,(MonthlyCharge,Tenure,Active_member,Streaming_Service,Online_Security,Online_backup,Internet_Service,Tech_Support,Payment_method,Gender,userId,text))
                db.commit()

                return render_template('telcom.html',prediction_text="The Customer will Churn="+text)
            except mysql.connector.Error as err:
                return f"An error occurred: {err}"
        
        else:
            return render_template('telcom.html')
    else:
        return redirect('/login')
    
@app.route('/otthistory',methods=['GET'])
def otthistory():
        try:
            user=session['user_id']
            # print(user)
            query="select * from ott where user_id=%s"
            cursor=db.cursor()
            
            cursor.execute(query,(user,))
            print(user)
            data = cursor.fetchall()
            print(data)
            if(data):
                return render_template('ott_history.html',data=data)
            else:
                return render_template('ott_history.html',not_found='No data Found')
        except mysql.connector.Error as err:
            return f"An error occurred: {err}"
        

@app.route('/ott',methods=['GET','POST'])
def ott():
    if 'user_id' in session:
        if request.method == 'POST':
            try:
                userId=session['user_id']
                Age=int(request.form['Age'])
                No_of_Days_Subscribed=int(request.form['No_of_Days_Subscribed'])
                Weekly_Mins_Watched = int(request.form['Weekly_Mins_Watched'])
                Minimum_Daily_Mins = int(request.form['Minimum_Daily_Mins'])
                Maximum_Daily_Mins = int(request.form['Maximum_Daily_Mins'])
                weekly_max_night_mins = int(request.form['weekly_max_night_mins'])
                Videos_Watched=int(request.form['Videos_Watched'])
                Maximum_Days_Inactive=int(request.form['Maximum_Days_Inactive'])
                Multi_Screen=request.form['Multi_Screen']
                mail_subscribed = request.form['mail_subscribed_yes']
                Gender = request.form['Gender_Male']
                Customer_Support_Calls= int(request.form['Customer_Support_Calls'])
                query=('INSERT INTO ott (age,NoOfDaysSub,WeekelyMinsWatched,MinimumDailyMins,MaximumDailyMins,WeeklyMaxNightMins,VideosWatched,MaximumDaysInactive,MultiScreen,MailSubscribed,user_id,churn) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
                
                if (Multi_Screen=="Yes"):
                    Multi_Screen_Yes=1
    
                else:
                    Multi_Screen_Yes=0
                    

                if (mail_subscribed=="Yes"):
                    mail_subscribed_Yes=1
                else:
                    mail_subscribed_Yes=0

                if(Gender == 'Male'):
                    Gender_Male = 1
                   
                else:
                    Gender_Male = 0

                prediction = model2.predict([[Age,No_of_Days_Subscribed,Weekly_Mins_Watched,Minimum_Daily_Mins,Maximum_Daily_Mins,weekly_max_night_mins,Videos_Watched,Maximum_Days_Inactive,Customer_Support_Calls,Gender_Male,Multi_Screen_Yes,mail_subscribed_Yes]])
            
                if prediction==1.0:
                    predict='Yes'
                    
                else:
                    predict='No'
                
                cursor = db.cursor()
                cursor.execute(query,(Age, No_of_Days_Subscribed, Weekly_Mins_Watched ,Minimum_Daily_Mins, Maximum_Daily_Mins, weekly_max_night_mins,Videos_Watched, Maximum_Days_Inactive,Multi_Screen,mail_subscribed,userId,predict))
                db.commit()
                return render_template('ott.html',prediction_text="The Customer Will Churn="+predict)
            except mysql.connector.Error as err:
                return f"An error occurred: {err}"
        
        else:
            return render_template('ott.html')
    else:
        return redirect('/login')
    
       
if __name__=="__main__":
    app.run(debug=True)


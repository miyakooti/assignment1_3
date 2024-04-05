from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import boto3
import os
import logging

from aws_credentials import get_session



app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

# AWS認証情報の設定
session = get_session()

# AWSクライアントの作成
s3_client = session.client('s3')
dynamodb_client = session.client("dynamodb")



class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')



@app.route('/', methods=['GET', 'POST'])
def login():

    response = dynamodb_client.list_tables()
    print(response)



    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print(email)
        print(password)

        response = dynamodb_client.get_item(
            TableName="login",
            Key={
                "email": {"S": email},
                "password": {"S": password},
            },
        )

        if response != None:
            print("login success")
            # return redirect(url_for('success'))


        
        # ログイン失敗時にログインページを再表示
        return render_template('login.html', message='email or password is invalid')
    
    # GETリクエストの場合はログインページを表示
    return render_template('login.html', message='')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/') 
def hello_world():
    return '誘導できた!' 



if __name__ == '__main__':
    app.run()
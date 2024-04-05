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

    response = dynamodb_client.get_item(
        TableName="login",
        Key={
            "email": {"S": "S40756889@student.rmit.edu.au"},
            "user_name": {"S": "kosuke arai 9"},
        },
    )

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']


        # DynamoDBからユーザー情報を取得
        response = login_table.get_item(
            Key={
                'email': email
            }
        )
        
        # ユーザーが存在し、パスワードが一致する場合にログイン成功とする
        if 'Item' in response:
            stored_password = response['Item']['password']
            if password == stored_password:
                return redirect(url_for('success'))
        
        # ログイン失敗時にログインページを再表示
        return render_template('login.html', message='Invalid email or password')
    
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
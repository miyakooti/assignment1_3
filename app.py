from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import boto3
import os
import logging



app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

# AWS認証情報の設定
session = boto3.Session(
    aws_access_key_id='ASIAQ3EGVH4JRBUGXUCY',
    aws_secret_access_key='ks2cwzMttFQzG2mLCZLWH6kyIzsQCQTkXDweSMnI',
    aws_session_token='IQoJb3JpZ2luX2VjEHMaCXVzLXdlc3QtMiJGMEQCIFenjpnD4AHcmQ3YQI9SCo7wIPhJbF5LgrGDNTRrhkHRAiBYTaJWA5ZxT3UUlkH+6a6Wd7lrefwwZ65WUAsfEOKzZCq/Agic//////////8BEAAaDDA1ODI2NDQ2OTI2NyIM9hk+VOGkCBQHCHyVKpMCXjnDx9M8pin7LoIiq9GqCKxhDEeP7rLdosGvnSrJh1ZVLQCyGhiYqWNWs5xFkcty7sMXrxoyYT6jrEtfF80Q/WghoTdz0SZWbMKvnSiWcNjfOPaq+49rBOr56RhbUtkgigj+/7Pho6H2PJNpcrqgXmmOjm0Z4pn1IFFsxt7n3BKvNNrJxVxSSu7D7Jb404y+U42ZSuLp6pNFP0z9TjOEtJPpVci9crugb0gt4hYG8Sf/VmXWBTLHZOKC2ncQXYapZRbhTzfsoN3lBX9H3EHuYjMG06Z9c4BEBcQ06PqNoBXFY46r/f3jFklocXtoXY3BkIJZil+mvlf9WaMY7hDWO+dJv1i0ApQrPN5+/22idPIO5dowv829sAY6ngHY4WdMI5k28A4yWwy4fWBM+1ikhdMLyPFMvxG4bd0GstbDyMixh6QUziT+TaC6VAPLvMCyHy/Oxoi5kk+5n7wUiVIJcZ5VmP+kgLqQVq5VPweiaEVwtFaJPoysUfLo3LFYzl+8+rq0Y2kGx7T0lGzPWVd36FKgdumjEpcFv8ZEh3+NU5sGdQYuJ/sGCSdNxe7o+qoKwtYGIS1/9W4N8g==',  # オプション（一般的には必要ありません）
    region_name='us-east-1'
)

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
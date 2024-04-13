from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required
from flask_login import LoginManager
from flask_login import current_user

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import boto3
import os
import logging
import json

from aws_credentials import get_session
from flask_login import UserMixin

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

login_manager = LoginManager(app)
login_manager.init_app(app)

session = get_session()

s3_client = session.client('s3')
dynamodb_client = session.client("dynamodb")

@app.route('/', methods=['GET', 'POST'])
def login():

    response = dynamodb_client.list_tables()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        response = dynamodb_client.get_item(
            TableName="login",
            Key={
                "email": {"S": email},
            },
        )

        user_name = response.get('Item', {}).get('user_name', {}).get('S')

        if response != None:
            print("login success")
            user = User(email)
            login_user(user)
            session_email = email
            session_user_name = user_name
            return redirect(url_for("home"))

        # fails
        return render_template('login.html', message='email or password is invalid')
    
    return render_template('login.html', message='')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        email = request.form['email']
        user_name = request.form['user_name']
        password = request.form['password']

        response = dynamodb_client.get_item(
            TableName="login",
            Key={
                "email": {"S": email},
            },
        )


        print(response.get("ResponseMetadata"))
        print(response.get("Item"))


        if response.get("Item") != None:
            print(response)
            print("the email is already used")
            return render_template('register.html', message='The email already exists')

        else:
            response = dynamodb_client.put_item(
                TableName="login",
                Item={
                    'email': {'S': email},
                    'user_name': {'S': user_name},
                    'password': {'S': password}
                }
            )
            # login judgement is here
            user = User(email)
            login_user(user)


            return redirect(url_for("login"))

    return render_template('register.html', message='')

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():

    message = ""

    # not good cus we have to scan every time it reloads
    print(current_user.id)
    email = current_user.id

    response = dynamodb_client.scan(
    TableName='login',
    FilterExpression='#email = :email',
    ExpressionAttributeNames={
        '#email': 'email'
    },
    ExpressionAttributeValues={
        ':email': {'S': email}
    }
    )

    item = response.get('Items', [])[0]
    user_name = item.get('user_name', {}).get('S')

    searched_items = []
    if request.method == 'POST':

        title = request.form['title']
        year = request.form['year']
        artist = request.form['artist']

        # preparation of scan
        # i guess we have to create corresponding class which enables us to construct query more easier.
        filter_expression = ""
        expression_attribute_names = {}
        expression_attribute_values = {}

        if title:
            filter_expression += "#title = :title"
            expression_attribute_names["#title"] = "title"
            expression_attribute_values[':title'] = {'S': title}
        if year:
            if filter_expression:
                filter_expression += " and "
            expression_attribute_names["#year"] = "year"
            filter_expression += "#year = :year"
            expression_attribute_values[':year'] = {'N': year}
        if artist:
            if filter_expression:
                filter_expression += " and "
            expression_attribute_names["#artist"] = "artist"
            filter_expression += "#artist = :artist"
            expression_attribute_values[':artist'] = {'S': artist}


        # scan
        print("検索を開始します")
        response = dynamodb_client.scan(
            TableName='music',
            FilterExpression=filter_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
        )

        # retrieve data
        searched_items = response.get('Items', [])

        if searched_items == []:
            message = "No result is retrieved. Please query again"

    # fix here. we can erase here when i brought user info.

    email = current_user.id

    response = dynamodb_client.get_item(
    TableName='login',
    Key={'email': {'S': email}},
    ProjectionExpression='favorite_list'
    )
    favorite_list = response['Item'].get('favorite_list', {'SS': []})['SS']

    # favorite items
    favorite_items = []
    for song_title in favorite_list:
        response = dynamodb_client.query(
            TableName='music',
            KeyConditionExpression='#title = :title',
            ExpressionAttributeNames={'#title': 'title'},
            ExpressionAttributeValues={':title': {'S': song_title}}
        )
        favorite_items.extend(response.get('Items', []))

    response = dynamodb_client.scan(
        TableName="music"
    )

    items = response.get('Items', [])

    return render_template('home.html', favorite_items=favorite_items, searched_items=searched_items, user_name=user_name, message=message)


@app.route('/add_to_favorites', methods=['POST'])
@login_required
def add_to_favorites():

    email = current_user.id
    song_title = request.form.get('song_title')

    print(song_title + "has been pushed")

    # loginテーブルからユーザーのお気に入りリストを取得
    response = dynamodb_client.get_item(
        TableName='login',
        Key={
            'email': {'S': email}
        }
    )

    # お気に入りリストを取得し、楽曲名を追加
    favorite_list = list(response.get('Item', {}).get('favorite_list', {'SS': []})['SS'])
    if song_title not in favorite_list:
        favorite_list.append(song_title)
    print("favorite_list")

    print(favorite_list)

    # 更新されたお気に入りリストをDynamoDBに保存
    dynamodb_client.update_item(
        TableName='login',
        Key={
            'email': {'S': email}
        },
        UpdateExpression='SET favorite_list = :fl',
        ExpressionAttributeValues={
            ':fl': {'SS': favorite_list}
        }
    )

    return redirect(url_for("home"))

@app.route('/delete_from_favorites', methods=['POST'])
@login_required
def delete_from_favorites():

    email = current_user.id
    song_title = request.form.get('song_title')

    # get fav_list from dynamodb
    response = dynamodb_client.get_item(
        TableName='login',
        Key={
            'email': {'S': email}
        }
    )

    favorite_list = list(response.get('Item', {}).get('favorite_list', {'SS': []})['SS'])
    favorite_list.remove(song_title)
    print(favorite_list)

    if favorite_list == []:
        # cus error occurs when i tried to push blank list
        dynamodb_client.update_item(
        TableName='login',
        Key={'email': {'S': email}},
        UpdateExpression='REMOVE favorite_list'
        )

    else:
        # update favorite_list
        dynamodb_client.update_item(
        TableName='login',
        Key={
            'email': {'S': email}
        },
        UpdateExpression='SET favorite_list = :fl',
        ExpressionAttributeValues={
            ':fl': {'SS': favorite_list}
        }
    )

    return redirect(url_for("home"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session_user_name = ""
    session_email = ""
    return redirect(url_for("login"))

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import boto3
import os


app = Flask(__name__)

ACCESS_ID = "ASIAQ3EGVH4JTH6RZZJG"
ACCESS_KEY = "diY3RvliiZQ9D8eIpqjqFHBE2qTvQ/RDpe28wIvA"

app.config['SECRET_KEY'] = os.urandom(24)
# dynamodb = boto3.resource("dynamodb", region_name='us-east-1',
#          aws_access_key_id=ACCESS_ID,
#          aws_secret_access_key= ACCESS_KEY)
dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
login_table = dynamodb.Table("login")


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = login_table.get_item(Key={'email': email})
        if 'Item' in user:
            if user['Item']['email'] == email:
                # ログイン成功
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'danger')
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/') 
def hello_world():
    return '誘導できた!' 



if __name__ == '__main__':
    app.run()
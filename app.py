from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Rjhjdf2007'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)


@app.route('/')
@app.route('/home')
def home():
    return render_template('homepage.html', user=session.get('user'))


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():

    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return "Пользователь уже существует"

        user = User(username=username, password=password, role=role)

        db.session.add(user)
        db.session.commit()

        return redirect('/home')

    return render_template('sign_up.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user'] = username
            return redirect('/home')
        else:
            return "Неверный логин или пароль"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/home')


@app.route('/profile')
def profile():

    if not session.get('user'):
        return redirect('/login')

    user = User.query.filter_by(username=session.get('user')).first()

    return render_template('profile.html', user=user)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
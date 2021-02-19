import json
import requests
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_mongoengine import MongoEngine

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin
from flask_login import login_user, logout_user, current_user, login_required

from create_user import CreateUserForm
from add_workout import AddCardioForm, AddResistanceForm
from login import LoginForm
from edit_workout import EditCardioForm, EditResistanceForm
from config import *

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'workout',
    'host': 'localhost',
    'port': 27017
}
app.config['SECRET_KEY'] = SECRET_KEY

db = MongoEngine()
db.init_app(app)

# login code
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class Users(db.Document, UserMixin):
    name = db.StringField(unique=True)
    password = db.StringField()

    def to_json(self):
        return {"name": self.name,
                "password": self.password}


class Cardio(db.Document, UserMixin):
    user = db.StringField()
    extype = db.StringField()
    name = db.StringField()
    duration = db.IntField()
    intensity = db.IntField()
    date = db.StringField()
    
    def to_json(self):
        return {"user": self.user,
                "extype": self.extype,
                "name": self.name,
                "duration": self.duration,
                "intensity": self.intensity,
                "date": self.date,
                }

class Resistance(db.Document, UserMixin):
    user = db.StringField()
    extype = db.StringField()
    name = db.StringField()
    weight = db.IntField()
    sets = db.IntField()
    repetitions = db.IntField()
    rest = db.IntField()
    date = db.StringField()

    def to_json(self):
        return {"user": self.user,
                "extype": self.extype,
                "name": self.name,
                "weight": self.weight,
                "sets": self.sets,
                "repetitions": self.repetitions,
                "rest": self.rest,
                "date": self.date,}


class News:
    def __init__(self, provider, title, image_url, url, date):
        self.provider = provider
        self.title = title
        self.image_url = image_url
        self.url = url
        self.date = date


def get_news(query, page):

    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/search/NewsSearchAPI"

    querystring = {"q": query, "pageNumber": page, "pageSize": "8", "autoCorrect": "true",
                   "withThumbnails": "true", "fromPublishedDate": "null", "toPublishedDate": "null"}

    headers = {
        'x-rapidapi-key': RAPID_API_KEY,
        'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    results = response.json()['value']

    final = []
    for res in results:
        provider = res['provider']['name']
        title = res['title']
        image_url = res['image']['thumbnail']
        url = res['url']
        date = res['datePublished'].split('T')[0]

        final.append(News(provider, title, image_url, url, date))

    return final


@login_manager.user_loader
def load_user(user_id):

    return Users.objects(id=str(user_id)).first()


@app.route('/')
@login_required
def index():
    name = current_user.name
    return render_template('index.html', name=name)


@app.route('/news', methods=['GET', 'POST'])
@login_required
def news():
    news_list = None

    if request.method == "POST":

        query = request.form.get("search")

        page = request.form.get("page")

        news_list = get_news(query, page)

        return render_template('news.html', news_list=news_list)

    return render_template('news.html', news_list=news_list)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    name = form.name.data
    user = Users.objects(name=name).first()

    if user:
        if check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login was successfull!")

            return redirect(url_for('index'))

        flash("Invalid Credentials")

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():

    form = CreateUserForm()

    if form.validate_on_submit():

        user = Users(name=form.name.data,
                     password=generate_password_hash(form.password.data, method='sha256'))

        try:
            user.save()

            flash("Registration was successfull, please login")

            return redirect(url_for('login'))

        except:
            flash("User Already Exists, Please Try Again!")

    return render_template('register.html', form=form)


@app.route('/add-workout', methods=['GET', 'POST'])
@login_required
def AddWorkout():

    if request.method == "POST":
        
        extype = request.form.getlist("type")[0]
        
        if extype == 'cardio':
            return redirect(url_for('add_cardio'))
        elif extype == 'resistance':
            return redirect(url_for('add_resistance'))

    return render_template('add_workout.html')

@app.route('/add-workout/cardio', methods=['GET', 'POST'])
@login_required
def add_cardio():
    form = AddCardioForm()
    user = current_user.name

    if form.validate_on_submit():
        cardio = Cardio(user=user,
                        extype='cardio',
                        name=form.name.data,
                        duration=form.duration.data,
                        intensity=form.intensity.data,
                        date=str(form.date.data)
                        )

        cardio.save()

        flash("Save was successfull!")

        return redirect(url_for('AddWorkout'))

    return render_template('add_cardio.html', form=form)

@app.route('/add-workout/resistance', methods=['GET', 'POST'])
@login_required
def add_resistance():
    form = AddResistanceForm()
    user = current_user.name

    if form.validate_on_submit():
        resistance = Resistance(user=user,
                        extype='resistance',
                        name=form.name.data,
                        weight=form.weight.data,
                        sets=form.sets.data,
                        repetitions=form.repetitions.data,
                        rest=form.rest.data,
                        date=str(form.date.data)
                        )

        resistance.save()

        flash("Save was successfull!")

        return redirect(url_for('AddWorkout'))

    return render_template('add_resistance.html', form=form)


@app.route('/edit-cardio/<id>', methods=['GET', 'POST'])
@login_required
def EditCardio(id):

    exercise = Cardio.objects(id=str(id)).first()

    form = EditCardioForm(obj=exercise)

    if form.validate_on_submit():
        exercise.user = exercise.user
        exercise.name = form.name.data
        exercise.duration = form.duration.data
        exercise.intensity = form.intensity.data
        exercise.date = form.date.data

        exercise.save()
        flash("Workout was edited successfully")

        return redirect(url_for('history'))

    form.name.data = exercise.name
    form.duration.data = exercise.duration
    form.intensity.data = exercise.intensity
    form.date.data = exercise.date

    return render_template('edit_cardio.html', form=form)

@app.route('/edit-resistance/<id>', methods=['GET', 'POST'])
@login_required   
def EditResistance(id):

    exercise = Resistance.objects(id=str(id)).first()

    form = EditResistanceForm(obj=exercise)

    if form.validate_on_submit():
        exercise.user = exercise.user
        exercise.name = form.name.data
        exercise.weight = form.weight.data
        exercise.sets = form.sets.data
        exercise.repetitions = form.repetitions.data
        exercise.rest = form.rest.data
        exercise.date = form.date.data

        exercise.save()
        flash("Workout was edited successfully")

        return redirect(url_for('history'))

    form.name.data = exercise.name
    form.weight.data = exercise.weight
    form.sets.data = exercise.sets
    form.repetitions.data = exercise.repetitions
    form.rest.data = exercise.rest
    form.date.data = exercise.date

    return render_template('edit_resistance.html', form=form)


@app.route('/delete-workout/<id>', methods=['GET', 'DELETE'])
@login_required
def DeleteWorkout(id):

    exercise = Resistance.objects(id=str(id)).first()
    exercise.delete()

    flash('Exercise was successfully deleted!')

    return redirect(url_for('history'))


@app.route('/history', methods=['GET'])
@login_required
def history():
    user = current_user.name

    exercises = Resistance.objects(user=user)

    return render_template('history.html', exercises=exercises, user=user)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

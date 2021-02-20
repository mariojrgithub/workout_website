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
    email = db.EmailField(unique=True)
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
                "date": self.date, }


class News:
    def __init__(self, provider, title, image_url, url, date):
        self.provider = provider
        self.title = title
        self.image_url = image_url
        self.url = url
        self.date = date

class Weather:
  def __init__(self, name, state, date, time, 
               icon, condition, temp, windchill, 
               humidity, windspeed, winddir):
    self.name = name
    self.state = state
    self.date = date
    self.time = time
    self.icon = icon
    self.condition = condition
    self.temp = temp
    self.windchill = windchill
    self.humidity = humidity
    self.windspeed = windspeed
    self.winddir = winddir

def get_weather(zip):
  
  url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

  querystring = {"q": str(zip),"days":"3"}

  headers = {
      'x-rapidapi-key': RAPID_API_KEY,
      'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
      }

  response = requests.request("GET", url, headers=headers, params=querystring)

  name = response.json()['location']['name']
  state = response.json()['location']['region']
  date = response.json()['location']['localtime'].split()[0]
  time = response.json()['location']['localtime'].split()[1]
  icon = response.json()['current']['condition']['icon']
  condition = response.json()['current']['condition']['text']
  temp = int(response.json()['current']['temp_f'])
  windchill = int(response.json()['current']['feelslike_f'])
  humidity = response.json()['current']['humidity']
  windspeed = response.json()['current']['wind_mph']
  winddir = response.json()['current']['wind_dir']

  if int(time.split(':')[0]) > 12:
      time = time.split(':')[0].replace(time.split(':')[0], str(int(time.split(':')[0]) - 12)) + ':' + time.split(':')[1] + 'pm'
  else:
      time = time + 'am'

  return Weather(name, state, date, time, 
               icon, condition, temp, windchill, 
               humidity, windspeed, winddir)


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
    weather = get_weather(46312)

    return render_template('index.html', name=name, weather=weather)


@app.route('/news', methods=['GET', 'POST'])
@login_required
def news():
    news_list = None

    if request.method == "POST":
    
        query = request.form.get("search")

        page = request.form.get("page")

        try:
            news_list = get_news(query, page)
        except:
            news_list = get_news('fitness', page)

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
    email = form.email.data
    user = Users.objects(email=email).first()
    
    if user:
        if check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login was successfull!")
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials.")

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():

    form = CreateUserForm()

    password = form.password.data
    val_pass = form.valpassword.data

    if password != val_pass:
        flash("Passwords do not match, please try again!")

    if password == val_pass and form.validate_on_submit():

        user = Users(name=form.name.data,
                     email=form.email.data,
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

        try:
            extype = request.form.getlist("type")[0]
            if extype == 'cardio':
                return redirect(url_for('add_cardio'))
            elif extype == 'resistance':
                return redirect(url_for('add_resistance'))
        except:
            flash("Please make a selection.")

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
        exercise.date = str(form.date.data)

        exercise.save()
        flash("Workout was edited successfully")

        return redirect(url_for('history'))

    form.name.data = exercise.name
    form.duration.data = exercise.duration
    form.intensity.data = exercise.intensity
    form.date.data = str(exercise.date)

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
        exercise.date = str(form.date.data)

        exercise.save()
        flash("Workout was edited successfully")

        return redirect(url_for('history'))

    form.name.data = exercise.name
    form.weight.data = exercise.weight
    form.sets.data = exercise.sets
    form.repetitions.data = exercise.repetitions
    form.rest.data = exercise.rest
    form.date.data = str(exercise.date)

    return render_template('edit_resistance.html', form=form)


@app.route('/delete-workout/<id>', methods=['GET', 'DELETE'])
@login_required
def DeleteWorkout(id):

    try:
        exercise = Resistance.objects(id=str(id)).first()
        exercise.delete()
    except:
        exercise = Cardio.objects(id=str(id)).first()
        exercise.delete()

    flash('Exercise was successfully deleted!')

    return redirect(url_for('history'))


@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    user = current_user.name

    if request.method == "POST":

        try:
            extype = request.form.getlist("type")[0]
        
            if extype == 'cardio':
                return redirect(url_for('cardio_history'))
            elif extype == 'resistance':
                return redirect(url_for('resistance_history'))
        except:
            flash("Please make a selection.")

    return render_template('history.html', user=user)


@app.route('/history/cardio', methods=['GET', 'POST'])
@login_required
def cardio_history():
    user = current_user.name

    exercises = Cardio.objects(user=user)

    return render_template('cardio_history.html', exercises=exercises, user=user)


@app.route('/history/resistance', methods=['GET', 'POST'])
@login_required
def resistance_history():
    user = current_user.name

    exercises = Resistance.objects(user=user)

    return render_template('resistance_history.html', exercises=exercises, user=user)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

import json
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_mongoengine import MongoEngine

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin
from flask_login import login_user, logout_user, current_user, login_required

from create_user import CreateUserForm
from add_workout import AddWorkoutForm
from login import LoginForm
from edit_workout import EditWorkoutForm

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'workout',
    'host': 'localhost',
    'port': 27017
}
app.config['SECRET_KEY']='LongAndRandomSecretKey'

db = MongoEngine()
db.init_app(app)

#login code
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Users(db.Document, UserMixin):
    name = db.StringField(unique=True)
    password = db.StringField()

    def to_json(self):
        return {"name": self.name,
                "password": self.password}

class Exercises(db.Document, UserMixin):
    user = db.StringField()
    name = db.StringField()
    duration = db.StringField()
    intensity = db.IntField()
    date = db.StringField()

    def to_json(self):
        return {"user": self.user,
                "name": self.name,
                "duration": self.duration,
                "intensity": self.intensity,
                "date": self.date}


@login_manager.user_loader
def load_user(user_id):
    
    return Users.objects(id=str(user_id)).first()


@app.route('/')
@login_required
def index():
    name = current_user.name
    return render_template('index.html', name = name)

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
 
    return render_template('login.html', form = form)


@app.route('/register', methods=['GET', 'POST'])
def register():

    form = CreateUserForm()

    if form.validate_on_submit():
        
        user = Users(name=form.name.data,
                    password = generate_password_hash(form.password.data, method = 'sha256'))

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

    form = AddWorkoutForm()

    if form.validate_on_submit():

        user = current_user.name

        exercises = Exercises(user=user,
                            name=form.name.data,
                            duration=form.duration.data,
                            intensity=form.intensity.data,
                            date=str(form.date.data))
        exercises.save()

        flash("Workout was added successfully")
        return redirect(url_for('AddWorkout'))

     
    return render_template('add_workout.html', form=form)

@app.route('/edit-workout/<id>', methods=['GET', 'POST'])
@login_required
def EditWorkout(id):

    exercise = Exercises.objects(id=str(id)).first()
    
    form = EditWorkoutForm(obj=exercise)

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
   

    return render_template('edit_workout.html', form=form)

@app.route('/delete-workout/<id>', methods=['GET', 'DELETE'])
@login_required
def DeleteWorkout(id):

    exercise = Exercises.objects(id=str(id)).first()
    exercise.delete()

    flash('Exercise was successfully deleted!')

    return redirect(url_for('history'))

@app.route('/history', methods=['GET'])
@login_required
def history():
    user = current_user.name

    exercises = Exercises.objects(user=user)
        
    return render_template('history.html', exercises = exercises, user = user)



# @app.route('/', methods=['POST'])
# def update_record():
#     record = json.loads(request.data)
#     user = User.objects(name=record['name']).first()
#     if not user:
#         return jsonify({'error': 'data not found'})
#     else:
#         user.update(email=record['email'])
#     return jsonify(user.to_json())

# @app.route('/', methods=['DELETE'])
# def delete_record():
#     record = json.loads(request.data)
#     user = User.objects(name=record['name']).first()
#     if not user:
#         return jsonify({'error': 'data not found'})
#     else:
#         user.delete()
#     return jsonify(user.to_json())

if __name__ == "__main__":
    app.run(host= '0.0.0.0', debug=True)
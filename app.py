import os
import sys
from datetime import datetime

from flask import Flask,render_template ,redirect 
from flask import flash,session ,request ,url_for
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError 
from flask_sqlalchemy import SQLAlchemy


# ------------ Owen Lib ------------- # 
from subpython.validate import login_required
from subpython.form import LoginForm , RegisterForm
from subpython.config import Development,Production
import subpython.validate as validate



app = Flask(__name__)
app.config.from_object(Production)

# data base config
db = SQLAlchemy(app)

# session config
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)
 

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64) ,nullable=False ,unique=True)
    password = db.Column(db.String(256) ,nullable=False,unique=False)
    # 0 = New user || 1 = Old User
    new_user = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime ,default=datetime.now())

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    task_title = db.Column(db.String(64) ,nullable=False ,unique=False)
    task_info = db.Column(db.String(256) ,nullable=False,unique=False)
    # 0 = on Doing || 1 = Done! 
    status = db.Column(db.Integer ,default = 0)
    date = db.Column(db.DateTime ,default=datetime.now())

# class History(db.Model):
#     __tablename__ = "history"
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     task_title = db.Column(db.String(64) ,nullable=False ,unique=False)
#     task_info = db.Column(db.String(256) ,nullable=False,unique=False)
#     # 0 = on Doing || 1 = Done! || 3 = Delete
#     status = db.Column(db.Integer ,default=0)

if "app.db" not in os.listdir():
    db.create_all()
    print(" * DB Created :)")



# Error Handler for 404 or 500
@app.errorhandler(500)
def error_500_server(e):
    return render_template('500.html'),500

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/")
@login_required
def index():
    user_task = []
    if session.get("user_id"):
        # get user all task from data base
        user_db_data = Task.query.filter_by(user_id=(session['user_id'])).all()
        for index,value in enumerate(user_db_data):
            print(value.status)
            if value.status != 1:
                user_task.append(value)
    
        return render_template("index.html",user_db=user_task,user_id=session['user_id'])
    else:
        return redirect("login")


@app.route("/login",methods=["POST","GET"])
def login():

    if request.method == "GET":
        session.clear()
        form_login = LoginForm()
        return render_template("login.html", form=form_login,error=False)

    # POST
    if request.method == "POST":
        form_login = LoginForm(request.form)
        if form_login.validate():
            username = request.form.get("username")
            password = request.form.get("password")
            checkbox = request.form.get("checkbox")
            
            # safety check
            if not validate.validate_field(username):
                return render_template("login.html", form = form_login ,error=True,error_message="Username is invalid :(")
            if not validate.validate_field(password):
                return render_template("login.html", form = form_login ,error=True,error_message="Password is invalid :(")
                

            # check username and password
            user = User.query.filter_by(username=username).first()
            if not user:
                return render_template("login.html", form=form_login,error=True,error_message="information Wrong :(")
            
            if user.username != username:
                return render_template("login.html", form=form_login,error=True,error_message="username is Wrong :(")

            pass_db = user.password
            if not check_password_hash(pass_db,password):
                return render_template("login.html", form=form_login,error=True,error_message="Password is Wrong :(")
            
            # add user id in db to user session
            session["user_id"] = user.id

            # check its first time user log in to web site to show welcome message
            if user.new_user == 0:
                user.new_user = 1
                db.session.commit()

                flash(f" Welcome Dear {user.username}")
                first = validate.first_login
                return redirect('/')
            else:
                return redirect("/")
        
        else:
             return render_template("login.html", form=form_login,error=True, error_message="Invalid Inputs")



@app.route("/register",methods=["POST","GET"])
def register():
    
    # GET
    if request.method == "GET":
            form = RegisterForm()
            return render_template("register.html",form=form,error=False)

    # POST
    if request.method == "POST":
        form = RegisterForm(request.form)
        if form.validate():
            username = request.form.get("username")
            password = request.form.get("password")
            password_re = request.form.get("password_re")

            # safety check            
            if not validate.validate_field(username):
                return render_template("register.html",form=form,error=True,error_message="Username Is invalid :(")
            
            password_validation = validate.validate_passwords(password,password_re)
            if password_validation == "NS":
                return render_template("register.html",form=form,error=True,error_message="Passwords Are Not Match :(")
            elif password_validation == False:
                return render_template("register.html",form=form,error=True,error_message="Passwords are Wrong")


            # check user is not duplicated
            user_check = User.query.filter_by(username=username).first()
            if user_check:
                return render_template("register.html",form=form,error=True,error_message="Username Already Take by Another User")

            # add it ro to data base 
            new_user = User(username=username,password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()

            # query to data base
            user_in_db = User.query.filter_by(username=username).first()
            if not user_in_db:
                return error_500_server()

            # add first column(welcome message too user task column)
            new_task = Task(user_id=user_in_db.id,task_title=validate.first_login[1],task_info=validate.first_login[2])
            db.session.add(new_task)
            db.session.commit()

            flash(f"Register complete {username} :) ")
            return redirect('login')
        else:
            return render_template("register.html",form=form,error=True,error_message="Invalid Inputs :(")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")

@app.route("/add_new_task",methods=['POST'])
@login_required
def add_new_task():
    title = request.form.get("Task_Info")
    info = request.form.get("Task_Name")   

    if not validate.validate_tasks(title):
        return redirect('/')
    if not validate.validate_tasks(info):
        return redirect('/')
    

    # add task to user db
    new_task = Task(user_id=session['user_id'],task_info=info.title(),task_title=title.title())
    try:
        db.session.add(new_task)
        db.session.commit()
        flash("Task Added SuccessFully")
        return redirect('/')
    except:
        return error_500_server()


@app.route("/edit",methods=["POST","GET"])
@login_required
def edit():
    if request.method == "GET":
        return render_template("edit.html",post_id=request.args.get("post_id"))
    if request.method == "POST":
        # edit section
        title = request.form.get("Edit_Task_Name")
        info = request.form.get("Edit_Task_Info")
        task_id = request.form.get("post_id")

        if not validate.validate_tasks(title):
            return redirect('/')
        if not validate.validate_tasks(info):
            return redirect('/')
        if not validate.validate_tasks(task_id):
            return redirect('/')
        
        try:
            new_task = Task.query.filter_by(id=task_id).first()
            if not new_task:
                return redirect("/")

            new_task.task_title=title.title()
            new_task.task_info=info.title()
            db.session.commit()
            flash("Task Edited Successfully")
            return redirect("/")
        except:
            return error_500_server
        

@app.route("/delete",methods=["POST","GET"])
@login_required
def delete():
    if request.method == "GET":
        return render_template("delete.html",post_id=request.args.get('post_id'))
    if request.method == "POST":
        if request.form.get('delete') == "Yes":
            try:
                new_task = Task.query.filter_by(id=request.form.get('post_id'),user_id=session["user_id"]).first()
                if new_task == None:
                    return redirect("/")
                db.session.delete(new_task)
                db.session.commit()
                flash("Task Deleted successfully")
                return redirect("/")
            except:
                flash(message="Invalid Task",category="error")
                return redirect("/")
        else:
            return redirect("/")
    else:
        return redirect("/")
    

@app.route("/done" ,methods=["POST"])
@login_required
def done():
    if request.method == "POST":
        task_id=request.form.get("post_id")

        # query to data base for change task status to done
        new_task = Task.query.filter_by(id=task_id ,user_id=session["user_id"]).first()
        
        if new_task == None:
            return redirect("/")
        # status code 1 equal to done
        new_task.status = 1
        print(new_task.status)
        print(new_task)
        db.session.commit()
        flash("Task Done. You can See Your all Done Tasks In history Section")
        return redirect("/")


@app.route("/history")
@login_required
def history():
    # query to db to get all Done Task
    old_Task = Task.query.filter_by(status=1,user_id=session["user_id"])
    return render_template("history.html",user_db=old_Task)



@app.route("/temp")
def temp():
    # return render_template("base.html")   
    return "hello"
  
  
 
 
 if __name__ == "__main__":
  app.run()
  
  

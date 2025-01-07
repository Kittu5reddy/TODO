from flask import Flask,render_template,redirect,url_for,request,session
from flask_session import Session
from flask_pymongo import PyMongo
from models import LoginForm,SignupForm,TaskForm
from api_keys import si,mongodb
from flask_bcrypt import Bcrypt


from flask_wtf.csrf import CSRFProtect

app = Flask(__name__,template_folder="template")
csrf = CSRFProtect(app)

app.config["SECRET_KEY"]=si
app.config["MONGO_URI"] = mongodb['url']
bcrypt=Bcrypt(app)
mongo=PyMongo(app).db

#session config
app.config["SESSION_TYPE"] = "mongodb"  # Specify MongoDB as the session type
app.config["SESSION_PERMANENT"] = False  # Make sessions non-permanent
app.config["SESSION_USE_SIGNER"] = True  # Use a signer for better security
app.config["SESSION_KEY_PREFIX"] = "flask_session:"  # Prefix for MongoDB keys

app.config["SESSION_MONGODB"] = mongo.client # Pass the client instance
app.config["SESSION_MONGODB_DB"] = "TODO"  # Database for session storage
app.config["SESSION_MONGODB_COLLECT"] = "sessions"  # Collection for session storage
Session(app)  # This is correct
#main routes
@app.route("/")
def homePage():
    return render_template('main/home.html')



@app.route("/about")
def aboutPage():
    return render_template('main/about.html')


@app.route("/services")
def servicesPage():
    return render_template('main/services.html')

#main routes ends here


#auth routes
@app.route("/signup",methods=["GET","POST"])
def signupPage():
    form=SignupForm()
    if request.method=="POST":
        if form.validate_on_submit():
            if not mongo.user.find_one({'email':form.email.data}):
                username=form.name.data
                email=form.email.data
                password=bcrypt.generate_password_hash(form.password.data)
                mongo.user.insert_one({'email':email,'username':username,'password':password})
                return redirect(url_for('loginPage'))
            else:
                return render_template('auth/signup.html',form=form,message="user exist")
                
    return render_template('auth/signup.html',form=form)

@app.route("/login",methods=["GET","POST"])
def loginPage():
    form=LoginForm()
    if request.method=="POST":
        if form.validate_on_submit():
            user=mongo.user.find_one({'email':form.email.data})
            if user:
                if bcrypt.check_password_hash(user['password'],form.password.data):
                    session['username']=user['username']
                    session['email']=user['email']
                    session['user_id']=str(user['_id'])                  
                    return redirect('profile')
                else:
                    return render_template('auth/login.html',form=form,message="Invalid credinates")
                    
            else:
                 return render_template('auth/login.html',form=form,message="user not found")
                
        
    return render_template('auth/login.html',form=form)

@app.route("/logout")
def logout():
    del session['email']
    del session['username']
    return redirect(url_for('homePage'))

#auth routes end





#dashboard routes


@app.route("/myassignments")
def myAssignments():
    data = mongo.assignments.find({'user_id': session['user_id']}) 
    return render_template('dashboard/my-assignments.html', data1=data)

@app.route("/postassignments",methods=["GET","POST"])
def postAssignments():
    form=TaskForm()
    if request.method=="POST":
        if form.validate_on_submit():
            mongo.assignments.insert_one({'user_id':session['user_id'],'task':form.task.data,'priority':form.priority.data})
            return redirect(url_for('myAssignments'))
    return render_template('dashboard/post-assignments.html',form=form)


@app.route("/complete")
def completePage():
    return render_template('dashboard/my-assignments.html')

@app.route('/myassignments/delete/<task_id>',methods=["POST","GET"])
def delete(task_id):
    mongo.assignments.delete_one({'_id':task_id})
    return redirect(url_for('myAssignments'))



@app.route("/profile")
def profilePage():
    
    return render_template('dashboard/profile.html')




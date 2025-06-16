from controllers.database import db
from flask import request,render_template,url_for,redirect,flash,session
from main import app
from model.models import User , Admin ,  Parkinglot , Parkingspot

@app.route('/login',methods=['GET','POST'])
def login():
    if(request.method=='GET'):
        return render_template('login.html')
    else:
        name = request.form['naam']
        email = request.form['email']
        password = request.form['password']
        user_in_db=None
        if('@gmail.com' in email):
            user_in_db = User.query.filter_by(email=email).first()
        else:
            flash('Please enter a valid email to login !!!')
            return redirect(url_for('login'))
        if(not user_in_db):
            flash('You have to register First !!!')
            return redirect(url_for('register'))
        else:
            if(user_in_db.user_name != name  and user_in_db.password != password):
                flash("enter correct name and correct password to login !!!")
                return redirect(url_for('login'))
            elif(user_in_db.password == password and user_in_db.user_name != name):
                flash("enter correct name to login !!!")
                return redirect(url_for('login'))
            elif(user_in_db.user_name == name and user_in_db.password != password):
                flash("enter correct password to login !!!")
                return redirect(url_for('login'))
        session['User_id'] = user_in_db.user_id
        if('User_id' in session):
            return redirect(url_for('homepage',user_id =user_in_db.user_id))
        
        
@app.route('/register',methods=['GET','POST'])
def register():
    if(request.method=='GET'):
        return render_template('register.html')
    elif(request.method=='POST'):
        name = request.form['naam']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        pincode = request.form['pincode']
        user_in_db = User.query.filter_by(email=email).first()
        original_name=''
        if(user_in_db):
            original_name=user_in_db.user_name
        users = db.session.query(User).all()
        if(not user_in_db and original_name==''):
            found=0
            if('@gmail.com' in email):
                for i in users:
                    if(name==i.user_name):
                        found=1
                        break
                if(found==0):
                    if(len(name)<=45 and len(password)<=45 and len(email)<=45 and len(address)<=45):
                        new_user = User(user_name=name,email=email,password=password,address=address , pincode=pincode)
                        db.session.add(new_user)
                        db.session.commit()
                        flash('Registration Successful , You can Login Now !!!')
                        return redirect(url_for('login'))
                    else:
                        flash('You have entered a field in username , email , address or password  that has length greater than 45 .Please Check Once all the fields !!! ')
                        return redirect(url_for('register'))
                else:
                    flash('Please use another username , username already exists !!!')
                    return redirect(url_for('register'))
            else:
                flash("Enter a valid email id to Register !!!")
                return redirect(url_for('register'))
        else:
            flash('You are already registered , you can login !!!')
        return redirect(url_for('login'))
    
@app.route('/',methods=["GET","POST"])
def role():
    if(request.method=="GET"):
        return render_template('role.html')
    else:
        role = request.form["role"]
        if(role=="User"):
            return redirect(url_for('login'))
        else:
            return redirect(url_for('admin_homepage'))

@app.route('/admin_home',methods=["GET",'POST'])
def admin_homepage():
    if(request.method=="GET"):
        return render_template('admin.html')
    elif(request.method=='POST'):
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        admin_in_db = Admin.query.first()
        if('@gmail.com' not in email):
            flash('Enter a valid Email to login !!!')
            return redirect(url_for('admin_homepage'))
        else:
            if(admin_in_db.admin_name != name and admin_in_db.email != email and admin_in_db.password != password):
                flash ("Enter Correct name , Correct email and Correct password to login !!!")
                return redirect(url_for('admin_homepage'))
            elif(admin_in_db.admin_name != name and admin_in_db.email != email and admin_in_db.password == password):
                flash("Enter Correct name  and Correct email to login !!! ")
                return redirect(url_for('admin_homepage'))
            elif(admin_in_db.email != email and admin_in_db.password != password and admin_in_db.admin_name == name):
                flash("Enter Correct email and Correct password to login !!! ")
                return redirect(url_for('admin_homepage'))
            elif(admin_in_db.admin_name != name and admin_in_db.password != password and admin_in_db.email == email):
                flash("Enter Correct name and Correct password to login !!! ")
                return redirect(url_for('admin_homepage'))
            elif(admin_in_db.admin_name != name and admin_in_db.password == password and admin_in_db.email == email):
                flash("Enter Correct name to login !!! ")
                return redirect(url_for('admin_homepage'))
            elif(admin_in_db.email != email and admin_in_db.password == password and admin_in_db.admin_name == name):
                flash("Enter Correct email to login !!! ")
                return redirect(url_for('admin_homepage'))
            elif(admin_in_db.password != password and admin_in_db.email == email and admin_in_db.admin_name == name):
                flash("Enter Correct password to login !!! ")
                return redirect(url_for('admin_homepage'))
            else:
                session['admin_name'] = name
                session['a_email'] = email
                session['a_pass'] = password
                if('admin_name' in session and 'a_email' in session and 'a_pass' in session):
                    return redirect(url_for('display'))

@app.route('/home_page',methods=["GET"])
def display():
    if(request.method=="GET"):
        if('admin_name' in session and 'a_email' in session and 'a_pass' in session):
            l=[]
            lot = db.session.query(Parkinglot).all()
            for i in lot:
                print(type(i.lot_id))
                empty = 0
                full=0
                spots = db.session.query(Parkingspot).filter(Parkingspot.lot_id==i.lot_id).all()
                for j in spots:
                    if(j.status=='O'):
                        full+=1
                    elif(j.status=='A'):
                        empty+=1
                l.append((i,spots,empty,full))
                print((i,empty,full))
            admin_db = Admin.query.first()
                
            return render_template('admin_homepage.html',lotspot = l,admin_name=admin_db.admin_name)
        else:
            flash('You are not logged in !!!')
            return redirect(url_for('admin_homepage'))
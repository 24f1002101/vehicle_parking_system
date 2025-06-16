from controllers.database import db
from model.models import Registeredspot , User , Parkinglot , Parkingspot
from main import app 
from flask import render_template , url_for , request , session , flash , redirect 
from datetime import datetime
@app.route('/user_homepage/<int:user_id>',methods=['GET','POST'])
def homepage(user_id):
    l=[]
    parkinglot = db.session.query(Parkinglot).all()
    ps = []
    for i in parkinglot:
        empty_parking_spots = db.session.query(Parkingspot).filter(Parkingspot.lot_id==i.lot_id,Parkingspot.status=='A').all()
        if(empty_parking_spots):
            ps.append((i,len(empty_parking_spots)))
    registeredspot = Registeredspot.query.filter_by(registered_user_id=user_id).all()
    print(registeredspot)
    for i in registeredspot:
        spot = db.session.query(Parkingspot).filter(Parkingspot.spot_id==i.registered_spot_id).first()
        print(spot)
        lot = db.session.query(Parkinglot).filter(Parkinglot.lot_id==spot.lot_id).first()
        l.append((i,spot,lot))
    if(request.method=='GET'):
        if('User_id' in session):
            user = db.session.query(User).filter(User.user_id==user_id).first()
            return render_template('user_homepage.html',user=user,details=l,ps=ps)
        else:
            flash('You have to login First !!!')
            return redirect(url_for('login'))
    else:
        user = db.session.query(User).filter(User.user_id==user_id).first()
        inputt = request.form['location']
        print(type(inputt),inputt)
        action = request.form['act']
        if(action=='check'):
            print(1)
            if(inputt.isdigit()):
                l1=[]
                print('Mohan')
                parkinglot = db.session.query(Parkinglot).all()
                for i in parkinglot:
                    print(0)
                    if(inputt in str(i.pincode)):
                        print('Hello')
                        l1.append(i)
                if(len(l1)==0):
                    print(l)
                    flash('Please Enter another Pincode for Parkinglot !!!')
                    return render_template('user_homepage.html',user=user,ps=ps,details=l)
                l2=[]
                for i in l1:
                    empty_parking_spots = db.session.query(Parkingspot).filter(Parkingspot.lot_id==i.lot_id,Parkingspot.status=='A').all()
                    if(empty_parking_spots):
                        l2.append((i,len(empty_parking_spots)))
                return render_template('user_homepage.html',user = user , ps=l2,details=l)
            elif(inputt.isalpha()):
                l1=[]
                print(2)
                parkinglot = db.session.query(Parkinglot).all()
                for i in parkinglot:
                    if(inputt.lower() in i.location.lower()):
                        print('sumu')
                        l1.append(i)
                if(len(l1)==0):
                    print('h')
                    flash('please enter another location for searching Parking Lot !!!')
                    return render_template('user_homepage.html',user=user,ps=ps,details=l)
                else:
                    l2=[]
                    for i in l1:
                        empty_parking_spots = db.session.query(Parkingspot).filter(Parkingspot.lot_id==i.lot_id,Parkingspot.status=='A').all()
                        if(empty_parking_spots):
                            l2.append((i,len(empty_parking_spots)))
                    return render_template('user_homepage.html',user = user , ps=l2,details=l)
        elif(action=='cancel'):
            return redirect(url_for('homepage',user_id=user_id))

@app.route('/edit_profile/<int:user_id>',methods=['GET','POST'] )
def EditProfile(user_id):
    if(request.method=='GET'):
        if('User_id' in session):
           user = User.query.filter_by(user_id=user_id).first()
           return render_template('edit_user.html',user=user)
        else:
            flash('You have to login First !!!')
            return redirect(url_for('login'))
    else:
        user_in_db = User.query.filter_by(user_id=user_id).first()
        name = request.form['naam']
        email = request.form['email']
        address = request.form['address']
        pincode = request.form['pin']
        password = request.form['password']
        typed = request.form['action']
        if(typed == 'change'):
            if(email):
                if('@gmail.com' in email):
                    if(len(email)<=45):
                        user_in_db.email = email
                    else:
                        flash('Enter email of length less than 46 !!!')
                        return redirect(url_for('EditProfile',user_id=user_id))
                else:
                    flash('Enter Valid email to Change the details of yours !!!')
                    return redirect(url_for('EditProfile',user_id = user_id ))
            if(name):
                print('yes')
                if(len(name)<=45):
                    user_in_db.user_name = name
                    print(0)
                else:
                    print(1)
                    flash('Enter name of length less than 46 !!!')
                    return redirect(url_for('EditProfile',user_id=user_id))
            if(address):
                if(len(address)<=50):
                    user_in_db.address = address
                else:
                    flash('Enter address of length less than 51 !!!')
                    return redirect(url_for('EditProfile',user_id=user_id))
            if(pincode):
                pincode = int(pincode)
                user_in_db.pincode = pincode
            if(password):
                if(len(password)<=45):
                    user_in_db.password = password
                else:
                    flash('Enter address of length less than 46 !!!')
                    return redirect(url_for('EditProfile',user_id=user_id))
            db.session.commit()
            if(name or email or address or pincode or password):
                flash('Edited profile Successfully !!!')
            else:
                flash("You haven't modified anything in your profile !!!")
            return redirect(url_for('homepage',user_id = user_in_db.user_id))
        else:
            return redirect(url_for('homepage',user_id=user_in_db.user_id))
        
@app.route('/spot_booking/<int:lot_id>/<int:user_id>',methods=['GET','POST'])
def spot_book(lot_id,user_id):
    user = db.session.query(User).filter(User.user_id==user_id).first()
    empty_first_spot = db.session.query(Parkingspot).filter(Parkingspot.lot_id==lot_id,Parkingspot.status=='A').first()
    spot_id = empty_first_spot.spot_id
    price = db.session.query(Parkinglot).filter(Parkinglot.lot_id==lot_id).first().price
    if(request.method=='GET'):
        if('User_id' in session):
            return render_template('book_spot.html',user_id=user_id,spot_id=empty_first_spot.spot_id,lot_id=lot_id, price = price)
        else:
            flash('You must login !!!')
            return redirect(url_for('login'))
    else:
        vehicle = request.form['vehicle_no']
        action = request.form['act']
        if(action=='reserve'):
            if(vehicle):
                if(len(vehicle)<=12):
                    registeredspot = Registeredspot(registered_spot_id=spot_id,registered_user_id=user_id , vehicle_no = vehicle , cost_per_hour = price )
                    db.session.add(registeredspot)
                    db.session.commit()
                    spot = db.session.query(Parkingspot).filter(Parkingspot.lot_id==lot_id, Parkingspot.spot_id==spot_id).first()
                    spot.status='O'
                    db.session.commit()
                    flash('Successfully Registered the spot , Welcome !!!')
                    return redirect(url_for('homepage',user_id=user_id))
                else:
                    flash('Please enter Vehicle Number length less than 13 !!!')
                    return redirect(url_for('spot_book',lot_id=lot_id,user_id=user_id))
            else:
                flash('Please Enter Vehicle Number to Book Spot !!!')
                return redirect(url_for('spot_book',lot_id=lot_id, user_id=user_id))
        elif(action=='cancel'):
            return redirect(url_for('homepage',user_id=user_id))
        
@app.route('/release_lot/<int:spot_id>/<int:user_id>/<int:registration_id>',methods=['GET','POST'])
def release(spot_id,user_id,registration_id):
    parkingspot = db.session.query(Parkingspot).filter(Parkingspot.spot_id==spot_id).first()
    parkinglot = db.session.query(Parkinglot).filter(Parkinglot.lot_id==parkingspot.lot_id).first()
    registeredspot = db.session.query(Registeredspot).filter(Registeredspot.registration_id==registration_id).first()

    if(request.method=='GET'):
        if('User_id' in session):
            timestamp = datetime.now()
            time = timestamp-registeredspot.parking_timestamp
            total_sec = time.total_seconds()
            total_hours = int(total_sec/3600)
            total_price=0
            if(total_hours<=1):
                total_price=parkinglot.price
            else:
                total_price = total_hours * parkinglot.price
            return render_template('release.html',parkingspot=parkingspot,parkinglot=parkinglot,registeredspot=registeredspot,user_id=user_id,timestamp=timestamp,price=total_price)
        else:
            flash('You must login !!!')
            return redirect(url_for('login'))
    else:
        action = request.form['act']
        if(action=='Release'):
            timestamp = datetime.now()
            registeredspot.leaving_timestamp = timestamp
            parkingspot.status = 'A'
            db.session.commit()
            flash('Successfully parked out from the spot , Drive Safe !!!')
            return redirect(url_for('homepage',user_id=user_id))
        elif(action=='Cancel'):
            return redirect(url_for('homepage',user_id=user_id))

@app.route('/summary/<int:user_id>',methods=['GET'])
def summary(user_id):
    if(request.method=='GET'):
        if('User_id' in session):
            registeredspot = db.session.query(Registeredspot).filter(Registeredspot.registered_user_id==user_id).all()
            l=[]
            for i in registeredspot:
                total_price=0
                total_hours=0
                parkingspot = db.session.query(Parkingspot).filter(Parkingspot.spot_id==i.registered_spot_id).first()
                parkinglot = Parkinglot.query.filter_by(lot_id=parkingspot.lot_id).first() 
                if(i.leaving_timestamp):
                    timestamp = i.leaving_timestamp - i.parking_timestamp
                    total_sec = timestamp.total_seconds()
                    total_hours = total_sec/3600
                    if(total_hours <= 1):
                        total_price=parkinglot.price
                    else:
                        total_price=parkinglot.price *total_hours
                    l.append((i,parkingspot,parkinglot,total_price,total_hours))
            return render_template('user_summary.html',details=l,user_id=user_id)
        else:
            flash('You must login !!!')
            return redirect(url_for('login'))
        
@app.route('/logout/<int:user_id>')
def logout(user_id):
    if('User_id' in session):
        session.pop('User_id')
        flash('Logouted Successfully , Thank You Have a great Day !!!')
        return redirect(url_for('login'))
    else:
        flash('You have to login first to logout  !!!')
        return redirect(url_for('login'))
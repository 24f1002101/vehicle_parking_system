from main import app
from controllers.database import db
from flask import session,url_for,render_template,request,flash,redirect
from model.models import Admin , User , Parkinglot , Parkingspot , Registeredspot
from datetime import datetime
@app.route('/change_details',methods=["GET","POST"])
def edit_profile():
    if(request.method=='GET'):
        if('admin_name' in session and 'a_email' in session and 'a_pass' in session):
            return render_template('edit_admin.html')
        else:
            flash("You should Login First !!!")
            return redirect(url_for('admin_homepage'))
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        action  = request.form['edit']
        if(action=='Change'):
            admin_db = Admin.query.first()
            if(email):
                if('@gmail' not in email):
                    flash('PLease enter a valid email to change !!!')
                    return redirect(url_for('edit_profile'))
                else:
                    if(len(email)<=45):
                        admin_db.email = email
                    else:
                        flash('PLease enter email of length less than 46 !!!')
                        return redirect(url_for('edit_profile'))
            if(name):
                if(len(name)<=45):
                    admin_db.admin_name = name
                else:
                    flash('PLease enter name of length less than 46 !!!')
                    return redirect(url_for('edit_profile'))
    
            if(password):
                if(len(password)<=45):
                    admin_db.password  = password
                else:
                    flash('PLease enter password of length less than 46 !!!')
                    return redirect(url_for('edit_profile'))
                
            db.session.commit()
            if(name or email or password):
                flash('Successfully Changed The Details !!!')
            else:
                flash("You haven't updated anything in your profile!!!")
                
            return redirect(url_for('display'))
        elif(action=="Don't Change"):
            return redirect(url_for('display'))
            
@app.route('/display_users',methods=["GET"])
def project_user():
    if('admin_name' in session and 'a_email' in session and 'a_pass' in session):
        users_in_db  = User.query.all()
        if(users_in_db):
            return render_template('users_registered.html',users=users_in_db)
        else:
            return render_template('users_registered.html',users=[])
    else:
        flash('You should Login to Know the Details of Users !!!')
        return redirect(url_for('admin_homepage'))
    
@app.route('/add_lot',methods=['GET','POST'])
def add_parkinglot():
    if(request.method=='GET'):
        if('admin_name' in session and 'a_email' in session and 'a_pass' in session):
            return render_template('add_lot.html')
        else:
            return redirect(url_for('admin_homepage'))
    else:
        location = request.form['location']
        address = request.form['address']
        pincode = int(request.form['pin'])
        max_spots = int(request.form['max_spots'])
        price = int(request.form['price'])
        lot_db = Parkinglot.query.filter_by(location=location,address=address,pincode=pincode).first()
        if(not lot_db):
            if(len(location)<=45 and len(address)<=50):
                new_lot = Parkinglot(location=location,price=price,address=address,pincode=pincode,max_spots=max_spots)
                db.session.add(new_lot)
                db.session.commit()
                new_lot_id = Parkinglot.query.filter_by(location=location,price=price,address=address,pincode=pincode,max_spots=max_spots).first().lot_id
                for i in range(max_spots):
                    db.session.add(Parkingspot(status='A',lot_id=new_lot_id))
                    db.session.commit()
                return redirect(url_for('display'))
            else:
                if(len(location)>45 and len(address)>50):
                    flash('Please enter location of length less than 46 and address of length less than 51 !!!')
                elif(len(location)>45 and len(address)<51):
                    flash('Please enter location of length less than 46 !!!')
                elif(len(location)<=45 and len(address)>50):
                    flash('Please enter address of length less than 5!!!')
                return redirect(url_for('add_parkinglot'))
        else:
            flash("You already added Parking Lot with this address !!!")
            return redirect(url_for('display'))
        
@app.route('/EditLot/<int:lot_id>',methods=['GET','POST'])
def Edit(lot_id):
    lot = db.session.query(Parkinglot).filter(Parkinglot.lot_id==lot_id).first()
    empty_spots = db.session.query(Parkingspot).filter(Parkingspot.lot_id==lot.lot_id,Parkingspot.status=='A').all()
    available_spots = db.session.query(Parkingspot).filter(Parkingspot.lot_id==lot.lot_id,Parkingspot.status=='O').all()
    available = len(available_spots)
    registered = db.session.query(Registeredspot).all()
    empty=len(empty_spots)
    if(request.method=='GET'):
        if('admin_name' in session and 'a_email' in session and 'a_pass' in session):
            return render_template('edit_lot.html',lot=lot,empty=empty,available=available)
    else:
        action = request.form['edit']
        location = request.form['location']
        address = request.form['address']
        pincode = request.form['pin']
        if(action=='Change'):
            if(pincode):
                pincode = int(pincode)
            max_spots = request.form['max_spots']
            price = request.form['price']
            if(price):
                price = int(price)
            if(location):
                if(len(location)<=45):
                    lot.location = location
                else:
                    flash('Please Enter location of length less than 46 !!!')
                    return redirect(url_for('Edit',lot_id=lot_id))
            if(address):
                if(len(address)<=50):
                    lot.address = address
                else:
                    flash('Please Enter Address of length less than 50 !!!')
                    return redirect(url_for('Edit',lot_id=lot_id))
            if(pincode):
                lot.pincode = pincode
            if(price):
                lot.price = price
            if(max_spots):
                spots_val = int(max_spots.split()[0])
                operation = max_spots.split()[1]
                if(operation=='i'):
                    lot.max_spots += spots_val
                    for i in range(spots_val):
                        new_spot = Parkingspot(status='A',lot_id=lot.lot_id)
                        db.session.add(new_spot)
                        db.session.commit()
                elif(operation=='d'):
                    if(spots_val > empty):
                        flash('Please Enter another value of max_spots , cannot delete Spots !!!')
                        return redirect(url_for('Edit',lot_id=lot.lot_id))
                    elif(spots_val<=empty):
                        count=0
                        lot.max_spots -= spots_val
                        for i in empty_spots:
                            if(count<spots_val):
                                for j in registered:
                                    if(j.registered_spot_id==i.spot_id):
                                        db.session.delete(j)
                                        db.session.commit()
                                db.session.delete(i)
                                db.session.commit()
                            else:
                                break
                            count+=1
            db.session.commit()
            if(location or address or pincode or max_spots or price):
                flash('Successfully changed the details of Lot !!!')
            else:
                flash("You haven't changed the details of the lot !!!")
            return redirect(url_for('display'))
        elif(action=="Don't Change"):
            return redirect(url_for('display'))
    
@app.route('/deleteLot/<int:lot_id>',methods=['GET'])
def deletelot(lot_id):
    if('admin_name' in session and 'a_email' in session and 'a_pass' in session):
        lot = db.session.query(Parkinglot).filter(Parkinglot.lot_id==lot_id).first()
        empty_spots = db.session.query(Parkingspot).filter(Parkingspot.lot_id==lot_id,Parkingspot.status=='A').all()
        spot_ids = db.session.query(Parkingspot).filter(Parkingspot.lot_id==lot_id).all()
        l = []
        for i in spot_ids:
            l.append(i.spot_id)
        registered = db.session.query(Registeredspot).all()
        for i in registered:
            if(i.registered_spot_id in l):
                db.session.delete(i)
                db.session.commit()
        if(lot.max_spots==len(empty_spots)):
            for i in empty_spots:
                db.session.delete(i)
                db.session.commit()
            db.session.delete(lot)
            db.session.commit()
            flash('Successsfully deleted the Parking lot !!!')
            return redirect(url_for('display'))
        else:
            flash('You cannot delete the Parking Lot !!!')
            return redirect(url_for('display'))
    else:
        return redirect(url_for('admin_homepage'))

@app.route('/expand/<int:lot_id>',methods=['GET'])
def expansion(lot_id):
    if(request.method=='GET'):
        if('admin_name' in session and 'a_email' in session and 'a_pass' in session):
            lot = db.session.query(Parkinglot).filter(Parkinglot.lot_id==lot_id).first()
            spots_lot = db.session.query(Parkingspot).filter(Parkingspot.lot_id==lot_id).all()
            return render_template('lotspot_details.html',lot= lot ,spots = spots_lot)
        else:
            return redirect(url_for('admin_homepage'))
@app.route('/delete_spot/<int:spot_id>/<int:lot_id>')
def delete_spot(spot_id,lot_id):
    if(request.method=='GET'):
        if('admin_name' in session and 'a_email' in session and 'a_pass' in session):
            registered_spot = db.session.query(Registeredspot).filter(Registeredspot.registered_spot_id==spot_id).all()
            parkingspot = Parkingspot.query.filter_by(spot_id=spot_id).first()
            parkinglot = Parkinglot.query.filter_by(lot_id=lot_id).first()
            if(registered_spot):
                for i in registered_spot:
                    db.session.delete(i)
                    db.session.commit()
                db.session.delete(parkingspot)
                parkinglot.max_spots  = parkinglot.max_spots -1 
                db.session.commit()
            else:
                db.session.delete(parkingspot)
                parkinglot.max_spots  = parkinglot.max_spots -1 
                db.session.commit()
            flash('successfully deleted the Spot with spot_id '+ str(spot_id)+ " in Lot with lot_id" + str(lot_id))
            return redirect(url_for('expansion',lot_id=lot_id))
        else:
            return redirect(url_for('admin_homepage'))

@app.route('/show/<int:spot_id>/<int:lot_id>')
def show(spot_id,lot_id):
    if(request.method=='GET'):
        if('admin_name' in session and 'a_email' in session and 'a_pass' in session):
            parkinglot = Parkinglot.query.filter_by(lot_id=lot_id).first()
            registered_spot = db.session.query(Registeredspot).filter(Registeredspot.registered_spot_id==spot_id,Registeredspot.leaving_timestamp==None).first()
            user = User.query.filter_by(user_id=registered_spot.registered_user_id).first()
            print(registered_spot)
            parking_time = None
            total_hours = 0
            total_price = 0
            flag = False
            if(registered_spot):
                parking_time = datetime.now() - registered_spot.parking_timestamp
                total_sec = parking_time.total_seconds()
                print(total_sec)
                total_hours = int(total_sec/3600)
                print(total_hours)
                if(total_hours <= 1):
                    total_price=parkinglot.price
                else:
                    total_price=parkinglot.price*total_hours
            return render_template('registered_details.html',registered_spot=registered_spot,hours = total_hours , price=total_price,lot_id=lot_id,user=user)
        else:
            return redirect(url_for('admin_homepage'))
        
@app.route('/search_by_admin',methods=['POST','GET'])
def admin_search():
    if(request.method=='GET'):
        if('admin_name' in session and 'a_email' in session and 'a_pass' in session):
            details = []
            lots = db.session.query(Parkinglot).all()
            for i in lots:
                available = 0
                occupied = 0
                parkingspots = db.session.query(Parkingspot).filter(Parkingspot.lot_id==i.lot_id).all()
                for j in parkingspots:
                    if(j.status=='O'):
                        occupied+=1
                    elif(j.status=='A'):
                        available+=1
                print((i,available,occupied))
                details.append((i,available,occupied))
            return render_template('admin_search.html',details=details)
        else:
            return redirect(url_for('admin_homepage'))
    else:
        option = request.form['searching']
        print(option)
        value = request.form['parameter']
        print(value)
        l=[]
        if(option=='user_id'):
            if(value and value.isdigit()):
                value=int(value)
                registered_spot_ids = db.session.query(Registeredspot.registered_spot_id).filter(Registeredspot.registered_user_id==value,Registeredspot.leaving_timestamp==None).all()
                if(registered_spot_ids):
                    for i in registered_spot_ids:
                        parkingspot = db.session.query(Parkingspot).filter(Parkingspot.spot_id==i.registered_spot_id).first()
                        parkinglot = db.session.query(Parkinglot).filter(Parkinglot.lot_id==parkingspot.lot_id).first()
                        empty=0
                        full=0
                        parkingspots = db.session.query(Parkingspot).filter(Parkingspot.lot_id==parkinglot.lot_id).all()
                        for j in parkingspots:
                            if(j.status=='O'):
                                full+=1
                            elif(j.status=='A'):
                                empty+=1
                        l.append((parkinglot,empty,full))
                else:
                    flash('Enter another User id , entered user_id has not parked any vehicle in any lot !!!')
                    return redirect(url_for('admin_search'))
            else:
                flash('Enter a valid Input for searching by User Id')
                return redirect(url_for('admin_search'))
        
        elif(option=='location'):
            if(value and value.isalpha()):
                lots  = Parkinglot.query.all()
                for i in lots:
                    if(value.lower() in i.location.lower()):
                        full=0
                        empty=0
                        parkingspot = db.session.query(Parkingspot).filter(Parkingspot.lot_id==i.lot_id).all()
                        for j in parkingspot:
                            if(j.status=='A'):
                                empty+=1
                            elif(j.status=='O'):
                                full+=1
                        l.append((i,empty,full))
            else:
                flash('Enter a valid Input for searching by Location')
                return redirect(url_for('admin_search'))
            
            if(len(l)==0):
                flash('Enter a different location, No parkinglot with entered location by you !!!')
                return redirect(url_for('admin_search'))
            
        elif(option=='pincode'):
            print(type(value))
            if(value and value.isdigit()):
                print(1)
                lots = Parkinglot.query.all()
                for i in lots:
                    if(value in str(i.pincode)):
                        print(i.pincode)
                        parkingspot = db.session.query(Parkingspot).filter(Parkingspot.lot_id==i.lot_id).all()
                        full=0
                        empty=0
                        print(parkingspot)
                        for j in parkingspot:
                            if(j.status=='O'):
                                full+=1
                            elif(j.status=='A'):
                                empty+=1
                        l.append((i,empty,full))
                        print(l)
            else:
                flash('Enter a valid Input for searching by Pincode ')
                return redirect(url_for('admin_search'))
            if(len(l)==0):
                flash('Enter a different pincode, No parkinglot with entered pincode by you !!!')
                return redirect(url_for('admin_search'))
    
        return render_template('admin_search.html',details=l)
            
@app.route('/summary')
def admin_summary():
    if('admin_name' in session and 'a_email' in session and 'a_pass' in session):
        lots = Parkinglot.query.all()
        registered = Registeredspot.query.all()
        utilizing={}
        utilized = {}
        cost = {}
        cor = {}
        occupied = {}
        available = {}
        for i in registered:
            if(i.leaving_timestamp is None):
                parkingspot = Parkingspot.query.filter_by(spot_id=i.registered_spot_id).first()
                parkinglot = Parkinglot.query.filter_by(lot_id=parkingspot.lot_id).first()
                timestamp = datetime.now()
                time = timestamp - i.parking_timestamp
                total_sec = time.total_seconds()
                total_hours = int(total_sec / 3600)           
                cost_per_hour = parkinglot.price
                total_price = 0
                if(total_hours<=1):
                    total_price = cost_per_hour
                else:
                    total_price = cost_per_hour * total_hours

                if(parkinglot not in utilizing):
                    utilizing[parkinglot] =1
                elif(parkinglot in utilizing):
                    utilizing[parkinglot]+=1

                if(parkinglot not in cost):
                    cost[parkinglot] = total_price
                elif(parkinglot in cost):
                    cost[parkinglot] += total_price


            elif(i.leaving_timestamp is not None):
                parkingspot = Parkingspot.query.filter_by(spot_id=i.registered_spot_id).first()
                parkinglot = Parkinglot.query.filter_by(lot_id=parkingspot.lot_id).first()
                time = i.leaving_timestamp - i.parking_timestamp
                time_sec = time.total_seconds()
                total_hours = int(time_sec / 3600)
                cost_per_hour = parkinglot.price
                total_price = 0
                if(total_hours<=1):
                    total_price = cost_per_hour
                else:
                    total_price = cost_per_hour * total_hours

                if(parkinglot not in utilized ):
                    utilized[parkinglot] =1
                elif(parkinglot in utilized):
                    utilized[parkinglot]+=1

                if(parkinglot not in cost):
                    cost[parkinglot] = total_price
                elif(parkinglot in cost):
                    cost[parkinglot] += total_price
        if(lots):
            for i in lots:
                parkingspots = db.session.query(Parkingspot).filter(Parkingspot.lot_id==i.lot_id).all()
                empty_spots = Parkingspot.query.filter_by(lot_id=i.lot_id,status='A').all()
                full_spots = Parkingspot.query.filter_by(lot_id=i.lot_id,status='O').all()
                empty=0
                full=0
                if(parkingspots):
                    for j in parkingspots:
                        if(j.status=='O'):
                            full+=1
                        elif(j.status=='A'):
                            empty+=1
                corc = 0
                if(full==0):
                    corc=0
                elif(full>=1):
                    corc = (full/i.max_spots)*100
                    print(corc)
                print((empty,full,i.max_spots))
                if(i not in cor):
                    cor[i] = corc
                if(i not in occupied):
                    occupied[i] = len(full_spots)
                if(i not in available):
                    available[i] = len(empty_spots)
        for i in lots:
            if(i not in utilizing):
                utilizing[i] = 0
            if(i not in utilized):
                utilized[i] = 0
            if(i not in cost):
                cost[i] = 0
            if(i not in cor):
                cor[i]=0

        return render_template('admin_summary.html',utilizing=utilizing,utilized=utilized,cost=cost,cor=cor,occupied=occupied,available=available)
    else:
        return redirect(url_for('admin_homepage'))

@app.route('/logout')
def logout_admin():
    if('admin_name' in session and 'a_email' in session and 'a_pass' in session):
        session.pop('admin_name')
        session.pop('a_email')
        session.pop('a_pass')
        flash('Successfully logged out !!!')
        return redirect(url_for('admin_homepage'))
    else:
        flash('You should login first !!!')
        return redirect(url_for('admin_homepage'))
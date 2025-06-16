from flask import Flask , render_template , url_for , session
from controllers.database import db
from controllers.config import Config
from flask_migrate import Migrate
from model.models import *
app = Flask(__name__ , static_folder='static', static_url_path='/',template_folder='templates')
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
with app.app_context():
   # db.create_all()
    admin_in_db = Admin.query.first()
    if(not admin_in_db):
        admin = Admin(admin_name="Alam Balaji",email = "alambalaji1972@gmail.com",password="Balaji_459")
        db.session.add(admin)
        db.session.commit()
        
from controllers.auth import *
from controllers.admin_func import *
from controllers.user_func import * 
if __name__=='__main__':
    app.run(debug=True)
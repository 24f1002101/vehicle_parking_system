VPMS (Vehicle Parking Management System) 

Overview :
1. This Vehicle Parking Management System consists of two roles (System Admin , Parking User).
2. This Vehicle Parking Management System allows admin to view about parkinglots,parkingspots,users,summary about parkinglots,editing his profile etc
3. This Vehicle Parking Management System allows users to view their Parking history,parkinglots , book spot in parkinglot , edit his profile etc

Features:
1. For Admin :
    1. Dashboard : Overview of all parkinglots , editing the parkinglot , delete parkinglot if empty
    2. Users : viewing all the registered Users
    3. Search : Search the parkinglots by user_id or location or pincode .if he clicks on parkinglot it expands and displays the all available and empty spots in that lot , there he/she can view details of occupied spot and delete the spot if it is empty .
    4. Edit Profile: Editing his/her profile
    5. logout : logging out of the system 

2. For User:
    1. Dashboard: Overview of his/her parking history if available and details of all parkinglots if it contains atleast one empty parking spot
    2. Edit Profile: editing his/her profile
    3. Summary:Overview of details which he parked out from the lots.

Technologies Used
1. Flask: Python web framework for backend logic.
2. SQLAlchemy: ORM for managing database relationships and queries.
3. Bootstrap and CSS: Frontend framework for styling and responsive design.
4. SQLite: Database for data persistence.
5. Jinja2: Templating engine for rendering HTML with dynamic data.

Installation
1. Clone the repository:
    git clone https://github.com/24f1002101/vehicle_parking_system.git
    cd vehicle_parking_system
2. Run the application:
    python main.py
The app will be accessible at https://127.0.0.1:5000/. The database will be created automatically on first run. bt no problem I have attached the database also ...

File Structure
vehicle_parking_system/
├── templates                 # HTML templates for rendering pages
├── instance                  # Contains the database of sqlite3
├── main.py                   # Main application file
├── contollers                # Contains(python files) implementing functionalities of user and admin
├── model                     # Contains the model classes of the database
├── .gitignore                # Contains the pycache and virtual environment folder
├── README.md                 # Project documentation

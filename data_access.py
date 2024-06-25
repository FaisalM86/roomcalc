from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Project, Room, Surface, SupplySystem, RoomSupplySystem, Light, Personnel, Equipment
from config import DATABASE_PATH  # Change this line to import DATABASE_PATH

# Create an engine that stores data in the local directory's RoomCalc.db file.
engine = create_engine(f"sqlite:///{DATABASE_PATH}")

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Function to create a new session
def create_session():
    return Session()

# Create a session
session = create_session()

# Add CRUD functions for each entity
def add_project(project):
    """Add a new project to the database."""
    session.add(project)
    session.commit()

def get_project_by_id(project_id):
    """Retrieve a project by its ID."""
    return session.query(Project).filter_by(ProjectID=project_id).first()

def update_project(project_id, project_data):
    """Update an existing project."""
    project = get_project_by_id(project_id)
    for key, value in project_data.items():
        setattr(project, key, value)
    session.commit()

def delete_project(project_id):
    """Delete a project by its ID."""
    project = get_project_by_id(project_id)
    if project:
        session.delete(project)
        session.commit()

def get_all_projects():
    """Retrieve all projects."""
    return session.query(Project).all()

def add_room(room):
    """Add a new room to the database."""
    session.add(room)
    session.commit()

def get_room_by_id(room_id):
    """Retrieve a room by its ID."""
    return session.query(Room).filter_by(RoomID=room_id).first()

def update_room(room):
    """Update an existing room."""
    session.merge(room)
    session.commit()

def delete_room(room_id):
    """Delete a room by its ID."""
    room = get_room_by_id(room_id)
    if room:
        session.delete(room)
        session.commit()

def get_room_data(room_id):
    """Retrieve room data by room ID."""
    return session.query(Room).filter_by(RoomID=room_id).first()

def get_surface_data(room_id):
    """Retrieve surface data by room ID."""
    return session.query(Surface).filter_by(RoomID=room_id).all()

def get_supply_system_data(project_id):
    """Retrieve supply system data by project ID."""
    return session.query(SupplySystem).filter_by(ProjectID=project_id).all()

def get_personnel_data(room_id):
    """Retrieve personnel data by room ID."""
    return session.query(Personnel).filter_by(RoomID=room_id).all()

def get_equipment_data(room_id):
    """Retrieve equipment data by room ID."""
    return session.query(Equipment).filter_by(RoomID=room_id).all()

def get_light_data(room_id):
    """Retrieve light data by room ID."""
    return session.query(Light).filter_by(RoomID=room_id).all()

def update_room_calculations(room_id, total_heat_gain, required_airflow):
    """Update the room with calculated values"""
    session = create_session()
    room = session.query(Room).filter_by(RoomID=room_id).first()
    if room:
        room.TotalHeatGain = total_heat_gain
        room.RequiredAirflow = required_airflow
        session.commit()
    session.close()

# Initialize the database
def init_db():
    """Initialize the database and create tables."""
    Base.metadata.create_all(engine)

# Ensure the database is initialized
init_db()

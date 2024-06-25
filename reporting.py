from sqlalchemy import create_engine
# reporting.py
# Handles the generation and management of reports for the RoomCalc application

from sqlalchemy.orm import sessionmaker
from models import Project, Room, Surface, SupplySystem, RoomSupplySystem, Light, Personnel, Equipment
from config import DATABASE_URL
import pandas as pd

def create_session():
    """Create and return a new session"""
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()

def generate_summary_report(project_id):
    """Generate a summary report for a given project"""
    session = create_session()
    try:
        project = session.query(Project).filter(Project.ProjectID == project_id).one()
        rooms = session.query(Room).filter(Room.ProjectID == project_id).all()
        
        print(f"Summary Report for Project: {project.ProjectName}")
        print("Room Details:")
        for room in rooms:
            print(f"Room Name: {room.RoomName}, Min Air Change Rate: {room.MinAirChangeRate}, Min Ventilation Per Area: {room.MinVentilationPerArea}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def generate_heat_load_list(project_id):
    """Generate a heat load list for each room in a project"""
    session = create_session()
    try:
        rooms = session.query(Room).filter(Room.ProjectID == project_id).all()
        heat_loads = []
        for room in rooms:
            heat_load = {
                'Room Name': room.RoomName,
                'Heat Load Summer': sum([light.HeatLoadSummer for light in room.lights]),
                'Heat Load Winter': sum([light.HeatLoadWinter for light in room.lights])
            }
            heat_loads.append(heat_load)
        
        df = pd.DataFrame(heat_loads)
        print(df)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def generate_detailed_report(project_id):
    """Generate a detailed report showing all input and calculated values for each room"""
    session = create_session()
    try:
        project = session.query(Project).filter(Project.ProjectID == project_id).one()
        rooms = session.query(Room).filter(Room.ProjectID == project_id).all()
        
        print(f"Detailed Report for Project: {project.ProjectName}")
        for room in rooms:
            print(f"Room Name: {room.RoomName}")
            print("Surfaces:")
            for surface in room.surfaces:
                print(f"Type: {surface.SurfaceType}, Area: {surface.Area}, UValue: {surface.UValue}")
            print("Supply Systems:")
            for rss in room.room_supply_systems:
                supply_system = session.query(SupplySystem).filter(SupplySystem.SupplySystemID == rss.SupplySystemID).one()
                print(f"System Name: {supply_system.SystemName}, Temp Supply Winter: {supply_system.TempSupplyWinter}")
            print("Lights:")
            for light in room.lights:
                print(f"Description: {light.LightDescription}, Heat Load Summer: {light.HeatLoadSummer}")
            print("Personnel:")
            for personnel in room.personnels:
                print(f"Quantity: {personnel.Quantity}, Heat Load Per Person Summer: {personnel.HeatLoadPerPersonSummer}")
            print("Equipment:")
            for equipment in room.equipments:
                print(f"Description: {equipment.EquipmentDescription}, Heat Load Summer: {equipment.HeatLoadSummer}")
            print("\n")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()



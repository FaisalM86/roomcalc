from sqlalchemy.exc import NoResultFound
# project_management.py
# Handles project creation, modification, and deletion functionalities for the RoomCalc application

from sqlalchemy.orm import sessionmaker
from models import Project
from data_access import create_session
import datetime

def create_project(project_data):
    """
    Create a new project with the given data.
    :param project_data: Dictionary containing project details.
    :return: Project instance if created successfully, None otherwise.
    """
    session = create_session()
    try:
        new_project = Project(
            ProjectName=project_data['ProjectName'],
            Client=project_data['Client'],
            Contract=project_data['Contract'],
            SubContractor=project_data['SubContractor'],
            DocumentNumber=project_data['DocumentNumber'],
            Revision=project_data['Revision'],
            RevisionDate=project_data['RevisionDate'],
            AmbientTempSummer=project_data['AmbientTempSummer'],
            AmbientTempWinter=project_data['AmbientTempWinter'],
            DefaultUValue=project_data['DefaultUValue'],
            Density=project_data['Density'],
            HeatCapacity=project_data['HeatCapacity']
        )
        session.add(new_project)
        session.commit()
        return new_project
    except Exception as e:
        print(f"Error creating project: {e}")
        session.rollback()
        return None
    finally:
        session.close()

def update_project(project_id, update_data):
    """
    Update an existing project.
    :param project_id: ID of the project to update.
    :param update_data: Dictionary containing fields to update.
    :return: True if the project was updated successfully, False otherwise.
    """
    session = create_session()  # Fixed typo: changed create_data() to create_session()
    try:
        project = session.query(Project).filter(Project.ProjectID == project_id).one()
        for key, value in update_data.items():
            if hasattr(project, key):  # Check if the attribute exists
                setattr(project, key, value)
        session.commit()
        return True
    except NoResultFound:
        print(f"Project with ID {project_id} not found.")
        return False
    except Exception as e:
        print(f"Error updating project: {e}")
        session.rollback()
        return False
    finally:
        session.close()

def delete_project(project_id):
    """
    Delete a project by its ID.
    :param project_id: ID of the project to delete.
    :return: True if the project was deleted successfully, False otherwise.
    """
    session = create_session()
    try:
        project = session.query(Project).filter(Project.ProjectID == project_id).one()
        session.delete(project)
        session.commit()
        return True
    except NoResultFound:
        print(f"Project with ID {project_id} not found.")
        return False
    except Exception as e:
        print(f"Error deleting project: {e}")
        session.rollback()
        return False
    finally:
        session.close()

def copy_project(project_id):
    """
    Copy an existing project.
    :param project_id: ID of the project to copy.
    :return: New Project instance if copied successfully, None otherwise.
    """
    session = create_session()
    try:
        project = session.query(Project).filter(Project.ProjectID == project_id).one()
        new_project = Project(
            ProjectName=project.ProjectName + " Copy",
            Client=project.Client,
            Contract=project.Contract,
            SubContractor=project.SubContractor,
            DocumentNumber=project.DocumentNumber,
            Revision=project.Revision,
            RevisionDate=datetime.datetime.now().strftime("%Y-%m-%d"),
            AmbientTempSummer=project.AmbientTempSummer,
            AmbientTempWinter=project.AmbientTempWinter,
            DefaultUValue=project.DefaultUValue,
            Density=project.Density,
            HeatCapacity=project.HeatCapacity
        )
        session.add(new_project)
        session.commit()
        return new_project
    except Exception as e:
        print(f"Error copying project: {e}")
        session.rollback()
        return None
    finally:
        session.close()


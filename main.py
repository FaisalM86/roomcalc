import json
from sqlalchemy.exc import IntegrityError
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from markupsafe import Markup
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from data_access import create_session, get_project_by_id, get_all_projects
from forms import RegistrationForm, LoginForm, ProjectForm, RoomForm
from models import User, Room, WallData, Project
from auth import authenticate_user, authorize_user
from project_management import create_project, delete_project, update_project
from reporting import generate_summary_report, generate_heat_load_list, generate_detailed_report

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
csrf = CSRFProtect(app)


@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())


@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf())


@app.route('/')
def index():
    return render_template('index.html')

@app.template_filter('tojson')
def to_json(value):
    return Markup(json.dumps(value))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        session_db = create_session()
        try:
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
            new_user = User(username=form.username.data, password=hashed_password, access_level=1)
            session_db.add(new_user)
            session_db.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            session_db.rollback()
            flash('Username already exists. Please choose a different one.', 'danger')
        except Exception as e:
            session_db.rollback()
            flash('An error occurred. Please try again.', 'danger')
        finally:
            session_db.close()
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session_db = create_session()  # Rename to avoid conflict with Flask session
        user = session_db.query(User).filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id  # Correctly assigning user_id to the session
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))

    session_db = create_session()  # Create a new session for database operations
    user = session_db.query(User).filter_by(id=session['user_id']).first()

    if not user or not authorize_user(user.username,
                                      required_access_level=1):  # Ensure required access level is provided
        session_db.close()
        flash('You do not have the required permissions to access this page.', 'danger')
        return redirect(url_for('login'))

    # Fetch projects with their associated rooms
    projects = session_db.query(Project).options(joinedload(Project.rooms)).all()

    # Convert projects to a list of dictionaries
    projects_data = []
    for project in projects:
        project_dict = project.__dict__.copy()
        project_dict.pop('_sa_instance_state', None)  # Remove SQLAlchemy internal state
        project_dict['rooms'] = [room.__dict__.copy() for room in project.rooms]
        for room in project_dict['rooms']:
            room.pop('_sa_instance_state', None)
        projects_data.append(project_dict)

    session_db.close()

    # Pass the projects data as a JSON string
    return render_template('dashboard.html', projects=projects_data)


@app.route('/project/new', methods=['GET', 'POST'])
def new_project():
    """ Route to create a new project. """
    form = ProjectForm(request.form)
    if request.method == 'POST' and form.validate():
        create_project(form.data)
        flash('Project created successfully!')
        return redirect(url_for('dashboard'))
    return render_template('project_form.html', form=form)


@app.route('/project/<int:project_id>/edit', methods=['GET', 'POST'])
def edit_project(project_id):
    session_db = create_session()
    project = session_db.query(Project).filter_by(ProjectID=project_id).first()

    if not project:
        flash('Project not found.', 'danger')
        return redirect(url_for('dashboard'))

    form = ProjectForm(request.form, obj=project)
    if request.method == 'POST' and form.validate():
        project.ProjectName = form.ProjectName.data
        project.Client = form.Client.data
        project.Contract = form.Contract.data
        project.SubContractor = form.SubContractor.data
        project.DocumentNumber = form.DocumentNumber.data
        project.Revision = form.Revision.data
        project.RevisionDate = form.RevisionDate.data
        project.AmbientTempSummer = form.AmbientTempSummer.data
        project.AmbientTempWinter = form.AmbientTempWinter.data
        project.DefaultUValue = form.DefaultUValue.data
        project.Density = form.Density.data
        project.HeatCapacity = form.HeatCapacity.data
        session_db.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('project_form.html', form=form, project=project)


@app.route('/project/<int:project_id>/delete', methods=['POST'])
def delete_project(project_id):
    session_db = create_session()
    project = session_db.query(Project).filter_by(ProjectID=project_id).first()
    if project:
        session_db.delete(project)
        session_db.commit()
        flash('Project deleted successfully!', 'success')
    else:
        flash('Project not found.', 'danger')
    session_db.close()
    return redirect(url_for('dashboard'))


@app.route('/project/<int:project_id>/report')
def project_report(project_id):
    """ Route to generate reports for a project. """
    summary = generate_summary_report(project_id)
    heat_load_list = generate_heat_load_list(project_id)
    detailed_report = generate_detailed_report(project_id)
    return render_template('report.html', summary=summary, heat_load_list=heat_load_list,
                           detailed_report=detailed_report)


#-----------------------Room-----------------------------------


@app.route('/project/<int:project_id>/room/new', methods=['GET', 'POST'])
def new_room(project_id):
    form = RoomForm()


    if request.method == 'POST':
        logging.info(f"Received POST request for new room in project {project_id}")
        logging.debug(f"Form data: {request.form}")

        if form.validate_on_submit():
            logging.info("Form validation successful")
            session_db = create_session()
            try:
                new_room = Room(
                    ProjectID=project_id,
                    LocationNo=form.LocationNo.data,
                    RoomName=form.RoomName.data,
                    Elevation=form.Elevation.data,
                    Height=form.Height.data,
                    MinVentilationPerPerson=form.MinVentilationPerPerson.data,
                    MinVentilationPerArea=form.MinVentilationPerArea.data,
                    MinAirChangeRate=form.MinAirChangeRate.data,
                    Occupancy=form.Occupancy.data,
                    Remarks=form.Remarks.data
                )
                session_db.add(new_room)
                session_db.flush()  # This assigns an ID to new_room

                # Add walls and create wall data array
                wall_data = []
                for wall_form in form.walls:
                    new_wall = WallData(
                        RoomID=new_room.RoomID,
                        Length=wall_form.Length.data,
                        Angle=wall_form.Angle.data
                    )
                    session_db.add(new_wall)
                    wall_data.append((wall_form.Length.data, wall_form.Angle.data))

                session_db.commit()
                logging.info("Successfully committed new room to database")
                flash('Room and its walls created successfully!', 'success')
                return redirect(url_for('heat_gain', room_id=new_room.RoomID))
            except Exception as e:
                session_db.rollback()
                logging.error(f"Error occurred while creating room: {str(e)}")
                flash(f'An error occurred: {str(e)}', 'error')
            finally:
                session_db.close()
        else:
            logging.warning("Form validation failed")
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in {getattr(form, field).label.text}: {error}", 'error')
                    logging.warning(f"Validation error in {field}: {error}")

    return render_template('room_form.html', form=form, project_id=project_id)


@app.route('/room/<int:room_id>/edit', methods=['GET', 'POST'])
def edit_room(room_id):
    app.logger.info(f"Received request to edit room {room_id}")

    app.logger.debug(f"Request method: {request.method}")
    app.logger.debug(f"Form data: {request.form}")
    session_db = create_session()
    room = session_db.query(Room).filter_by(RoomID=room_id).first()
    project = session_db.query(Project).filter_by(ProjectID=room.ProjectID).first()

    if not room:
        flash('Room not found', 'error')
        return redirect(url_for('dashboard'))

    form = RoomForm(obj=room)


    if request.method == 'GET':
        # Populate form with existing walls
        while len(form.walls) > 0:
            form.walls.pop_entry()
        for wall in room.walls:
            form.walls.append_entry({
                'WallID': wall.WallID,
                'Length': wall.Length,
                'Angle': wall.Angle if wall.Angle is not None else 0
            })

    if form.validate_on_submit():
        try:
            # Update room properties
            form.populate_obj(room)

            # Process walls
            existing_wall_ids = set(wall.WallID for wall in room.walls)
            updated_wall_ids = set()
            wall_data = []

            for wall_form in form.walls:
                wall_id = wall_form.WallID.data

                if wall_id and wall_id in existing_wall_ids:
                    # Update existing wall
                    wall = next(wall for wall in room.walls if wall.WallID == wall_id)
                    wall.Length = wall_form.Length.data
                    wall.Angle = wall_form.Angle.data
                    updated_wall_ids.add(wall_id)
                else:
                    # Add new wall
                    new_wall = WallData(
                        RoomID=room.RoomID,
                        Length=wall_form.Length.data,
                        Angle=wall_form.Angle.data
                    )
                    session_db.add(new_wall)
                    room.walls.append(new_wall)
                wall_data.append((wall_form.Length.data, wall_form.Angle.data))

            # Remove walls that were not updated or added
            room.walls = [wall for wall in room.walls if wall.WallID in updated_wall_ids or wall.WallID is None]



            session_db.commit()
            flash('Room and its walls updated successfully!', 'success')
            return redirect(url_for('heat_gain', room_id=room.RoomID))
        except Exception as e:
            session_db.rollback()
            flash(f'An error occurred: {str(e)}', 'error')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'error')

    return render_template('room_form.html', form=form, room=room)



@app.route('/room/<int:room_id>/delete', methods=['POST'])
def delete_room(room_id):
    session_db = create_session()
    room = session_db.query(Room).filter_by(RoomID=room_id).first()
    if room:
        try:
            session_db.delete(room)
            session_db.commit()
            return jsonify({"status": "success", "message": "Room deleted successfully!"})
        except Exception as e:
            session_db.rollback()
            return jsonify({"status": "error", "message": f"An error occurred: {str(e)}"}), 400
        finally:
            session_db.close()
    return jsonify({"status": "error", "message": "Room not found!"}), 404



@app.route('/room/<int:room_id>/report')
def room_report(room_id):
    # Code to generate room report
    return render_template('room_report.html', room_id=room_id)


# Heat gain
def safe_float(value, default=0.0):
    try:
        return float(value) if value.strip() else default
    except (ValueError, AttributeError):
        return default

@app.route('/heat_gain/<int:room_id>', methods=['GET', 'POST'])
def heat_gain(room_id):
    session_db = create_session()
    try:
        room = session_db.query(Room).filter_by(RoomID=room_id).first()
        if not room:
            flash('Room not found.', 'danger')
            return redirect(url_for('dashboard'))

        project = session_db.query(Project).filter_by(ProjectID=room.ProjectID).first()
        if not project:
            flash('Project not found.', 'danger')
            return redirect(url_for('dashboard'))

        supply_systems = session_db.query(SupplySystem).all()
        supply_systems_data = {system.SystemNo: {
            'TempSupplySummer': system.TempSupplySummer,
            'TempSupplyWinter': system.TempSupplyWinter
        } for system in supply_systems}

        roof_area = room.FloorArea
        floor_area = room.FloorArea
        required_airflow = room.RequiredAirflow or 1
        roof_u_value = project.DefaultUValue
        floor_u_value = project.DefaultUValue
        walls = session_db.query(WallData).filter_by(RoomID=room_id).all()
        height = room.Height
        airflow = room.RequiredAirflow





        return render_template('heat_gain.html',
                               supply_systems=supply_systems,
                               roof_area=roof_area,
                               floor_area=floor_area,
                               roof_u_value=roof_u_value,
                               floor_u_value=floor_u_value,
                               walls=walls,
                               ambient_temp_summer=project.AmbientTempSummer,
                               ambient_temp_winter=project.AmbientTempWinter,
                               room=room,
                               height=height,
                               project=project,
                               density=project.Density,
                               heat_capacity=project.HeatCapacity,
                               required_airflow=required_airflow,
                               supply_systems_data=supply_systems_data,
                                airflow=airflow,
                               csrf_token=generate_csrf())
    except Exception as e:
        flash('An error occurred: {}'.format(e), 'danger')
        return redirect(url_for('dashboard'))
    finally:
        session_db.close()


#--Supply system
from forms import SupplySystemForm
from models import SupplySystem

@app.route('/supply_systems', methods=['GET', 'POST'])
def supply_systems():
    app.logger.info('Received request to view supply systems')
    form = SupplySystemForm()
    session_db = create_session()

    if request.method == 'POST':
        app.logger.info('POST request received')
        app.logger.info(f'Form data: {request.form}')

    if form.validate_on_submit():
        app.logger.info('Form validated successfully')
        new_system = SupplySystem(
            SystemNo=form.SystemNo.data,
            SystemName=form.SystemName.data,
            TempSupplyWinter=form.TempSupplyWinter.data,
            TempSupplySummer=form.TempSupplySummer.data,
            CoolingEnthalpy=form.CoolingEnthalpy.data,
            FanHeat=form.FanHeat.data
        )
        session_db.add(new_system)
        session_db.commit()
        app.logger.info('Supply system added successfully')
        flash('System added successfully!', 'success')
        session_db.close()
        return redirect(url_for('supply_systems'))
    else:
        app.logger.warning('Form validation failed')
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'error')
                app.logger.warning(f"Validation error in {field}: {error}")

    systems = session_db.query(SupplySystem).all()
    session_db.close()
    return render_template('supply_systems.html', form=form, systems=systems)

@app.route('/delete_system/<int:system_id>', methods=['POST'])
def delete_system(system_id):
    session_db = create_session()
    system = session_db.query(SupplySystem).get(system_id)
    if system:
        session_db.delete(system)
        session_db.commit()
        flash('System deleted successfully!', 'success')
    session_db.close()
    return redirect(url_for('supply_systems'))

if __name__ == '__main__':
    from models import Base
    from sqlalchemy import create_engine
    from config import DATABASE_PATH

    engine = create_engine(f"sqlite:///{DATABASE_PATH}")
    Base.metadata.create_all(engine)


    app.run(debug=True)

import json
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash, check_password_hash
from data_access import create_session, get_project_by_id, get_all_projects
from forms import RegistrationForm, LoginForm, ProjectForm, RoomForm
from models import User, Room, WallData, Project
from auth import authenticate_user, authorize_user
from project_management import create_project, delete_project, update_project
from reporting import generate_summary_report, generate_heat_load_list, generate_detailed_report
from calculations import calculate_room_parameters
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
csrf = CSRFProtect(app)

@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        session_db = create_session()  # Rename to avoid conflict with Flask session
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password, access_level=1)  # Default access level
        session_db.add(new_user)
        session_db.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
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

    if not user or not authorize_user(user.username, required_access_level=1):  # Ensure required access level is provided
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

@app.route('/project/<int:project_id>/room/new', methods=['GET', 'POST'])
def new_room(project_id):
    form = RoomForm()
    if form.validate_on_submit():
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
                Volume=form.Volume.data,
                FloorArea=form.Area.data,
                Occupancy=form.Occupancy.data,
                RequiredAirflow=form.RequiredAirflow.data,
                Remarks=form.Remarks.data
            )
            session_db.add(new_room)
            session_db.commit()

            for wall_form in form.walls.entries:
                new_wall = WallData(
                    RoomID=new_room.RoomID,
                    Length=wall_form.data['Length'],
                    Angle=wall_form.data['Angle']
                )
                session_db.add(new_wall)

            session_db.commit()
            flash('Room and its walls created successfully!')
            return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"Error creating room: {e}")  # Debugging line
            session_db.rollback()
        finally:
            session_db.close()
    else:
        print("Form validation failed.")
        print(form.errors)  # Debugging line
    return render_template('room_form.html', form=form)



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
    return render_template('report.html', summary=summary, heat_load_list=heat_load_list, detailed_report=detailed_report)

@app.route('/room/<int:room_id>/edit', methods=['GET', 'POST'])
def edit_room(room_id):
    session_db = create_session()
    room = session_db.query(Room).filter_by(RoomID=room_id).first()
    form = RoomForm(obj=room)

    if form.validate_on_submit():
        # Update room properties
        form.populate_obj(room)

        # Process walls
        existing_wall_ids = set(wall.WallID for wall in room.walls)
        updated_wall_ids = set()

        for wall_form in form.walls.entries:
            wall_id = wall_form.form.WallID.data

            # Check if the wall is marked for removal
            if request.form.get(f'walls-{wall_form.form.WallID.data}-removed') != 'true':
                if wall_id and wall_id in existing_wall_ids:
                    # Update existing wall
                    wall = session_db.query(WallData).get(wall_id)
                    wall.Length = wall_form.form.Length.data
                    wall.Angle = wall_form.form.Angle.data
                    updated_wall_ids.add(wall_id)
                else:
                    # Add new wall
                    new_wall = WallData(
                        RoomID=room.RoomID,
                        Length=wall_form.form.Length.data,
                        Angle=wall_form.form.Angle.data
                    )
                    session_db.add(new_wall)

        # Remove walls that were not updated or added
        for wall_id in existing_wall_ids - updated_wall_ids:
            wall_to_remove = session_db.query(WallData).get(wall_id)
            session_db.delete(wall_to_remove)

        # Recalculate room properties
        updated_walls = [wall for wall in room.walls if wall.WallID in updated_wall_ids] + \
                        [wall for wall in session_db.new if isinstance(wall, WallData) and wall.RoomID == room.RoomID]

        if len(updated_walls) >= 2:
            room.FloorArea = updated_walls[0].Length * updated_walls[1].Length
        else:
            room.FloorArea = 0

        room.Volume = room.FloorArea * room.Height
        room.RequiredAirflow = room.Volume * room.MinAirChangeRate

        session_db.commit()
        flash('Room and its walls updated successfully!')
        return redirect(url_for('dashboard'))

    return render_template('room_form.html', form=form, room=room)


@app.route('/room/<int:room_id>/delete', methods=['POST'])
def delete_room(room_id):
    session_db = create_session()
    room = session_db.query(Room).filter_by(RoomID=room_id).first()
    session_db.delete(room)
    session_db.commit()
    flash('Room deleted successfully!')
    return redirect(url_for('dashboard'))

@app.route('/room/<int:room_id>/report')
def room_report(room_id):
    # Code to generate room report
    return render_template('room_report.html', room_id=room_id)


# Heat gain

@app.route('/heat_gain/<int:room_id>', methods=['GET', 'POST'])
def heat_gain(room_id):
    session_db = create_session()
    room = session_db.query(Room).filter_by(RoomID=room_id).first()
    project = session_db.query(Project).filter_by(ProjectID=room.ProjectID).first()


    if not room:
        flash('Room not found.', 'danger')
        return redirect(url_for('dashboard'))

    roof_area = room.FloorArea
    floor_area = room.FloorArea
    roof_u_value =project.DefaultUValue
    floor_u_value = project.DefaultUValue
    height = room.Height

    # Fetch wall data
    walls = session_db.query(WallData).filter_by(RoomID=room_id).all()



    return render_template('heat_gain.html', roof_area=roof_area,
                           floor_area=floor_area,roof_u_value=roof_u_value,
                           floor_u_value=floor_u_value, walls=walls, height=height)
if __name__ == '__main__':
    from models import Base
    from sqlalchemy import create_engine
    from config import DATABASE_PATH

    engine = create_engine(f"sqlite:///{DATABASE_PATH}")
    Base.metadata.create_all(engine)

    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))

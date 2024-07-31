
# forms.py
# Form handling for the RoomCalc application using Flask-WTF

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField, SelectField, TextAreaField,PasswordField,SubmitField
from wtforms.fields.form import FormField
from wtforms.fields.list import FieldList
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired, Optional, NumberRange, EqualTo, Length, InputRequired


class ProjectForm(FlaskForm):
    ProjectID = HiddenField('ProjectID')
    ProjectName = StringField('Project Name', validators=[DataRequired()])
    Client = StringField('Client', validators=[Optional()])
    Contract = StringField('Contract', validators=[Optional()])
    SubContractor = StringField('SubContractor', validators=[Optional()])
    DocumentNumber = StringField('Document Number', validators=[Optional()])
    Revision = StringField('Revision', validators=[Optional()])
    RevisionDate = StringField('Revision Date', validators=[Optional()])
    AmbientTempSummer = FloatField('Ambient Temperature Summer', validators=[DataRequired()])
    AmbientTempWinter = FloatField('Ambient Temperature Winter', validators=[DataRequired()])
    DefaultUValue = FloatField('Default U-Value', validators=[DataRequired()])
    Density = FloatField('Density', validators=[DataRequired()])
    HeatCapacity = FloatField('Heat Capacity', validators=[DataRequired()])
    submit = SubmitField('Save')

class WallForm(FlaskForm):
    WallID = HiddenField()
    Length = FloatField('Length (m)')
    Angle = FloatField('Angle (°)')

class RoomForm(FlaskForm):
    LocationNo = StringField('Location No', validators=[InputRequired()])
    RoomName = StringField('Room Name', validators=[InputRequired()])
    Elevation = FloatField('Elevation', validators=[DataRequired()])
    Height = FloatField('Height (Meters)', validators=[DataRequired()])
    MinVentilationPerPerson = FloatField('Min Ventilation Per Person (l/s)', validators=[DataRequired()])
    MinVentilationPerArea = FloatField('Min Ventilation Per Area (l/sm\u00B2)', validators=[DataRequired()])
    MinAirChangeRate = FloatField('Min Air Change Rate (ac/h)', validators=[DataRequired()])
    Volume = FloatField('Volume (m\u00B3)', render_kw={'readonly': True})
    Area = FloatField('Floor Area (m\u00B2)', render_kw={'readonly': True})
    Occupancy = FloatField('No of People', validators=[InputRequired()])
    RequiredAirflow = FloatField('Minimum Airflow (m\u00B3/h)', render_kw={'readonly': True})
    MinimumAirFlow = FloatField('Minimum Airflow (m\u00B3/h)', render_kw={'readonly': True})
    Remarks = StringField('Remarks')
    walls = FieldList(FormField(WallForm))
    submit = SubmitField('Save & Next')

class SurfaceForm(FlaskForm):
    SurfaceType = SelectField('Surface Type', choices=[('Wall', 'Wall'), ('Roof', 'Roof'), ('Floor', 'Floor')], validators=[DataRequired()])
    Area = FloatField('Area', validators=[DataRequired()])
    UValue = FloatField('U-Value', validators=[DataRequired()])
    TemperatureOther = FloatField('Temperature Other Side', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SupplySystemForm(FlaskForm):
    SystemNo = StringField('System Number', validators=[InputRequired()])
    SystemName = StringField('System Name', validators=[InputRequired()])
    TempSupplyWinter = FloatField('Supply Temperature Winter', validators=[DataRequired()])
    TempSupplySummer = FloatField('Supply Temperature Summer', validators=[InputRequired()])
    CoolingEnthalpy = FloatField('DeltaH', validators=[InputRequired()])
    FanHeat = FloatField('Fan Heat', validators=[InputRequired()])
    submit = SubmitField('Save')

class LightForm(FlaskForm):
    LightDescription = StringField('Light Description', validators=[DataRequired()])
    HeatLoadSummer = FloatField('Heat Load Summer', validators=[DataRequired()])
    HeatLoadWinter = FloatField('Heat Load Winter', validators=[DataRequired()])
    ApplySummer = SelectField('Apply in Summer', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    ApplyWinter = SelectField('Apply in Winter', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class PersonnelForm(FlaskForm):
    Quantity = IntegerField('Quantity', validators=[DataRequired()])
    HeatLoadPerPersonSummer = FloatField('Heat Load per Person Summer', validators=[DataRequired()])
    HeatLoadPerPersonWinter = FloatField('Heat Load per Person Winter', validators=[DataRequired()])
    ApplySummer = SelectField('Apply in Summer', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    ApplyWinter = SelectField('Apply in Winter', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class EquipmentForm(FlaskForm):
    EquipmentDescription = StringField('Equipment Description', validators=[DataRequired()])
    HeatLoadSummer = FloatField('Heat Load Summer', validators=[DataRequired()])
    HeatLoadWinter = FloatField('Heat Load Winter', validators=[DataRequired()])
    ApplySummer = SelectField('Apply in Summer', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    access_level = SelectField('Access Level', choices=[(1, 'User'), (2, 'Admin')], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Sign Up')
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
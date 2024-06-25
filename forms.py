
# forms.py
# Form handling for the RoomCalc application using Flask-WTF

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField, SelectField, TextAreaField,PasswordField,SubmitField
from wtforms.fields.form import FormField
from wtforms.fields.list import FieldList
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired, Optional, NumberRange,EqualTo,Length




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
    Length = FloatField('Length (m)', validators=[DataRequired()])
    Angle = FloatField('Angle (°)', validators=[Optional()])

class RoomForm(FlaskForm):
    LocationNo = StringField('Location No', validators=[DataRequired()])
    RoomName = StringField('Room Name', validators=[DataRequired()])
    Elevation = FloatField('Elevation (meters)', validators=[DataRequired()])
    Height = FloatField('Height (meters)', validators=[DataRequired()])
    MinVentilationPerPerson = FloatField('Minimum Ventilation per Person (l/s)', validators=[DataRequired()])
    MinVentilationPerArea = FloatField('Minimum Ventilation per Area (l/sm²)', validators=[Optional()])
    MinAirChangeRate = FloatField('Minimum Air Change Rate (ac/h)', validators=[DataRequired()])
    Volume = FloatField('Volume (m³)', validators=[DataRequired()])
    Area = FloatField('Floor Area (m²)', validators=[DataRequired()])
    Occupancy = IntegerField('Number of Persons', validators=[Optional()])
    RequiredAirflow = FloatField('Minimum Airflow (m³/h)', validators=[DataRequired()])
    Remarks = TextAreaField('Remarks')
    walls = FieldList(FormField(WallForm), min_entries=1, max_entries=10)
    submit = SubmitField('Save')

class SurfaceForm(FlaskForm):
    SurfaceType = SelectField('Surface Type', choices=[('Wall', 'Wall'), ('Roof', 'Roof'), ('Floor', 'Floor')], validators=[DataRequired()])
    Area = FloatField('Area', validators=[DataRequired()])
    UValue = FloatField('U-Value', validators=[DataRequired()])
    TemperatureOther = FloatField('Temperature Other Side', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SupplySystemForm(FlaskForm):
    SystemNo = StringField('System Number', validators=[DataRequired()])
    SystemName = StringField('System Name', validators=[DataRequired()])
    TempSupplyWinter = FloatField('Supply Temperature Winter', validators=[DataRequired()])
    TempSupplySummer = FloatField('Supply Temperature Summer', validators=[DataRequired()])
    CoolingEnthalpy = FloatField('Cooling Enthalpy', validators=[DataRequired()])
    FanHeat = FloatField('Fan Heat', validators=[DataRequired()])
    submit = SubmitField('Submit')

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
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
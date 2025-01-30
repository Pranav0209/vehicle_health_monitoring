from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from datetime import datetime

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Full Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    pincode = StringField('PIN Code', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Register')

class VehicleRegistrationForm(FlaskForm):
    registration_number = StringField('Vehicle Registration Number', validators=[DataRequired()])
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    year = IntegerField('Year of Manufacture', validators=[DataRequired()])
    fuel_type = SelectField('Fuel Type', choices=[
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('cng', 'CNG'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid')
    ])
    current_mileage = IntegerField('Current Mileage (km)', validators=[DataRequired()])
    service_interval_km = IntegerField('Service Interval (km)', validators=[DataRequired()])
    last_service_date = DateField('Last Service Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Register Vehicle')

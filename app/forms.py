from flask_wtf import FlaskForm
from wtforms import StringField,FloatField,TextAreaField,SubmitField,PasswordField

from wtforms.validators import DataRequired,NumberRange,Length

class EnquiryForm(FlaskForm):
    name=StringField("Name",validators=[DataRequired(),Length(max=120)])
   
    contact=StringField("Contact No:",validators=[DataRequired(),Length(min=7,max=20)])
    pickup_location=StringField("Pickup Location",validators=[DataRequired(),Length( max=200)])
    drop_location=StringField("Destination",validators=[DataRequired(),Length( max=200)])
    weight=FloatField("Weight",validators=[DataRequired(),NumberRange(min=0.1)])
    parcel_details=TextAreaField("ParcelDetails",validators=[DataRequired()])
    submit = SubmitField("Submit Enquiry")
class TrackForm(FlaskForm):
    tracking_id=StringField("Tracking ID",validators=[DataRequired()])

    submit = SubmitField("Track")
class LoginForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Submit Login")
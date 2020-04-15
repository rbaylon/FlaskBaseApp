from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, HiddenField
from wtforms.validators import InputRequired, Length
from wtforms_components import DateField
from datetime import date

class LteForm(FlaskForm):
    input = IntegerField('Input Count', validators=[InputRequired()])
    archive = IntegerField('Archive Count', validators=[InputRequired()])
    error = IntegerField('Error Count', validators=[InputRequired()])
    drop = IntegerField('Drop Count', validators=[InputRequired()])
    location = SelectField('Location', choices=[('lsdc', 'LSDC'),('reston','Reston'),('other','Other')])
    rdate = DateField('Date',default=date.today(), format="%Y-%m-%d")
    delete = HiddenField('Delete', default='N', validators=[Length(max=1)])    

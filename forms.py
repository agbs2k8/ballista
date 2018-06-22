from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired

from ballista.models import Caliber, User, Rifle


class LoginForm(Form):
    username = StringField('Your Username:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class AddRifleForm(Form):
    name = StringField('Rifle Name', validators=[DataRequired()])
    barrel_length = FloatField('Barrel Length', validators=[DataRequired()])
    caliber = SelectField('Caliber', validators=[DataRequired()],
                          choices=[(c.id, c.caliber_name) for c in Caliber.query.order_by(Caliber.id)])

    def validate(self):
        return True


#class SelectRifleForm(Form):
#    rifle = SelectField('Rifle', validators=[DataRequired()],
#                        choices=[(r.id, r.name) for r in User.rifles])
#
#    def validate(self):
#        return True

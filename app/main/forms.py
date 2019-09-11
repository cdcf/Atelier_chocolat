from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    first_name = StringField('Prénom', validators=[DataRequired()])
    second_name = StringField('Nom', validators=[DataRequired()])
    about_me = TextAreaField('A propos de moi', validators=[Length(min=0, max=256)])
    submit = SubmitField('Enregistrer')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Veuillez utiliser un nom d\'utilisateur différent.')

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    RadioField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    widgets,
)
from wtforms.validators import DataRequired
import operator

sections = [
    ('', "---"),
    ('BA - Philosophie', "Philosophie"),
    ('BA - Histoire', "Histoire"),
    ('BA - Français moderne', "Français moderne"),
    ('BA - Français médiéval', "Français médiéval"),
    ('BA - Archéologie', "Archéologie"),
    ('BA - Histoire ancienne', "Histoire ancienne"),
    ('BA - Latin', "Latin"),
    ('BA - Grec ancien', "Grec ancien"),
    ('BA - Italien', "Italien"),
    ('BA - Espagnol', "Espagnol"),
    ('BA - Allemand', "Allemand"),
    ('BA - Anglais', "Anglais"),
    ('BA - Etudes slaves', "Langues et civilisation slaves"),
    ("BA - Langues et civilisations d'Asie du Sud", "Langues et civilisation d'Asie du Sud"),
    ('BA - Histoire et sciences des religions', "Histoire et sciences des religions"),
    ('BA - Linguistique', "Linguistique"),
    ("BA - Histoire de l'art", "Histoire de l'art"),
    ('BA - Cinéma', "Histoire et esthétique du cinéma"),
    ('BA - Informatique pour les sciences humaines', "Informatique pour les sciences humaines"),
    ('BA - Français langue étrangère', "Français langue étrangère"),
    ('BA - Géographie', "Géographie"),
    ('BA - Science politique (mineure en SSP)', "Science politique"),
    ('BA - Psychologie (mineure en SSP)', "Psychologie"),
    ('BA - Sciences sociales (mineure en SSP)', "Science sociales"),
    ('BA - Etudes théologiques', "Études théologiques"),
]

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ClassesForm(FlaskForm):
    year = RadioField("Choisir l'année", choices=[('propédeutique', "Propédeutique"), ('2ème', "2ème partie")])
    semester = RadioField('Choisir le semestre', choices=[('Automne', "Automne"), ('Printemps', "Printemps")])
    section1 = SelectField('Choisir la section 1', choices=sorted(sections, key=operator.itemgetter(1)))
    section2 = SelectField('Choisir la section 2', choices=sorted(sections, key=operator.itemgetter(1)))
    section3 = SelectField('Choisir la section 3', choices=sorted(sections, key=operator.itemgetter(1)))
    submit = SubmitField('Valider')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag='ul', prefix_label=False)
    option_widget = widgets.CheckboxInput()

    # Overriding the built-in validation to accept dynamic choices added by the user
    def pre_validate(self, form):
        pass


class ListForm(FlaskForm):
    selection1 = MultiCheckboxField('Choisir les cours pour la section 1', choices=[])
    selection2 = MultiCheckboxField('Choisir les cours pour la section 2', choices=[])
    selection3 = MultiCheckboxField('Choisir les cours pour la section 3', choices=[])
    submit = SubmitField('Valider la liste de cours')


class SimpleForm(FlaskForm):
    string_of_files = ['one\r\ntwo\r\nthree\r\n']
    list_of_files = string_of_files[0].split()
    # create a list of value/description tuples
    files = [(x, x) for x in list_of_files]
    example = MultiCheckboxField('Label', choices=files)

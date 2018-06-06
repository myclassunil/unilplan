from flask import Flask, render_template, request, redirect, url_for
from app import app
from pymongo import MongoClient
from bson.objectid import ObjectId
from ChoiceResultsController import choice_user_controller
from DbHandler import list_classes_generator, filter_classes_by_year
from app.forms import ClassesForm, ListForm, SimpleForm
import json

# client = MongoClient()
# db = client.db_unilplan

DB_NAME = "unilplan"
DB_HOST = "ds147469.mlab.com"
DB_PORT = 47469
DB_USER = "Turing"
DB_PASS = "turing"

connection = MongoClient(DB_HOST, DB_PORT)
db = connection[DB_NAME]
db.authenticate(DB_USER, DB_PASS)
classes = db.classes
classesDB = classes.find()
list_classes = list_classes_generator(classesDB)

list_classes_test = [
    {
        #'id': ObjectId('5b0c9cc20f31871480f3c615'),
        'Section': "BA - Histoire de l'art",
        'Name': "Proséminaire en histoire de l'art contemporain - BA-HART-1-102030",
        'Teacher': 'Wagen-Magnon Samuel',
        'CourseType': 'C/TP',
        'Location': 'Anthropole/4173 - Argand',
        'Semester': 'Automne',
        'Time': '10:15 12:00',
        'TimeStart': '10:15',
        'TimeEnd': '12:00',
        'Day': 'Lundi',
        'Year': 'propédeutique',
        'day_idx': 1,
        'event': 'event-1',
    },
    {
        #'id': ObjectId('5b0c9cc20f31871480f3c618'),
        'Section': "BA - Histoire de l'art",
        'Name': "Proséminaire en histoire de l'art moderne - BA-HART-1-102020 ",
        'Teacher': 'Dutoit Geneviève<br>Menal Sibylle',
        'CourseType': 'C/TP',
        'Location': 'Anthropole/3174',
        'Semester': 'Automne',
        'Time': '13:15 15:00',
        'TimeStart': '13:15',
        'TimeEnd': '15:00',
        'Day': 'Mardi',
        'Year': 'propédeutique',
        'day_idx': 2,
        'event': 'event-1',
    },
    {
        #'id': ObjectId('5b0c9cc20f31871480f3c787'),
        'Section': 'BA - Italien',
        'Name': 'Lingua e linguistica italiana : espressione scritta - BA-ITA-1-1010 ',
        'Teacher': 'Lala Letizia',
        'CourseType': 'C/S',
        'Location': 'Anthropole/4078',
        'Semester': 'Automne',
        'Time': '15:15 17:00',
        'TimeStart': '15:15',
        'TimeEnd': '17:00',
        'Day': 'Mercredi',
        'Year': 'propédeutique',
        'day_idx': 3,
        'event': 'event-2',
    },
]


@app.route('/', methods=['post', 'get'])
def home():
    valid_form = False
    is_section1 = False
    is_section2 = False
    is_section3 = False
    overlap = False
    form = ClassesForm()
    list_form = ListForm()

    if form.validate_on_submit():
        # Used to activate the if valid_form clause in base.html
        valid_form = True

        # Get the data of the form submitted by the user
        year_data = form.year.data
        semester_data = form.semester.data
        section1_data = form.section1.data
        section2_data = form.section2.data
        section3_data = form.section3.data
        print(year_data, semester_data, section1_data, section2_data)

        # Filter the list of classes according to the choices of the user in the form
        list_classes_filtered1 = choice_user_controller(list_classes, year_data, semester_data, section1_data)
        list_classes_filtered2 = choice_user_controller(list_classes, year_data, semester_data, section2_data)
        list_classes_filtered3 = choice_user_controller(list_classes, year_data, semester_data, section3_data)

        # Create the list of classes the user can chose from for the section 1 and 2
        if section1_data:
            is_section1 = True
            list_form.selection1.label = "Choisir les cours en " + section1_data
            list_form.selection1.choices = [
                (item['id'],
                 "<span class=\"time-of-class\">" + item['Day'] + " | " +
                 item['TimeStart'] + "-" + item['TimeEnd'] + "</span><br>" +
                 "<span class=\"name-of-class\">" + item['Name'] + "</span><br>" +
                 "<span class=\"teacher-of-class\">" + item['Teacher'] + "</span>") for item in list_classes_filtered1
            ]
            print(list_form.selection1.choices)
        if section2_data:
            is_section2 = True
            list_form.selection2.label = "Choisir les cours en " + section2_data
            list_form.selection2.choices = [
                (item['id'],
                 "<span class=\"time-of-class\">" + item['Day'] + " | " +
                 item['TimeStart'] + "-" + item['TimeEnd'] + "</span><br>" +
                 "<span class=\"name-of-class\">" + item['Name'] + "</span><br>" +
                 "<span class=\"teacher-of-class\">" + item['Teacher'] + "</span>") for item in list_classes_filtered2
            ]
        if section3_data:
            is_section3 = True
            list_form.selection3.label = "Choisir les cours en " + section3_data
            list_form.selection3.choices = [
                (item['id'],
                 "<span class=\"time-of-class\">" + item['Day'] + " | " +
                 item['TimeStart'] + "-" + item['TimeEnd'] + "</span><br>" +
                 "<span class=\"name-of-class\">" + item['Name'] + "</span><br>" +
                 "<span class=\"teacher-of-class\">" + item['Teacher'] + "</span>") for item in list_classes_filtered3
            ]

    else:
        print(form.errors)
        print("error in myform")

    # If the user has selected classes and submit it
    if list_form.validate_on_submit():
        print(list_form.selection1.data)
        print("list_form validate")
        list_classes_selected = []
        list_overlap = []

        # Puts the classes selected by the user in a list
        for item in list_classes:
            # The data retrieved from the list of classes is just the id of the class
            for classe_id in list_form.selection1.data:
                if str(item['id']) == str(classe_id):
                    # event-1 used to determine the category of the event in schedule.html
                    item['event'] = 'event-1'
                    list_classes_selected.append(item)
            for classe_id in list_form.selection2.data:
                if str(item['id']) == str(classe_id):
                    # event-2 used to determine the category of the event in schedule.html
                    item['event'] = 'event-2'
                    list_classes_selected.append(item)
            for classe_id in list_form.selection3.data:
                if str(item['id']) == str(classe_id):
                    # event-3 used to determine the category of the event in schedule.html
                    item['event'] = 'event-3'
                    list_classes_selected.append(item)

        # Checks if there is an overlap in the classes selected by the user
        if list_classes_selected:
            nbr_classes = len(list_classes_selected)
            idx1 = 0
            idx2 = 1

            while idx1 < nbr_classes-1:
                chevauchement = False
                classe1 = list_classes_selected[idx1]
                while idx2 < nbr_classes:
                    classe2= list_classes_selected[idx2]
                    # Checks if classes are on the same day and start at the same time or during one of the classes
                    if classe1['Day'] == classe2['Day'] and \
                            (classe1['TimeStart'] <= classe2['TimeStart'] < classe1['TimeEnd'] or
                            classe2['TimeStart'] <= classe1['TimeStart'] < classe2['TimeEnd']):
                        print("overlap True")
                        overlap = True
                        chevauchement = True
                    idx2 += 1
                # list-overlap used to display day and time of overlap in schedule.html
                if chevauchement:
                    list_overlap.append([classe1['Day'], classe1['TimeStart']])
                idx1 += 1
                idx2 = idx1+1

        print(list_classes_selected)

        if list_form.selection1.data or list_form.selection2.data or list_form.selection3.data:
            """
            return render_template(
                'schedule.html',
                list_classes=list_classes_selected,
                overlap_checker=overlap,
                overlap_info=list_overlap,
            )
            """
            print("list selected", list_classes_selected)

            i = 0
            while i < len(list_classes_selected):
                list_classes_selected[i]['id'] = "i+1"
                list_classes_selected[i]['HourStart'] = list_classes_selected[i]['TimeStart'][:2]
                list_classes_selected[i]['MinuteStart'] = list_classes_selected[i]['TimeStart'][-2:]
                list_classes_selected[i]['HourEnd'] = list_classes_selected[i]['TimeEnd'][:2]
                list_classes_selected[i]['MinuteEnd'] = list_classes_selected[i]['TimeEnd'][-2:]
                i += 1

            print("list selected update", list_classes_selected)

            return render_template('weekcalendar.html', list_classes=json.dumps(list_classes_selected))

    else:
        print(list_form.errors)
        print("error in list_form")

    return render_template(
        'index.html',
        myform=form,
        list_form=list_form,
        valid_form=valid_form,
        is_section1=is_section1,
        is_section2=is_section2,
        is_section3=is_section3,
    )

@app.route('/schedule')
def schedule():
    return render_template('schedule.html', list_classes=list_classes)

@app.route('/calendar')
def calendar():
    i = 0
    while i < len(list_classes_test):
        list_classes_test[i]['HourStart'] = list_classes_test[i]['TimeStart'][:2]
        list_classes_test[i]['MinuteStart'] = list_classes_test[i]['TimeStart'][-2:]
        list_classes_test[i]['HourEnd'] = list_classes_test[i]['TimeEnd'][:2]
        list_classes_test[i]['MinuteEnd'] = list_classes_test[i]['TimeEnd'][-2:]
        i += 1

    return render_template('weekcalendar.html', list_classes=json.dumps(list_classes_test))

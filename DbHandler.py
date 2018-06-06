import operator

# from app import db
# from app.models import Classes

list_classes = [
    {
        'name': "cours 01", 'semester': "sem2", 'section': "allemand", 'year': "prope", 'day': "mardi", 'day_idx': 2,
    },
    {
        'name': "cours 02", 'semester': "sem1", 'section': "français", 'year': "2e", 'day': "mercredi", 'day_idx': 3,
    },
    {
        'name': "cours 03", 'semester': "sem2", 'section': "allemand", 'year': "2e", 'day': "lundi", 'day_idx': 1,
    },
    {
        'name': "cours 04", 'semester': "sem2", 'section': "français", 'year': "2e", 'day': "lundi", 'day_idx': 1,
    },
    {
        'name': "cours 05", 'semester': "sem1", 'section': "allemand", 'year': "prope", 'day': "vendredi", 'day_idx': 5,
    },
]

semester = "sem2"
year = "2e"
section = "allemand"


def main():
    list_filtered = filter_classes_by_semester(list_classes, semester)
    print("----- semester -----", list_filtered)
    list_filtered = filter_classes_by_year(list_classes, year)
    print("----- year -----", list_filtered)
    list_filtered = filter_classes_by_section(list_classes, section)
    print("----- section -----", list_filtered)

def list_classes_generator(classesDB):
    """
    Converts the data stored in the database into a list of classes (list of dictionaries).
    Adds a "day_idx" key (1 for Monday, 2 for Tuesday, etc) in order to sort the list by day.
    """

    list_classes = []

    for item in classesDB:
        class_dict = {}
        class_dict['id'] = item['_id']
        class_dict['Section'] = item['Section']
        class_dict['Name'] = item['Name']
        class_dict['Teacher'] = item['Teacher']
        class_dict['CourseType'] = item['CourseType']
        class_dict['Location'] = item['Location']
        class_dict['Semester'] = item['Semester']
        class_dict['Time'] = item['Time']

        # Splits the time of classes in time of start and time of end
        time_list = item['Time'].split(" ")
        class_dict['TimeStart'] = time_list[0]
        class_dict['TimeEnd'] = time_list[1]

        # Checks if there is a day specified for the class. If not, specifying "Day not defined"
        if item['Day'] == "" and item['Time'] == "0:0</ 0</td":
            class_dict['Day'] = "Cours bloc"
            class_dict['Time'] = ""
            class_dict['TimeStart'] = ""
            class_dict['TimeEnd'] = ""
        elif item['Day'] == "":
            class_dict['Day'] = "[Jour non défini]"
        else:
            class_dict['Day'] = item['Day']

        # Only keeps the first word of year field (like 'propedeutique' and not 'propedeutique (2017 -&gt;)' in DB)
        year_list = item['Year'].split(" ")
        if year_list[0] == '2p' or year_list[0] == '2e':
            year_list[0] = "2ème"
        elif year_list[0] == 'propé' or year_list[0] == 'Propé':
            year_list[0] = "propédeutique"
        class_dict['Year'] = year_list[0]

        # Add an index corresponding to the day of the class to sort the list by day
        if item['Day'] == "Lundi":
            class_dict['day_idx'] = 1
        elif item['Day'] == "Mardi":
            class_dict['day_idx'] = 2
        elif item['Day'] == "Mercredi":
            class_dict['day_idx'] = 3
        elif item['Day'] == "Jeudi":
            class_dict['day_idx'] = 4
        elif item['Day'] == "Vendredi":
            class_dict['day_idx'] = 5
        else:
            class_dict['day_idx'] = 0

        list_classes.append(class_dict)

    return list_classes


def filter_classes_by_year(list_classes, year):
    """ Takes a list of classes and returns a new list of classes, that correspond to the year given as a parameter. """

    list_classes_by_year = []
    for item in list_classes:
        if item['Year'] == year:
            list_classes_by_year.append(item)

    list_classes_by_year = sorted(sorted(list_classes_by_year, key=operator.itemgetter('Time')), key=operator.itemgetter('day_idx'))
    return list_classes_by_year


def filter_classes_by_section(list_classes, section):
    """ Takes a list of classes and returns a new list of classes, that correspond to the section given as a parameter. """

    list_classes_by_section = []
    for item in list_classes:
        if item['Section'] == section:
            list_classes_by_section.append(item)

    list_classes_by_section = sorted(list_classes_by_section, key=operator.itemgetter('day_idx'))
    return list_classes_by_section


def filter_classes_by_semester(list_classes, semester):
    """ Takes a list of classes and returns a new list of classes, that correspond to the semester given as a parameter. """

    list_classes_by_semester = []
    for item in list_classes:
        if item['Semester'] == semester:
            list_classes_by_semester.append(item)

    # list_classes_by_semester = sorted(list_classes_by_semester, key=operator.itemgetter('day_idx'))
    return list_classes_by_semester


if __name__ == '__main__':
    main()

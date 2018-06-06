from DbHandler import filter_classes_by_year, filter_classes_by_section, filter_classes_by_semester

list_classes = [
    {
        'name': "cours 01", 'semester': "sem2", 'section': "allemand", 'year': "prope", 'day': "mardi", 'day_idx': 2,
    },
    {
        'name': "cours 02", 'semester': "sem2", 'section': "français", 'year': "2e", 'day': "mercredi", 'day_idx': 3,
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


def main():
    result = choice_user_controller(list_classes, "2e", "français")
    print(result)


def choice_user_controller(list_classes, choice_year, choice_semester, choice_section):
    """ Takes a list of classes and returns a list of the classes that
    correspond to the year, section and semester given as parameters. """

    filtered_classes = []
    filtered_classes = filter_classes_by_year(
        filter_classes_by_semester(
            filter_classes_by_section(
                list_classes,
                choice_section
            ),
            choice_semester),
        choice_year
    )

    return filtered_classes


if __name__ == '__main__':
    main()
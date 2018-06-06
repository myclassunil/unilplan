import re
import tempfile

def recoverSectionAndYear(file):
    """
    Due to the way the html data is presented on unil.ch, this function is required to extract the section and the year
    the courses on the page are available for.
    :param file: a path to the .html file that the data needs to be extracted from;
    :return: dict;
    """
    # initiations...
    selection_regex = re.compile("<h2>Votre sélection :</h2>(.+)<br><br><h2>Agenda (Printemps|Automne)")
    work_file = open(file, "r")
    output = None

    # loops on the lines of the html file, and selects the relevant part of the file with a regex.
    for line in work_file:

        output_match_object = selection_regex.match(line)
        if output_match_object:
            output = output_match_object.group(1, 2)
    work_file.close()

    # transforms the tuple created via the regex match group in a more explicit dictionary, and outputs it.
    if output:
        output_dict = dict()
        output_dict["Section"] = output[0].split(', ')[0]
        try:
            output_dict["Year"] = output[0].split(', ')[1]
        except IndexError:
            output_dict["Year"] = "N/A"
        output_dict["Semester"] = output[1]
        return output_dict
    else:
        return None


def recoverDay(file, string):
    """
    This function is not used as is and was created for testing purposes only, it is expected to be removed when/if
    we go live (although it's not a real problem, and it could be used elsewhere)
    It extracts the day of the week should the course we are working on is the very first course on that day
    It is then returned as a string, to modify the day variable.
    :param file: a path to the .html file that the data needs to be extracted from
    :param string: The name of the course
    :return:
    """
    day_regex = re.compile('.+(Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche).+\n.+\n.+\n.+\n.+'+string)
    work_file = open(file, "r")
    content_string = work_file.read()
    output_match_object = day_regex.findall(content_string)
    if output_match_object:
        return output_match_object[0]
    else:
        return None


def recoverTimePlaceNameAndTeacher(file):
    """
    This function extracts the data from the html file, and outputs a json formatted string which contains the
    data of all the courses of the html file.
    :param file: a path to the .html file that the data needs to be extracted from;
    :return: string
    """

    # initiations...
    selection_regex = re.compile("(^<td>)(.+)")
    options_filter_regex = re.compile("Programme")
    work_file = open(file, "r")
    content_string = work_file.read()
    indicator = 0
    day = ""
    temp = tempfile.TemporaryFile()
    output_string = ""
    section_and_year_and_semester = recoverSectionAndYear(file)
    
    work_file.seek(0)

    # creates from the original html file a temp file which contains only the data we are looking for
    for line in work_file:
        output_match_object = selection_regex.match(line)
        if output_match_object:
            temp.write(bytes(output_match_object.group(2)+"\n", "UTF-8"))
    temp.seek(0)

    # check whether or not the course actually fit in those we wish to treat (BA, excluding "Programme à options"
    if section_and_year_and_semester["Section"][0:2] == "BA" and not options_filter_regex.search(section_and_year_and_semester["Section"]):

        # This loop uses the line numbers to select the data and treat it
        for line in temp:
            decoded_line = line.decode()
            # decoded_line = decoded_line.replace('"', '\\\"')
            decoded_line = decoded_line.replace('"', "'")

            if indicator == 0:
                # lines 0 indicate the time and the start of a new course
                if section_and_year_and_semester:
                    output_string += ('{"Section" : "'+ section_and_year_and_semester["Section"] + '", "Year" : "' + section_and_year_and_semester["Year"] + '", "Semester" : "' + section_and_year_and_semester["Semester"] + '", ')
                else:
                    output_string += '{"Section" : "Inconnu", "Year" : "Inconnu", "Semester" : "Inconnu", '
                output_string += (' "Time" : "' + decoded_line[32:37] + ' ' + decoded_line[46:51] + '", ')
                indicator += 1
            elif indicator == 1:
                # line 1 is blank (it is a \n)
                indicator += 1
            elif indicator == 2:
                # line 2 contains the name of the course and treats the day of the week
                name = decoded_line.split("<")[0]

                day_regex = re.compile('.+(Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche).+\n.+\n.+\n.+\n.+' + name)
                day_match_object = day_regex.findall(content_string)
                if day_match_object:
                    day = day_match_object[0]
                output_string += ('"Name" : "'+ re.split("[</]", decoded_line)[0] + '", ')
                output_string += ('"Day" : "' + day + '", ')
                indicator += 1
            elif indicator == 3:
                # line 3 contains the teacher(s) of the course
                output_string += ('"Teacher" : "' + decoded_line[:-6] + '", ')
                indicator += 1
            elif indicator == 4:
                # line 4 contains the type of the course (C, C/TP, TP, ...)
                output_string += ('"CourseType" : "' + decoded_line[:-6] + '", ')
                indicator += 1
            elif indicator == 5:
                # line 5 contains the location of the course
                output_string += ('"Location" : "' + decoded_line[:-6] + '"}, \n')
                indicator = 0

    work_file.close()
    return output_string

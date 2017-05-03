"""

"""
from MailAsks.util import get_project_path
from MailAsks.util import get_archive_path
from MailAsks.util import get_subject_folder_path

import os


def get_questions():
    """
    Loads the files, that contain the questions of the subjects and formats them into a dictionary,
    Returns:
    A dictionary, whose keys are the strings with the subject names and the items are list, which in turn contain other
    sub lists, each one containing two items, the first(in order) being the string of the question and the second one
    being the
    """
    question_dictionary = {}
    # The list, containing all the string paths to the subject files
    subject_path_list = get_subject_path_list()

    for path in subject_path_list:

        # Getting the subject name as the name of the file
        subject_name = os.path.basename(path)

        # Getting the subject content
        subject_content = get_file_content(subject_name)
        # Getting the list structure from the string content
        subject_list = content_to_list(subject_content)

        # Adding it as an entry to the dictionary
        question_dictionary[subject_name] = subject_list

    # Returning the finished dictionary data structure
    return question_dictionary


def get_file_content(subject):
    """
    If given the name of the requested subject, this function assembles the path to the according file, reads all its
    contents and returns the read string.

    Args:
        subject: The string name of the subject, that is requested

    Returns:
    The complete string content of the file according to the given subject
    """
    # Getting the project path and the assembling the complete path with the subject included
    project_path = get_project_path()
    subject_path = os.path.join(project_path, "subjects", subject)

    # Reading the content of the file
    with open(subject_path, "r", encoding='iso-8859-1') as file:
        content = file.read()

    return content


def content_to_list(subject_content):
    """
    Takes the content that was read from one of the subject files in string format and converts it into a list, which
    contains sublists of two items, one being the question and the second the according integer amount of the previous
    uses of that question

    Args:
        subject_content: The string that was read from one subject content file

    Returns:
    A list, with sublists of the length two, that contain the question string and the according use amount in order
    """
    question_list = []
    # The string is formatted in a way, that the question string is in one line and in the next line is the integer
    # amount of how many times the question was previously used.
    # iterating through the list of lines and putting the question string and the integer into one sublist
    lines_list = subject_content.split("\n")
    sublist = []
    for line in lines_list:

        # First checking if the line is an empty string, and ignoring in case it is
        if len(line) == 0:
            continue

        sublist_length = len(sublist)
        # In case the length of the temporary sublist is zero, that means that no item has been added yet and also that
        # the next item that is to be expected is at the position of a question string
        if sublist_length == 0:
            sublist.append(line)

        # In case the length is one, that means, that the question string has been added already, that means that in the
        # next line there is to be expected the matching integer for the amount of past uses
        elif sublist_length == 1:
            sublist.append(int(line))

        # In case the length is 2, that means the sublist is complete for one question, thus the sublist is appended
        # to the main list and being reset
        elif sublist_length == 2:
            question_list.append(sublist)
            sublist = [line]
            continue

    # At the end it is possible, that the lines ended, but that there still is one question pair stuck in the sublist
    # thus checking for that case and appending to the main list if necessary.
    if len(sublist) == 2:
        question_list.append(sublist)

    # At the end returning the finished main list with the question tuple lists
    return question_list


def get_subject_path(subject):
    """
    This function creates the absolute path of the subject given
    Args:
        subject: The string name of the subject

    Returns:
    The string absolute path to the file of the subject given
    """
    # The path to the folder, in which all the subject files are being stored
    subject_folder_path = get_subject_folder_path()
    subject_path = os.path.join(subject_folder_path, subject)
    # Checking if the file exists
    if not os.path.exists(subject_path):
        raise FileExistsError("The file '{}' does not exist".format(subject_path))
    # Checking if it is a file
    if not os.path.isfile(subject_path):
        raise TypeError("The path '{}' does not point to a file".format(subject_path))

    return subject_path


def get_subject_path_dict():
    """
    This function creates a dictionary, that contains the names of the subjects as keys and the absolute paths to
    the subjects files as values.
    Returns:
    A dict with string subject names as keys and the string subject path as value
    """
    path_dict = {}
    # The folder in which the subject files are being saved
    subject_folder_path = get_subject_folder_path()
    # The names of all the subject files
    name_list = os.listdir(subject_folder_path)
    for subject_name in name_list:
        # The path to the subject of the current loop name
        subject_path = os.path.join(subject_folder_path, subject_name)
        # Checking whether it is a file, in case it is adding the path to the dictionary
        if os.path.isfile(subject_path):
            path_dict[subject_name] = subject_path

    return path_dict


def get_subject_path_list():
    """
    This function creates a list of all the paths to the subject files
    Returns:
    A list with the absolute string paths to the subject files
    """
    # Getting the path dictionary first and then just simply using the values list as the list to return
    path_dict = get_subject_path_dict()
    path_list = list(path_dict.values())
    return path_list


def get_subject_list():
    """
    This function creates a list containing all the string names of the subjects currently in the system
    Returns:
    A list of the string names of the subjects
    """
    # Simply using the path dictionary's keys list
    path_dict = get_subject_path_dict()
    names_list = list(path_dict.keys())
    return names_list


def update_files(dictionary_structure_chosen):
    """
    If given the dictionary structure, as it is returned by the picking algorithm, this function will laod the files
    of the subjects again, augment the amount of uses for the chosen questions only and then save the files again

    Args:
        dictionary_structure_chosen: The dictionary, whose keys are the string names of the subjects and the items being
            the lists with the chosen questions

    Returns:
    void
    """
    # Getting the project path and then extending it to be the path to the subjects folder of the project
    project_path = get_project_path()
    subjects_path = os.path.join(project_path, "subjects")

    # Iterating through the files subjects, building the paths to their according files, opening them changing the
    # numbers and then saving them again
    for subject in dictionary_structure_chosen.keys():
        question_list = dictionary_structure_chosen[subject]
        # The path to the file for the subject
        path = os.path.join(subjects_path, subject)

        with open(path, "r", encoding='iso-8859-1') as file:
            # Reading the file and splitting the content into the lines
            file_content = file.read()
            lines = file_content.split("\n")

        with open(path, "w+", encoding='iso-8859-1') as file:
            # Iterating through the chosen questions and for each question finding the index within the list of lines of
            # the file, it appears on and getting the item at the next index as the amount times this question was used,
            # then incrementing this number and replacing the old ine in the list with the incremented one
            for question in question_list:
                index = lines.index(question)
                amount_uses = int(lines[index + 1])
                lines[index + 1] = str(amount_uses + 1)

            # Writing the new lines list to the file
            file_content = '\n'.join(lines)
            file.write(file_content)


def archive(date_string, mail_content):
    """
    Given the string format of a date and the content of a mail string this function will create a file with a name
    derived from the date string inside the folder, that is specified as the archive folder in the config of the
    project and will then save the given string content to that file, thus archiving its content.
    The function checks for already existing files for the same date, instead of overwriting them though the file name
    will be extended by an additional index number.

    Args:
        date_string: The string format of the current date
        mail_content:  The string of the content, that is supposed to be archived

    Returns:
    void
    """
    # Getting the string of  the folder in which the archive files are supposed to be saved in from the config file
    archive_path = get_archive_path()
    # Creating the actual path of the file to save from the archive path and the filename from the date string
    file_name = "{}.txt".format(date_string)
    file_path = os.path.join(archive_path, file_name)

    # First checking how how many files for the current date already exist
    already_exists = True
    index = 2
    while already_exists:
        # Checking for the existence of the just assembled file path, in case the path does indeed exist, the file name
        # will be extended by an additional number at the end, repeating the process of checking the new file name
        # until a number has been found for which no file already exists.
        if os.path.exists(file_path):
            # Adding the index number to the string
            file_path = file_path.replace(".txt", "({}).txt".format(index))
            file_path = file_path.replace("({})".format(index - 1), "")
            index += 1

        else:
            # Breaking the loop in case the file path does not exist
            already_exists = False

    # Creating and opening the file with the file path and then writing the given mail content to it
    with open(file_path, "w+") as file:
        file.write(mail_content)


# The functions used to RESET the system

def reset_subject(subject):
    """
    This function will reset the progress of all the questions of the subject given, replacing the numbers stored in
    the subject file to track the amount of uses with a zero.
    Args:
        subject: The string name of the subject, whose questions to reset

    Returns:
    void
    """
    # Getting the subject path
    subject_path = get_subject_path(subject)
    # Opening the file and resetting all the use numbers for the questions to 0
    with open(subject_path, "w+") as file:
        lines = file.readlines()
        new_lines = []
        for line in lines:
            try:
                # Removing all the whitespace from the line
                line = line.replace(" ", "")
                # Trying if the line only consists of a number
                int(line)
                # Adding a zero instead
                new_lines.append("0")
            except ValueError:
                # In case the line is not a number just adding the normal question string to the new list aswell
                new_lines.append(line)
        # Writing the new lines into the file
        file.write('\n'.join(new_lines))


def reset_all():
    """
    This function will reset the progress on all the subjects.
    Returns:
    void
    """
    # Getting a list of all the subjects currently in the system
    subject_list = get_subject_list()
    # For each subject running the reset function
    for subject in subject_list:
        reset_subject(subject)







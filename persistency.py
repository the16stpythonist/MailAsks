from MailAsks.util import get_project_path

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
    subject_path_list = get_subject_paths()

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
    subject_path = "{}\\subjects\\{}".format(project_path, subject)

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


def get_subject_paths():
    """
    Returns:
    The list of absolute paths to the subject files, that contain the questions
    """
    path = "{}\\subjects".format(get_project_path())
    path_list = []
    # Getting the names of the files and folders inside the folder of the given path
    names = os.listdir(path)

    for name in names:

        # Assembling the complete path to the name
        temp_path = "{}\\{}".format(path, name)

        # Checking whether the path belongs to a file, if so adding it to the final list
        if os.path.isfile(temp_path):
            path_list.append(temp_path)

    return path_list


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
    subjects_path = "{}\\subjects".format(project_path)

    # Iterating through the files subjects, building the paths to their according files, opening them changing the
    # numbers and then saving them again
    for subject in dictionary_structure_chosen.keys():
        question_list = dictionary_structure_chosen[subject]
        # The path to the file for the subject
        path = "{}\\{}".format(subjects_path, subject)

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


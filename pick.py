from MailAsks.util import get_project_path
from MailAsks.util import get_total_uses
import random


def choose_questions(dictionary_structure, amount):
    """
    If given the dictionary structure, that has been loaded from the file system by the persitency module, this
    function applies the pseudo random picking algorithm to the list structures of each subject to generate a new
    dictionary structure, whose keys are the subject names and the lists of the chosen questions are the items.

    Args:
        dictionary_structure: The dictionary, whose keys are the string names of the subjects and the items the lists
            that contain the sub lists with the question strings and the amount of times they have used already.
            This structure is as defined by the interface between the picking algorithm and the persistency module
        amount: The integer amount of questions to be chosen per subject

    Returns:
    A dictionary, whose keys are the string names of the subjects and the items being the list, containing the strings
    of those questions that have been chosen by the algorithm
    """
    # The new dictionary, that is going to contain the subjects as the keys and the lists with the chosen question
    # strings as the items
    question_dict = {}

    for key in dictionary_structure.keys():
        item = dictionary_structure[key]

        # Choosing the questions for the subject
        question_list = choose_questions_subject(item, amount)

        # Adding the entry of the subject name and the chosen questions list to the new dictionary
        question_dict[key] = question_list

    # Returning the new dictionary
    return question_dict


def choose_questions_subject(list_structure, amount):
    """
    If given a list structure, as defined by the interface between the picking algorithm and the persitency system,
    this function pseudo randomly (which means, questions, that have been used more often than others have a lower
    probability of being chosen) chooses the questions to be sent.
    Args:
        list_structure: A list, containing sub lists, who in turn have to contain two items, the first being the string
            question and the second being the integer amount of times it was used already.
        amount: The integer amount of questions to be chosen from the list_structure


    Returns:
    A list, containing the strings of those questions, that have been chosen by the algorithm
    """
    # All the chosen questions will be added to this list
    question_list = []

    # Now getting the maximum amount of usages in the given list structure, so basically the amount of usages for
    # the question, that has been used the most, as all other questions stand in contrast to this local reference
    # originating from the same subject.
    maximum_usage_amount = get_max_amount_usages(list_structure) + 1

    # Repeating the process of choosing a question or not as long as the desired amount of questions has been
    # chosen and added to the final list
    while len(question_list) < amount:

        # The first step is to randomly choose one item, in this case a sublist, from the list structure
        sublist = random.choice(list_structure)

        # Building the difference between the maximum amount of usages of this subject and the actual amount of
        # usages for the randomly chosen question, which creates higher numbers, the lower the use amount of the
        # chosen question is
        difference = maximum_usage_amount - sublist[1]

        # Now generating a random number between 0 and 10, if the number is smaller than the difference, the question
        # will be picked and added to the main list, if not the while loop will just continue. By this practice, if the
        # difference number is bigger, the probability of the question being chosen is higher, thus the probability
        # for questions with a low use count(->higher difference) is higher.
        random_number = random.randint(1, 10)
        if random_number <= difference:
            question = sublist[0]
            question_list.append(question)

    return question_list


def get_max_amount_usages(list_structure):
    """
    For a given list structure, as it is the value to one of the subjects in the dictionary structure, that is loaded
    from the file system, this function will get the maximum amount for a question in the set

    Args:
        list_structure:  A list, containing sub lists, who in turn have to contain two items, the first being the string
            question and the second being the integer amount of times it was used already.

    Returns:
    The integer amount of the amount og usages of the question in the list, that has been used the most, so basically
    the biggest usage amount in the list
    """
    max_amount = 0
    for sublist in list_structure:

        # The amount a question of the list structure of the given subject has been used already is always given by
        # the integer, that is the second element of each sublist
        usages = sublist[1]
        # In case the new iteration of the loop found an amount fo usages that is bigger than all the previous ones
        # the saved number will be replaced with the new one
        if usages > max_amount:
            max_amount = usages

    # At the end of the loop the maximum amount of all the usages should have been found and is returned
    return max_amount


from MailAsks.util import get_total_uses
from MailAsks.util import get_amount_questions


def simple_string_format(dictionary_structure):
    """
    If given the dictionary structure, that was created as the output of the picking algorithm, this function will
    format the information of the dict into one single string, that contains a short introduction text at the
    beginning of the message and then the chosen questions sorted by the subject they are from

    Args:
        dictionary_structure: The dictionary, whose keys are the string names of the subjects to be used and whose
            items are lists containing the strings of tje chosen questions

    Returns:
    One single string, that contains the information about the chosen questions, which can be sent as it is
    """
    # This is the list, that will contain the sub strings, to be assembled as the main string in the end
    string_list = []

    # Getting the amount of questions used in this project as the the number of keys in the dictionary
    amount_questions = len(dictionary_structure) * get_amount_questions()
    # Getting the amount of uses aka the amount of already sent mails
    amount_uses = get_total_uses()

    # Generating the introduction text string
    introduction_string = get_introduction(amount_uses, amount_questions)
    string_list.append(introduction_string)
    string_list.append("\n\n")
    # Generating the main text string
    main_string = get_main_body(dictionary_structure)
    string_list.append(main_string)

    return ''.join(string_list)


def get_main_body(dictionary_structure):
    """
    If given the dictionary structure, as it is returned by the picking algorithm
    Args:
        dictionary_structure:

    Returns:
    The string, with all the chosen questions sorted by the subjects they are from
    """
    # this list contains the sub strings, which will later be assembled into the final string
    string_list = []

    for subject in dictionary_structure.keys():
        question_list = dictionary_structure[subject]
        # Building the header for the subject in as string in caps
        header = ["#"*(len(subject) + 2), "\n#", subject.upper(), "#\n", "#"*(len(subject) + 2)]
        string_list.append(''.join(header))
        string_list.append('\n\n')

        # Adding the Questions to the list
        for question in question_list:
            string_list.append(question)
            string_list.append("\n\n")

    return ''.join(string_list)


def get_introduction(uses, amount_questions):
    """
    If given the amount of total uses aka the amount of mails sent and the amount of questions for this particular
    Mail session, this will return the Introduction string for the email.

    Args:
        uses: The integer amount of mails already sent
        amount_questions: The amount of questions that were chosen for this mail

    Returns:
    The introduction string for the email
    """
    string_list = ["Greetings! ", "\n\n", "This is your learning aid Assistant MailAsks!", "\n",
                   "Today I prepared a total amount of ", str(amount_questions), " questions for your ", str(uses),
                   "th Mail.\n "]
    return ''.join(string_list)


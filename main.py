from MailAsks.persistency import get_questions
from MailAsks.persistency import update_files
from MailAsks.format import simple_string_format
from MailAsks.util import get_amount_questions
from MailAsks.pick import choose_questions
from MailAsks.mail import send


def send_mail(recipients):

    # Frist loading all the questions from the persitency and getting the dictionary structure as output
    dictionary_structure = get_questions()

    # Now choosing the questions to actually use according with the algorithm
    amount_questions = get_amount_questions()
    dictionary_structure = choose_questions(dictionary_structure, amount_questions)

    # Assembling the data structure into the final string
    message = simple_string_format(dictionary_structure)

    # Sending the message
    send(recipients, message)

    # Updating the amount of times the chosen questions have been used in the saved files for the subjects
    update_files(dictionary_structure)


if __name__ == "__main__":
    send_mail("jonseb1998@gmail.com")
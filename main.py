from MailAsks.persistency import get_questions
from MailAsks.persistency import update_files
from MailAsks.persistency import archive
from MailAsks.format import simple_string_format
from MailAsks.util import get_amount_questions
from MailAsks.util import get_last_sent_datetime
from MailAsks.util import get_date_string
from MailAsks.util import get_send_time
from MailAsks.pick import choose_questions
from MailAsks.mail import send

import datetime
import time



def send_mail(recipients, archiving=True):

    # Frist loading all the questions from the persitency and getting the dictionary structure as output
    dictionary_structure = get_questions()

    # Now choosing the questions to actually use according with the algorithm
    amount_questions = get_amount_questions()
    dictionary_structure = choose_questions(dictionary_structure, amount_questions)

    # Assembling the data structure into the final string
    message = simple_string_format(dictionary_structure)

    # Sending the message
    send(recipients, message)

    if archiving is True:
        # Getting the current date and archiving the send mail
        current_date_string = get_date_string()
        archive(date_string=current_date_string, mail_content=message)

    # Updating the amount of times the chosen questions have been used in the saved files for the subjects
    update_files(dictionary_structure)

    return True


def run():

    while True:
        # Waiting a Minute and then checking, if a new mail has to be sent
        time.sleep(10)
        # Checking whether the time for the new sending has come and whether it has already sent a mail today
        last_sent_datetime = get_last_sent_datetime()
        send_time = get_send_time()
        # The datetime object for the current time
        current_datetime = datetime.datetime.fromtimestamp(time.time())

        print(str(last_sent_datetime))
        print(str(send_time))
        print(str(current_datetime))

        if current_datetime.hour == send_time and last_sent_datetime.day != current_datetime.day:
            send_mail("jonseb1998@gmail.com")


if __name__ == "__main__":
    run()
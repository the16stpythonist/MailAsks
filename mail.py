from MailAsks.util import get_gmail_account
from MailAsks.util import get_config_path
from MailAsks.util import get_gmail_password
from MailAsks.util import get_total_uses
from email.mime.text import MIMEText
import configparser
import smtplib

TABLE = {
        0xe4: u'ae',
        ord(u'ö'): u'oe',
        ord(u'ü'): u'ue',
        ord(u'ß'): u's',
    }


def send(recipient, message):
    """
    This function will send an email from the specific email account of the MailAsks project to the email address
    specified as the string parameter and it will send an email containing the content, that was psecified by the
    string giiven as the message parameter. The subject of the email being a unified string, that is enumerated
    by the amount of the total uses / total emails sent until this point.

    Args:
        recipient: The string that specifies the email address of the one, that is supposed to receive the mail.
            This parameter can also be list fo strings, which each one of the strings being one of many receivers.
        message: The string, that is supposed to be sent.

    Returns:
    void
    """
    # Just wrapping the function that already sends an email with the account being used being fix
    gmail_account = get_gmail_account()
    gmail_password = get_gmail_password()
    subject = "Your daily learning questions {}".format(get_total_uses())

    send_email(gmail_account, gmail_password, recipient, subject, message)

    config_parser = configparser.ConfigParser()
    config_parser.read(get_config_path())

    uses = int(config_parser["Statistic"]["uses"])
    config_parser["Statistic"]["uses"] = str(uses + 1)
    with open(get_config_path(), "w") as file:
        config_parser.write(file)


def send_email(user, pwd, recipient, subject, body):
    """
    This function sends an email vie the email service Gmail of Google. The function therefore needs a google account
    name, which is the email address and the password for the account as strings. Also the string of the email address
    of the recipient is needed. For the email itself the subject and the body can be specified in two separate strings

    Args:
        user: The string of the gmail address of the user, that is being used to send the email
        pwd: The password for the gmail account, that is being used to send the mail
        recipient: The string of the email addresss the email is supposed to be sent to
        subject: The string of the short message, that is supposed to be used as the subject of the string
        body: The string, that is supposed to be the content of the email

    Returns:
    void
    """
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    message = message.translate(TABLE).encode('ascii', 'ignore')

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except Exception as e:
        print(e)

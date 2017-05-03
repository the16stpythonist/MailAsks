import configparser
import datetime
import time
import os


# THE UTILITY FUNCTIONS

def get_project_path():
    """
    Gets the path of this project folder in the filesystem as it is specified within the config file of this project

    Returns:
    The string with the absolute path leading to the main folder of this project
    """
    return os.path.dirname(os.path.abspath(__file__))


def get_config_path():
    """
    Gets the path of the config file to this project
    Returns:
    The string path of this project
    """
    project_path = get_project_path()
    config_path = os.path.join(project_path, "config.ini")
    return config_path


def get_subject_folder_path():
    """
    This function creates the path string for the path leading to the folder in which the subjects are being stored
    Returns:
    The string path to the subjects folder
    """
    project_path = get_project_path()
    subject_path = os.path.join(project_path, "subjects")
    return subject_path


def get_config():
    """
    This function returns the config parser, which can essentially be used as a dictionary
    Returns:
    pass
    """
    config_path = get_config_path()
    config = configparser.ConfigParser(config_path)
    return config


def get_total_uses():
    """
    Reads the config file of the project and returns the total amount of uses, which is essentially the total amount of
    mails already sent
    Returns:
    The integer amount of total mails sent
    """
    # Creating the config parser to read tge contents of the config file
    # The amount of total uses is saved inside the key 'uses' of the 'Statistic' header
    config_parser = configparser.ConfigParser()
    config_parser.read(get_config_path())

    uses = config_parser['Statistic']['uses']
    uses = int(uses)

    return uses


def get_amount_questions():
    """
    Reads the config file of the project and returns the amount of questions to be put into one mail
    Returns:
    The integer amount of questions in one Mail
    """
    # Creating the config parser object to read the config file of the project
    # The information about the amount questions to put into the mail, is saved in the 'questions_amount'
    config_parser = configparser.ConfigParser()
    config_parser.read(get_config_path())

    amount_questions = config_parser["Config"]['questions']
    amount_questions = int(amount_questions)

    return amount_questions


def get_gmail_account():
    """
    Reads the config file to fetch the account name of the gmail account from which to send the mails
    Returns:
    The string of the account name / the mail address of the according account
    """
    # Creating the config parser object to read the config file of the project
    # The information about the amount questions to put into the mail, is saved in the 'questions_amount'
    config_parser = configparser.ConfigParser()
    config_parser.read(get_config_path())

    gmail_account = config_parser["Config"]['gmail_account']
    gmail_account = gmail_account

    return gmail_account


def get_gmail_password():
    """
    Reads the config file of the project to get the password for the gmail account from which the messages are supposed
    to be sent
    Returns:
    The string of the password
    """
    # Creating the config parser object to read the config file of the project
    # The information about the amount questions to put into the mail, is saved in the 'questions_amount'
    config_parser = configparser.ConfigParser()
    config_parser.read(get_config_path())

    gmail_password = config_parser["Config"]['gmail_password']
    gmail_password = gmail_password

    return gmail_password


def get_archive_path():
    """
    Reads the confog file of this project to get the path of the folder in which the path to the folder, where the
    sent mails are supposed to be archived
    Returns:
    The string of the path to the folder of the archive
    """
    # Creating the config parser, that reads the INI config file of this project
    config_parser = configparser.ConfigParser()
    config_parser.read(get_config_path())

    archive_path = config_parser['Paths']['archive_path']

    return archive_path


def get_date_string():
    """
    Accesses the current date and time from as given from the operating system and the creates a formatted string from
    the current date. The day being first, the mont second and the year last, all three being separated by an
    underscore
    Returns:
    The string, containing the day, mont and year of when this function was called
    """
    # Creating the timestamp for the current time
    get_current_timestamp = time.time()
    # Creating the datetime obejct for the current datetime from the timestamp
    current_datetime = datetime.datetime.fromtimestamp(get_current_timestamp)

    # Getting the relevant information about the current date from the datetime object, which is the year, month and
    # the day
    year = current_datetime.year
    month = current_datetime.month
    day = current_datetime.day

    # Creating the formatted string of the date
    date_string_list = [str(day), '_', str(month), '_', str(year)]
    date_string = ''.join(date_string_list)

    return date_string


def get_last_sent():
    """
    This function reads the config file and returns the last time a mail was sent as the timestamp and the date string
    Returns:
    A tuple, whose first item is the float timestamp of the time a mail was sent and the second item being the string
    about that time
    """
    config = get_config()
    # Getting the float timestamp from the config
    timestamp = config["Statistic"]["last_sent_stamp"]
    timestamp = float(timestamp)
    # Getting the representative string from the config
    string = config["Statistic"]["last_sent"]

    return timestamp, string


def set_last_sent(timestamp):
    """
    This method sets the last sent parameter of the config file
    Args:
        timestamp: The float timestamp of the time, to which the last sending time is supposed to be set

    Returns:

    """
    config = get_config()
    # Setting the timestamp value directly
    config["Statistic"]["last_sent_stamp"] = str(timestamp)
    # Building a datetime object from the timestamp and saving the string representation of that object
    last_sent = datetime.datetime.fromtimestamp(timestamp)
    last_sent_string = str(last_sent)
    config["Statistic"]["last_sent"] = last_sent_string

    # Saving the config file
    config.write(get_config_path())
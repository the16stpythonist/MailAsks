import configparser


def get_project_path():
    """
    Gets the path of this project folder in the filesystem as it is specified within the config file of this project

    Returns:
    The string with the absolute path leading to the main folder of this project
    """
    # Creating the config parser to read the contents of the config file, which is in the same folder as this
    # module
    config_parser = configparser.ConfigParser()
    config_parser.read('config.ini')

    # Getting the project path as the item to the key 'project_path' in the 'Paths' header
    path = config_parser['Paths']['project_path']
    # Returning the string of the path
    return path


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
    config_parser.read('config.ini')

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
    config_parser.read('config.ini')

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
    config_parser.read('config.ini')

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
    config_parser.read('config.ini')

    gmail_password = config_parser["Config"]['gmail_password']
    gmail_password = gmail_password

    return gmail_password
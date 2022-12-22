import features as execute
import logging
import os


def setup_logging():
    """
    Set up the configuration for logging
    """
    logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO,
                        format=' %(levelname)s: %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


quit = False


def execute_command(params):
    """
    Map command to its corresponding method
    :param params: command followed by parameters
    :return: result of command
    """
    logging.info(f'Given command: {params[0]}')
    result = None
    command = params[0].lower()

    if command == "add_song":
        result = execute.add_song(params[1:])
    elif command == "delete_song":
        execute.delete_song(params[1:])
    elif command == "modify_data":
        result = execute.modify_data(params[1:])
    elif command == "search":
        result = execute.search(params[1:])
    elif command == "create_save_list":
        result = execute.create_save_list(params[1:])
    elif command == "play":
        result = execute.play(params[1:])
    else:
        logging.info("Invalid command")
        print("Unknown command")
    return result


def read_input_and_execute():
    """
    Read the input of the user and validate it
    :return: Result of the command
    """
    logging.info('Reading input from user')
    print("Type command: ")
    params = input().split()

    if len(params) < 1:
        print("No command")
        logging.error('No command')
        return

    given_command = params[0].lower()

    if given_command == "quit":
        global quit
        quit = True
        logging.info("Quitting the program")
        print("Quitting the program")
        return

    result = execute_command(params)

    return result


def create_storage_directory_if_not_exist():
    """
    Create a new storage directory if it does not exist
    """
    logging.info('Creating storage directory if not exist')
    path = "./Storage"
    global quit

    try:
        isExist = os.path.exists(path)

        if not isExist:
            os.makedirs(path)
            print("The new directory is created!")
            logging.info("The new directory is created!")

    except Exception as err:
        logging.exception(f"Error while creating song directory: {err}")
        print("Error while creating song directory")
        quit = True


def main():
    """
    Starting point pf the application
    """
    setup_logging()
    logging.info('Starting the program')

    try:
        create_storage_directory_if_not_exist()
        describe_features()
        while not quit:
            result = read_input_and_execute()
            if result is not None:
                print("Result: ", result)
    except Exception as err:
        logging.error(f'Error while executing the program: {err}')

    logging.info('Ending the program')


def describe_features():
    """
    Helper method to describe how the application can be used
    """
    print("This is SongStorage project. What you can do: \n")
    print("add_song path singer_name song_name date tags")
    print("delete_song id")
    print("modify_data id singer=test")
    print("search singer=maluma")
    print("create_save_list destinatie.zip singer=maluma")
    print("play singer=maluma song=mama \n")


main()

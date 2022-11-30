import features as execute
import logging
import os


def setup_logging():
    logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO,
                        format=' %(levelname)s: %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


quit = False


def execute_comand(params):
    logging.info(f'Given command: {params[0]}')
    result = ""

    command = params[0].lower()
    if command == "add_song":
        result = execute.add_song(params[1:])
    elif command == "delete_song":
        execute.delete_song(params[1:])
    elif command == "modify_data":
        result = execute.modify_data(params[1:])
    elif command == "search":
        execute.search(params[1:])
    elif command == "create_save_list":
        execute.create_save_list(params[1:])
    else:
        print("Unknown command")
        return result


def read_input_and_execute():
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
        return

    result = execute_comand(params)
    return result


def create_storage_directory_if_not_exist():
    path = "./Storage"
    global quit

    try:
        isExist = os.path.exists(path)

        if not isExist:
            os.makedirs(path)
            print("The new directory is created!")
    except Exception as err:
        logging.error(f"Error while creating song directory: {err}")
        print("Error while creating song directory")
        quit = True


def main():
    setup_logging()
    create_storage_directory_if_not_exist()
    logging.info('Starting the program')
    try:
        while not quit:
            result = read_input_and_execute()
            if result is not None:
                print("Result: ", result)
    except Exception as err:
        logging.error(f'Error while executing the program: {err}')

    logging.info('Ending the program')


main()

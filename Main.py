import features as execute
import logging


def setup_logging():
    logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO,
                        format=' %(levelname)s: %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


quit = False


def execute_comand(params):
    logging.info(f'Given command: {params[0]}')

    command = params[0].lower()
    if command == "add_song":
        execute.add_song(params[1:])
    elif command == "delete_song":
        execute.delete_song(params[1:])
    elif command == "modify_data":
        execute.modify_data(params[1:])
    elif command == "search":
        execute.search(params[1:])
    elif command == "create_save_list":
        execute.create_save_list(params[1:])
    else:
        print("Unknown command")
        return


def read_input_from_user():
    logging.info('Reading input from user')
    print("Type command: ")
    params = input().split()

    if len(params) < 1:
        print("No command given")
        return

    given_command = params[0].lower()

    if given_command == "quit":
        global quit
        quit = True
        return

    execute_comand(params)


def main():
    setup_logging()
    logging.info('Starting the program')
    try:
        while not quit:
            read_input_from_user()
    except:
        logging.error('Error while executing the program')

    logging.info('Ending the program')


main()

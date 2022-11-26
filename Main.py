import logging


def setup_logging():
    logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO,
                        format=' %(levelname)s: %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def main():
    setup_logging()

    logging.warning('warningg')
    logging.error('error')
    logging.info("info")
    logging.critical("critical")


main()

import logging
import redis
import json
import os
import zipfile
import uuid
from shutil import copy as copy_file
from pygame import mixer
import eyed3

db = redis.Redis(host='localhost', port=6379, db=0)


class Song:
    def __init__(self, file_name, singer, song_name, song_date, tags):
        self.file_name = file_name
        self.singer = singer
        self.song_name = song_name
        self.song_date = song_date
        self.tags = tags
        _, file_extension = os.path.splitext(file_name)
        self.format = file_extension


def get_new_id():
    """
    Generate a unique id
    :return: A new id
    """
    current_id = ''
    try:
        new_uuid = str(uuid.uuid4())
        current_id = f'song-{new_uuid}'
    except Exception as err:
        logging.error(f"Error while getting id from db {err}")
        exit()

    return current_id


def check_files_extension_and_path(path):
    """
    Check if file exists and the type is allowed.
    :param path: path where the file is located
    :return: False if file does not exist or is not in allowed types, True otherwise
    """
    logging.info("start check_files_extension_and_path method")
    print("start check_files_extension_and_path method")

    allowed_type = ["mp3", "wav"]

    if not os.path.exists(path):
        logging.error("File doesn't exist")
        print("File doesn't exist")
        return False

    _, file_extension = os.path.splitext(path)

    if file_extension[1:] not in allowed_type:
        logging.error("File extension not allowed")
        print("File extension not allowed")
        return False

    logging.info("check_files_extension_and_path method end")
    print("check_files_extension_and_path method end")

    return True


def add_song_auto(params):
    """
    Add a new song to the Storage folder and extract the metadata automatically.
    :param params: song file
    :return: The id of the song if it was created successfully, otherwise None
    """
    try:
        logging.info(f'start add_song_auto method')
        print(f'start add_song_auto method')

        if len(params) < 1:
            print("Wrong number of parameters")
            logging.error('Wrong number of parameters for add_song_auto')
            return

        path = params[0]

        if check_files_extension_and_path(path):
            extract_file_name = os.path.basename(os.path.normpath(path))
            file_path_in_Storage = f"./Storage/{extract_file_name}"

            if os.path.exists(file_path_in_Storage):
                logging.error("File already in storage")
                print("File already in storage")
                return None

            copy_file(path, "./Storage")

            audiofile = eyed3.load(path)
            singer = audiofile.tag.artist
            song_name = audiofile.tag.title
            song_date = audiofile.tag.getBestDate()
            tags = ""
            print(
                f'Are you ok with those metadata? singer={singer} song_name={song_name} song_date={song_date} (y/n)')
            answer = input()
            if answer is not "y":
                return None
            new_song = Song(file_path_in_Storage, singer,
                            song_name, song_date, tags)

            id = get_new_id()
            new_song_to_string = json.dumps(
                new_song, indent=4, cls=CustomEncoder)
            db.set(id, new_song_to_string)
            logging.info(
                f"add_song_auto method end. Song with id {id} was added in db")
            print(
                f"add_song_auto method end. Song with id {id} was added in db")
            return id

        return None

    except Exception as err:
        logging.error(f"Error while adding song: {err}")
        print("error")


def add_song(params):
    """
    Add a new song to the Storage folder and save the metadata in database.
    :param params:
    :return: The id of the song if it was created successfully, otherwise None
    """
    try:
        logging.info(f'start add_song method')
        print(f'start add_song method')

        if len(params) < 5:
            print("Wrong number of parameters")
            logging.error('Wrong number of parameters for add_song')
            return

        path = params[0]

        if check_files_extension_and_path(path):
            extract_file_name = os.path.basename(os.path.normpath(path))
            file_path_in_Storage = f"./Storage/{extract_file_name}"

            if os.path.exists(file_path_in_Storage):
                logging.error("File already in storage")
                print("File already in storage")
                return None

            copy_file(path, "./Storage")
            new_song = Song(file_path_in_Storage,
                            params[1], params[2], params[3], params[4])
            id = get_new_id()
            new_song_to_string = json.dumps(
                new_song, indent=4, cls=CustomEncoder)
            db.set(id, new_song_to_string)
            logging.info(
                f"add_song method end. Song with id {id} was added in db")
            print(f"add_song method end. Song with id {id} was added in db")
            return id

        return None

    except Exception as err:
        logging.error(f"Error while adding song: {err}")
        print("error")


def delete_song(params):
    """
    Delete a song by id.
    :param params: id of the song
    :return: None if there was an exception
    """
    logging.info('start delete_song method')

    try:
        if len(params) < 1:
            logging.error("Wrong number of parameters")
            print("Please provide an id")
            return None

        id = params[0]
        song = db.get(id)
        if song is not None:
            song_as_dict = json.loads(song)
            file_path = song_as_dict.get("file_name")
            if os.path.exists(file_path):
                print("File found")
                os.remove(file_path)
                db.delete(id)
                logging.info(f"Song with id {id} was deleted")
            else:
                print("Can not delete the file as it doesn't exists")
                logging.error("Can not delete the file as it doesn't exists")
        else:
            print("Song id not found")
            logging.info(f"Song id={id} not found")

    except Exception as err:
        logging.error(f"Error while deleting song: {err}")


def modify_data(params):
    """
    Modify metadata for an existing song in database
    :param params: fields that should be updated
    :return: None if an error occurred or the updated song
    """
    logging.info(f'start modify_data method')
    print(f'start modify_data method')
    new_song_to_string = ""

    try:
        if len(params) < 1:
            logging.error("Wrong number of parameters")
            print("Wrong number of parameters")
            return None
        else:
            id = params[0]
            for i in range(1, len(params)):
                if params[i].find("=") == -1:
                    logging.error("Wrong format of parameters")
                    print("Wrong format of parameters. Return")
                    return None
        song = db.get(id)
        if song is not None:
            song_as_dict = json.loads(song)
            new_fields = {}
            for i in range(1, len(params)):
                field, value = params[i].split("=")
                new_fields[field] = value
            song_as_dict.update(new_fields)
            new_song = convert_dict_to_song(song_as_dict)
            new_song_to_string = json.dumps(
                new_song, indent=4, cls=CustomEncoder)
            db.set(id, new_song_to_string)

    except Exception as err:
        logging.exception(f"Error while modifying song: {err}")
        return None

    logging.info(f"modify_data method end")
    print("modify_data method end")

    return new_song_to_string


def search(params):
    """
    Search songs based on given filters
    :param params: filters
    :return: Found songs
    """
    logging.info('start search method')
    print('start search method')
    filters = {}
    result = []
    try:
        for i in range(0, len(params)):
            if "=" not in params[i]:
                print("incorrect params")
                return None

            field, value = params[i].split("=")
            filters[field] = value

        db_registrations = db.keys("song-[0-9a-f]*")
        if len(db_registrations) > 0:
            for element in db_registrations:
                isOk = True
                item = db.get(element)
                item_as_dict = json.loads(item)
                for filter in filters.items():
                    key, value = filter
                    if item_as_dict.get(key).lower() != filters.get(key).lower():
                        isOk = False
                if isOk:
                    result.append(item_as_dict)
        else:
            print("Data not found")
            logging.info("Data not found")

    except Exception as err:
        logging.exception(f"Error while searching song: {err}")

    logging.info('search method end')
    print("search method end")

    return result


def create_save_list(params):
    """
    Create a zip with all the songs found based on the filters
    :param params: path to archive and song filters
    :return: None if exceptions occurred otherwise location of the zip file
    """
    try:
        logging.info("start create save list")
        print("start create save list")
        path_archive = params[0]
        _, file_extension = os.path.splitext(path_archive)
        if file_extension != ".zip":
            logging.error("Invalid output format")
            print("Please, provide correct path")
            return None
        zip_file = zipfile.ZipFile(path_archive, "w")

        result = search(params[1:])
        for item in result:
            path = item["file_name"]
            zip_file.write(path, path[10:])

        return zip_file

    except Exception as err:
        print("Error while creating save list")
        logging.exception(err)
        return None


def play(params):
    """
    Search a song by filters and play it
    :param params: filters
    :return: void
    """
    logging.info('start play')
    print('start play')
    try:
        result = search(params)
        if len(result) == 1:
            path = result[0]['file_name']
            if check_files_extension_and_path(path):
                mixer.init()
                mixer.music.load(path)
                mixer.music.play()
                input("press ENTER to stop")
                mixer.music.stop()
                mixer.quit()
        else:
            logging.error("Many songs were founded. Introduce more filters")
            print("Many songs were founded. Introduce more filters")

    except Exception as err:
        logging.exception(f"Error while playing song: {err}")

    logging.info('End Play')
    print('End Play')


def convert_dict_to_song(song_as_dict):
    """
    Convert a dictionary to a Song object
    :param song_as_dict: dictionary with key values strings
    :return: Song object
    """
    new_song = Song(song_as_dict.get("file_name"), song_as_dict.get("singer"), song_as_dict.get(
        "song_name"), song_as_dict.get("song_date"), song_as_dict.get("tags"))

    return new_song


class CustomEncoder(json.JSONEncoder):
    """
    Helper method used by json. dumps to encode a song object as json
    """

    def default(self, o):
        return o.__dict__

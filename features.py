import logging
import redis
import json
import os
from json import JSONEncoder
from shutil import copy as copy_file
from pygame import mixer

db = redis.StrictRedis(
    host='redis-15187.c300.eu-central-1-1.ec2.cloud.redislabs.com',
    port=15187,
    password='1KUpJnGql9sO5JwSz2hrXhipmffFXBNU',
    decode_responses=True)


class Song:
    def __init__(self, file_name, singer, song_name, song_date, tags):
        self.file_name = file_name
        self.singer = singer
        self.song_name = song_name
        self.song_date = song_date
        self.tags = tags


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def get_id_and_increment():
    current_id = "0"
    try:
        last_id = db.get("ids")

        if last_id is None:
            db.set("ids", "0")
            return current_id

        current_id = str(int(last_id)+1)
        db.set("ids", current_id)

        return current_id

    except:
        logging.error("Error while getting id from db")
        exit


def check_files_extension_and_path(path):
    logging.info("start check_files_extension_and_path")
    allowed_type = ["mp3", "wav", "png", "mp4"]
    if not os.path.exists(path):
        return False
    filename, file_extension = os.path.splitext(path)
    if file_extension[1:] not in allowed_type:
        return False
    return True


def add_song(params):
    try:
        logging.info(f'start add_song')

        if len(params) < 5:
            print("Wrong number of parameters")
            logging.error('Wrong number of parameters for add_song')
            return

        path = params[0]
        if check_files_extension_and_path(path):
            copy_file(path, "./Storage")
            file_name = os.path.basename(os.path.normpath(path))
            file_path_in_Storage = f"./Storage/{file_name}"
            new_song = Song(file_path_in_Storage,
                            params[1], params[2], params[3], params[4])
            id = get_id_and_increment()
            new_song_to_string = json.dumps(
                new_song, indent=4, cls=CustomEncoder)
            db.set(id, new_song_to_string)
            logging.info(
                f"add_song method end. Song with id {id} was added in db")
            print("Song added:", new_song_to_string)
            return id
        else:
            print("Wrong file type or path")
            logging.error(
                "Error extension file not allowed or file doesn't exist")
            return

    except Exception as err:
        logging.error(f"Error while adding song: {err}")
        print("eroare")


def delete_song(params):
    id = params[0]
    try:
        logging.info(f'start delete_song')
        song = db.get(id)
        if song is not None:
            song_as_dict = json.loads(song)
            file_path = song_as_dict.get("file_name")
            if os.path.exists(file_path):
                print("File found")
                os.remove(file_path)
                logging.info(f"File was deleted")
            else:
                print("Can not delete the file as it doesn't exists")
                logging.error("Can not delete the file as it doesn't exists")
            db.delete(id)
            logging.info(f"Song with id {id} was deleted from db")
        else:
            print("Song id not found")
            logging.info(f"Song id={id} not found")
    except Exception as err:
        logging.error(f"Error while deleting song: {err}")
    return


def modify_data(params):
    logging.info(f'start modify_data')
    id = params[0]

    try:
        # check params and format
        if (len(params) < 1):
            logging.error("Wrong number of parameters")
            return
        else:
            for i in range(1, len(params)):
                if (params[i].find("=") == -1):
                    logging.error("Wrong format of parameters")
                    print("Wrong format of parameters. Return")
                    return
        song = db.get(id)
        if song is not None:
            song_as_dict = json.loads(song)
            new_fields = {}
            for i in range(1, len(params)):
                field, value = params[i].split("=")
                new_fields[field] = value
            song_as_dict.update(new_fields)
            new_song = Song(song_as_dict.get("file_name"), song_as_dict.get("singer"), song_as_dict.get(
                "song_name"), song_as_dict.get("song_date"), song_as_dict.get("tags"))
            new_song_to_string = json.dumps(
                new_song, indent=4, cls=CustomEncoder)
            db.set(id, new_song_to_string)
    except Exception as err:
        logging.exception(f"Error while modifying song: {err}")

    logging.info(f"modify_data method end")
    return id


def search(params):
    logging.info('start search')
    filters = {}
    result = []
    isOk = True
    try:
        if len(params) < 1:
            return

        for i in range(0, len(params)):
            field, value = params[i].split("=")
            filters[field] = value

        db_registrations = db.keys('[0-9]*')
        if len(db_registrations) > 0:
            for element in db_registrations:
                iteam = db.get(element)
                item_as_dict = json.loads(iteam)
                for filter in filters.items():
                    key, value = filter
                    if item_as_dict.get(key) != filters.get(key):
                        isOk = False
                if isOk:
                    result.append(item_as_dict)
        else:
            print("Data not found")
            logging.info("Data not found")
    except Exception as err:
        logging.exception(f"Error while searching song: {err}")
    logging.info('search method end')
    print(result)
    return result


def create_save_list(params):
    print(params)
    return


def play(params):
    logging.info('start play')
    try:
        result = search(params)
        if len(result) == 1:
            path = result[0]['file_name']
            print(path)
            if check_files_extension_and_path(path):
                mixer.init()
                mixer.music.load(path)
                mixer.music.play()
                input("press ENTER to stop")
                mixer.music.stop()
                mixer.quit()
        else:
            logging.error("Many songs was founded. Introduce more filters")
            print("Many songs was founded. Introduce more filters")

    except Exception as err:
        logging.exception(f"Error while playing song: {err}")
    return


def convert_dict_to_song(song_as_dict):
    new_song = Song(song_as_dict.get("file_name"), song_as_dict.get("singer"), song_as_dict.get(
        "song_name"), song_as_dict.get("song_date"), song_as_dict.get("tags"))
    return new_song

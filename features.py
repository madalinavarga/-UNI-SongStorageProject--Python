import logging
import redis
import json
import os
from json import JSONEncoder
from shutil import copy as copy_file


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
    allowed_type = ["mp3", "wav", "png"]
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
            file_path_in_Storage = f".Storage/{file_name}"
            new_song = Song(file_path_in_Storage,
                            params[1], params[2], params[3], params[4])
            id = get_id_and_increment()
            new_song_to_string = json.dumps(
                new_song, indent=4, cls=CustomEncoder)
            db.set(id, new_song_to_string)
            logging.info(
                f"add_song method end. Song with id {id} was added in db")
            print("Song added")
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
            db.set(id, new_song)
    except Exception as err:
        logging.exception(f"Error while modifying song: {err}")

    return


def search(params):
    print(params)
    return


def create_save_list(params):
    print(params)
    return

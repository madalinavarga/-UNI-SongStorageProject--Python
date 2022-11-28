import logging
import redis
import json
import os
from json import JSONEncoder
from shutil import copy as copy_file


db = redis.Redis(
    host='redis-15187.c300.eu-central-1-1.ec2.cloud.redislabs.com',
    port=15187,
    password='1KUpJnGql9sO5JwSz2hrXhipmffFXBNU')


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


def check_files_extension(path):
    print("path:", path)
    allowed_type = ["mp3", "wav", "png"]
    try:
        filename, file_extension = os.path.splitext(path)
        print(file_extension)
        if file_extension[1:] not in allowed_type:
            return False
        return True
    except Exception as err:
        logging.error(f"Error extension file not allowed: {err}")


def add_song(params):
    try:
        print("paramsin add method", params)
        logging.info(f'start add_song')

        if len(params) < 5:
            print("Wrong number of parameters")
            logging.warning('Wrong number of parameters for add_song')
            return

        path = params[0]
        if check_files_extension(path):
            copy_file(path, "./Storage")
            new_song = Song(path, params[1], params[2], params[3], params[4])
            id = get_id_and_increment()
            new_song_to_string = json.dumps(
                new_song, indent=4, cls=CustomEncoder)
            db.set(id, new_song_to_string)

        logging.info(f"add_song method end. Song with id {id} was added in db")
        print("Song added")
        return id

    except Exception as err:
        logging.error(f"Error while adding song: {err}")
        print("eroare")


def delete_song(params):
    print(params)
    return


def modify_data(params):
    print(params)
    return


def search(params):
    print(params)
    return


def create_save_list(params):
    print(params)
    return

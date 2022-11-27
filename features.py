# from Main import setup_logging
import logging
import redis
import json
from json import JSONEncoder

# setup_logging()

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


def get_id():
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


def add_song(params):
    try:
        logging.info(f'start add_song')

        if len(params) < 5:
            print("Wrong number of parameters")
            logging.warning('Wrong number of parameters for add_song')
            return

        new_song = Song(params[0], params[1], params[2], params[3], params[4])
        id = get_id()
        new_song_to_string = json.dumps(new_song, indent=4, cls=CustomEncoder)
        db.set(id, new_song_to_string)

        logging.info("add_song method end. Song with id {id} was added in db")
        return id

    except:
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

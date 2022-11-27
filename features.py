from Main import setup_logging
import logging
import redis

setup_logging()

r = redis.Redis(
  host='redis-15187.c300.eu-central-1-1.ec2.cloud.redislabs.com',
  port=15187,
  password='1KUpJnGql9sO5JwSz2hrXhipmffFXBNU')


def add_song(params):
    logging.info(f'Sunt in modul 2')
    print(params)
    return


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

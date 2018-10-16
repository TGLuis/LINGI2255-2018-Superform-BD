from flask import current_app
import json

FIELDS_UNAVAILABLE = ['Title']

CONFIG_FIELDS = ["sender"]

def run(publishing,channel_config):
    print("hello")
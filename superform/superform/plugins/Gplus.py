from flask import current_app
import json
import google

FIELDS_UNAVAILABLE = ['Title']

CONFIG_FIELDS = ["sender"]

def run(publishing,channel_config):

    print("hello")
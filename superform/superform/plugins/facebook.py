from flask import current_app
import json
import facebook
import bond

FIELDS_UNAVAILABLE = ['Title', 'Description']  # list of field names that are not used by your module

CONFIG_FIELDS = ["page_id",
                 "app_id"]  # This lets the manager of your module enter data that are used to communicate with other services.

def run(publishing, channel_config):  # publishing:DB channelconfig:DB channel
    page_id = get_page_id(channel_config)  # data sur le sender ds channelconfig(= dictionnaire)
    js = bond.make_bond('JavaScript')
    js.eval_block('function getPageToken(){console.log("getting page token.... ");FB.api("/me/accounts?type=page", function(response) {console.log("response received");response.data.forEach(function(item, index, array) {if (item.name == "Test"){document.getElementById("access_token").value = item.access_token;console.log(item.access_token);return item.access_token;}});});}}')
    access_token = js.call('getPageToken()')  # data sur le receiver ds channelconfig(= dictionnaire)

    cfg = get_config(page_id, access_token)
    api = get_api(cfg)

    msg = get_message(publishing)
    link = get_link(publishing)
    image = get_image(publishing)

    status = api.put_object(
        parent_object="me",
        connection_name="feed",
        message=msg,
        link=link
    )

def get_api(cfg):
    graph = facebook.GraphAPI(cfg['access_token'])
    return graph


def get_page_id(config):
    json_data = json.loads(config)
    return json_data['page_id']


def get_app_id(config):
    json_data = json.loads(config)
    return json_data['app_id']


def get_config(page_id, access_token):
    cfg = {
        "page_id": page_id,  # Step 1
        "access_token": access_token  # Step 3
    }
    return cfg

def get_message(publishing):
    return publishing.title + "\n\n" + publishing.description

def get_link(publishing):
    return publishing.link_url


def get_image(publishing):
    return publishing.image_url
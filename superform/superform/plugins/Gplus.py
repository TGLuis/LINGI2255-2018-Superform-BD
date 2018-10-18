import json
import pprint

import google.oauth2.credentials
import googleapiclient.discovery
import flask

from superform import __init__

from flask import Blueprint

import google_auth_oauthlib.flow
import requests

Gplus_page = Blueprint('Gplus', __init__.__name__)



# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "superform/client_secret.json"



FIELDS_UNAVAILABLE = ['Title']
CONFIG_FIELDS = ['token', 'refresh_token', 'token_uri', 'client_id', 'client_secret', 'scopes']

#API_KEY = current_app.config['GPLUS_APIKEY']
#API = 'plusDomains'
#VERSION = 'v1'
#GPLUS = discovery.build(API, VERSION, developerKey=API_KEY)

#CLIENT_ID = ''
#CLIENT_SECRET = ''
# List the scopes required to create posts:
SCOPES = ['https://www.googleapis.com/auth/plus.me',
          'https://www.googleapis.com/auth/plus.stream.write']
#REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'





def run(publishing,channel_config):

    # Create the client object
    service = create_client_object(channel_config)

    # We can then refer to this client with 'me'
    user_id = 'me'
    body = create_activity_body(publishing)

    # Insert the activity
    result = service.activities().insert(
        userId = user_id,
        body = body
    ).execute()

    # Print the results
    print('Result = %s' % pprint.pformat(result))


def create_client_object(channel_config):
    """Creates a client object that allows us to publish posts
    :param ajoutezdesargsptn:
    :return: a client object # TODO change arg name!!!
    """
    credential = json.loads(channel_config)
    credentials = google.oauth2.credentials.Credentials(
       **credential)

    service = googleapiclient.discovery.build(
       'plus', 'v1', credentials=credentials)
    people_resource = service.people()
    people_document = people_resource.get(userId='me').execute()
    return people_document

    # print( "ID: " + people_document['id'])
    # print("Display name: " + people_document['displayName'])
    # print("Image URL: " + people_document['image']['url'])
    # print("Profile URL: " + people_document['url'])

def create_activity_body(publishing):
    """Creates the body of an activity specifying the content of the publication, restrictions on who will be able
    to see the activity and other options.
    :param publishing: the data of the publication
    :return: a JSON object respresenting a Google+ publication
    """
    # Get publication data
    content = publishing.description

    # Put data in body WARNING: modify the code to manage multiple circles, etc.
    body = {
        'object': {
            'originalContent': content
        },
        'access': {
            'items': [
                { 'type': 'domain' },
                { 'type': 'circle', 'id': 'PUT_ID'}
            ],
            'domainRestricted': True
        }
    }
    return body

@Gplus_page.route('/authorizeGplus')
def authorize():
  # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)

  flow.redirect_uri = flask.url_for('Gplus.oauth2callback',  _external=True)

  authorization_url, state = flow.authorization_url(
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true')

  # Store the state so the callback can verify the auth server response.
  flask.session['state'] = state

  return flask.redirect(authorization_url)

@Gplus_page.route('/oauth2callbackGplus')
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.
  state = flask.session['state']

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
  flow.redirect_uri = flask.url_for('Gplus.oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = flask.request.url
  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  credentials = flow.credentials
  flask.session['credentials']=credentials_to_dict(credentials)

  return flask.redirect(flask.url_for('channels.configure_channel', id=flask.session['id']))

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}



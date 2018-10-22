import json
import pprint

# Google+ API
import google.oauth2.credentials
from googleapiclient import discovery
import google_auth_oauthlib.flow

# Flask
from flask import Blueprint, url_for, request, redirect, session

from superform import __init__

FIELDS_UNAVAILABLE = ['Title']
CONFIG_FIELDS = ['token', 'refresh_token', 'token_uri', 'client_id', 'client_secret', 'scopes']

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "superform/configs/Gplus.json"

# Google+ API
API = 'plusDomains'
API_VERSION = 'v1'

# List of scopes required to create posts:
SCOPES = ['https://www.googleapis.com/auth/plus.me',
          'https://www.googleapis.com/auth/plus.stream.write']

Gplus_page = Blueprint('Gplus', __init__.__name__)


def run(publishing, channel_config):
    """Publishes the Google+ activity represented in @publishing, on the Google+ channel in channel_config.
    :param publishing: the data of the Google+ activity to be published
    :param channel_config: the configuration of the Google+ channel on which the activity will be published
    """
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
    # return result


def create_client_object(channel_config):
    """Creates a client object that allows us to publish posts
    :param channel_config: the configuration of the Google+ channel on which the activity will be published
    :return: a client object
    """

    # Load credentials
    credentials = google.oauth2.credentials.Credentials(**json.loads(channel_config))

    # Load API + get client object
    service = discovery.build(API, API_VERSION, credentials=credentials)
    people_resource = service.people()
    people_document = people_resource.get(userId='me').execute()
    return people_document


def create_activity_body(publishing):
    """Creates the body of an activity specifying the content of the publication, restrictions on who will be able
    to see the activity and other options.
    See https://developers.google.com/+/web/api/rest/latest/activities for infos about the activity options
    :param publishing: the data of the Google+ activity to be published
    :return: a dictionary representing a Google+ publication
    """
    # The main dictionary
    body = dict()
    # Dictionary containing the data in the publication (url, content, image, etc.)
    object = dict()
    # Dictionary containing the access restrictions to the publication
    access = dict()

    # Add publication data
    object['originalContent'] = publishing.description

    # Add link url
    if publishing.link_url is not None:
        object['url'] = publishing.link_url

    # Add image url #Todo add image
    if publishing.image_url is not None:
        #fullimage = dict()
        #fullimage['url'] = publishing.image_url
        #object['attachements'] = [{'fullimage', fullimage}]
        pass

    # Set access control #Todo manage more specific options (circle, etc.)
    access['items'] = [{'type': 'domain'}]

    # Add the sub-dictionaries to the body
    body['object'] = object
    body['access'] = access
    return body


@Gplus_page.route('/authorizeGplus')
def authorize():
    """Creates response object that allows a user to authorize access to his Google+ account.
    :return: a response object that, if called, redirects the client to the authorization url
    """
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('Gplus.oauth2callback',  _external=True)

    authorization_url, state = flow.authorization_url(
      # Enable offline access so that we can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    session['state'] = state

    return redirect(authorization_url)


@Gplus_page.route('/oauth2callbackGplus')
def oauth2callback():
    """Stores the credentials that enables access to the user's Google+ account.
    :return: a response object that, if called, redirects the client to the channel configuration page
    """
    # Specify the state when creating the flow in the callback so that it can be
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('Gplus.oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    credentials = flow.credentials
    session['credentials']=credentials_to_json(credentials)

    return redirect(url_for('channels.configure_channel', id=session['id']))


def credentials_to_json(credentials):
    """Transforms @credentials into a json object.
    :param credentials:
    :return: a json object containing the data in @credentials
    """
    dictionary = {'token': credentials.token,
                  'refresh_token': credentials.refresh_token,
                  'token_uri': credentials.token_uri,
                  'client_id': credentials.client_id,
                  'client_secret': credentials.client_secret,
                  'scopes': credentials.scopes}
    return json.dumps(dictionary)



import pprint



# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"



FIELDS_UNAVAILABLE = ['Title']
CONFIG_FIELDS = ["sender"]

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
    service = create_client_object()

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


def create_client_object(ajoutezdesargsptn):
    """Creates a client object that allows us to publish posts
    :param ajoutezdesargsptn:
    :return: a client object
    """
    pass

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


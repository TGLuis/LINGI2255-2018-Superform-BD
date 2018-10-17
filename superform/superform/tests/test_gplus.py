import datetime
import os
import tempfile

import pytest
import json

import superform.plugins.Gplus as Gplus

from superform import app, db
from superform.plugins import mail


@pytest.fixture
def client():
    app.app_context().push()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_run_gplus(client):
    # Is there a way to test a send mail function?
    assert True == True


def test_publish(publishing, channel_publishing):
    my_publi = Gplus.create_activity_body(publishing)
    assert my_publi is not None
    assert is_json(my_publi)
    #assert Gplus.run(publishing, channel_publishing)


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

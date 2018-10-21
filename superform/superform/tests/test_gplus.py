import datetime
import os
import tempfile

import pytest
import json
import unittest

import superform.plugins.Gplus as Gplus
import publishings as Publishing


from superform import app, db

class TestGPlus(unittest.TestCase):
    def test_login(self):
        pass

    def test_publish(self):
        my_publy = Publishing()

if __name__ == "__main__":
    unittest.main()


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
    # Is there a way to test a publishing method ? I think Yes ...
    assert True == True


def test_publish(publishing, channel_publishing):
    my_publi = Gplus.create_activity_body(publishing)
    assert my_publi is not None
    assert is_json(my_publi)
    assert my_publi.get('object').get('originalContent') == publishing.description
    #assert Gplus.run(publishing, channel_publishing)


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


import datetime
import os
import tempfile

import json
import unittest

import plugins.Gplus as Gplus


class Publishing:
    def __init__(self, post_id, title, description, link_url, image_url,
                 date_from, date_until, option=None, channel_id="Google+ INGI-UCL", state=-1):
        if option is None:
            option = [{"disablesharing": True, "disablecomments" : True, "circles": "Fanfan_Le_FDP"}]
        self.post_id = post_id
        self.channel_id = channel_id
        self.state = state
        self.title = title
        self.description = description
        self.link_url = link_url
        self.image_url = image_url
        self.date_from = date_from
        self.date_until = date_until
        self.extra = json.dumps(option)


class TestGPlus(unittest.TestCase):
    def test_login(self):
        channel_config = {"token": "ya29.Glw_BhYJwlHLDp3PlDxYJ9OzEL5k00bGMpsiVwwvC954J4l13Doo02P7PWD91m0NetnM1jF9zfaCZGQH5xLdUnfJbSloWzPGudBit-Up4otiqMTHPYY_0XuWglvYMw", "refresh_token": None, "token_uri": "https://www.googleapis.com/oauth2/v3/token", "client_id": "59367346006-eoo13gm4gm2aud1j4k0u6ebl1lvd311o.apps.googleusercontent.com", "client_secret": "N5aZQdD3frVPHxdAw643QoS-", "scopes": ["https://www.googleapis.com/auth/plus.me", "https://www.googleapis.com/auth/plus.stream.write"]}
        cl_doc = Gplus.create_client_object(channel_config)
        print(cl_doc["id"])

    def test_publishing(self):
        my_publy = Publishing(0, "Why Google+ is still relevant, even though it will soon cease to exist",
                              "And Jesus said : This is my body",
                              "www.chretienDeTroie.fr",
                              None, " 24-12-2018", "12-12-2222")
        retur = Gplus.create_activity_body(my_publy)
        self.assertEqual(retur['object'].get('originalContent', 'No content'), my_publy.description, "Problem with content")
        for a in retur['object']['attachements']:
            if a.get('objectType') == "article":
                self.assertEqual(retur['object']['attachements'].get('url', 'No content'), my_publy.link_url,
                                 "Problem with the link url")
            elif a.get('objectType') == "photo":
                self.assertEqual(retur['object']['attachements'].get('url', 'No content'), my_publy.image_url,
                                 "Problem with the image url")
        self.assertNotEquals((retur['object']['attachements'].get("Title", "No Title")), my_publy.title, "There should be no Title !")


if __name__ == "__main__":
    unittest.main()

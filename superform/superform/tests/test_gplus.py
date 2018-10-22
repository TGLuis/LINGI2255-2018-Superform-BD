import datetime
import os
import tempfile

import json
import unittest

import plugins.Gplus as Gplus


class Publishing:
    def __init__(self, title, description, link, image, from_, until_, channel_id = "Google+ INGI-UCL"):
        self.title = title
        self.description = description
        self.link = link
        self.image = image
        self.from_ = from_
        self.until_ = until_
        self.channel_id = channel_id


class TestGPlus(unittest.TestCase):
    def test_login(self):
        pass

    def test_publishing(self):
        my_publy = Publishing("Why Google+ is still relevant, even though it will soon cease to exist",
                              "And Jesus said : This is my body",
                              "www.chretienDeTroie.fr",
                              None, " 24-12-2018", "12-12-2222")
        retur = Gplus.create_activity_body(my_publy)
        self.assertEqual(retur.get('originalContent', 'No content'), my_publy.description, "Problem with content")
        self.assertEqual(retur.get('url', 'No content'), my_publy.link, "Problem with the link url")
        self.assertEqual(retur.get('image', 'No content'), my_publy.image, "Problem with the image url")
        self.assertEqual(retur.get('from', 'No content'), my_publy.from_, "Problem with the from date")
        self.assertEqual(retur.get('until', 'No content'), my_publy.until_, "Problem with the until date")
        self.assertNotEquals((retur.get("Title", "No Title")), my_publy.title, "There should be no Title !")


if __name__ == "__main__":
    unittest.main()

from django.test import TestCase, RequestFactory
import unittest
from tourneyBrag.views import PlayerList


class playerTests(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_post(self):
        request_instance = RequestFactory()
        request = request_instance.post('/fake-path', data={"playerID":"0", "playerName":"Dath", "password":"notdath", "gamePlayed":"Sm4sh", "mainCharacter":"Robin"})

        view = PlayerList.as_view()(request)

        self.assertNotEqual(view.data['playerID'], "0")
       # self.assertEqual(view.data[''])


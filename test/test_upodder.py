import unittest
import urllib2
from flask import Flask
from flask.ext.testing import LiveServerTestCase

class TestUpodder(LiveServerTestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        # Default port is 5000
        app.config['LIVESERVER_PORT'] = 8943

        @app.route("/ajax")
        def return_podcast_xml():
            return 'asdf'
        
        return app

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen(self.get_server_url() + '/ajax')
        self.assertEqual(response.code, 200)


if __name__ == '__main__':
    unittest.main()
import os, OCAPP, unittest, tempfile

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, OCAPP.app.config['DATABASE'] = tempfile.mkstemp()
        OCAPP.app.config['TESTING'] = True
        self.app = OCAPP.app.test_client()
        with OCAPP.app.app_context():
            OCAPP.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(OCAPP.app.config['DATABASE'])

    #We need to start writing tests prior to coding to make sure everything is fucntional as planned.

    # def test_display_conference_regis(self):
    #     rv = self.app.get('/conferences/2017')
    #     assert b'

if __name__ == '__main__':
    unittest.main()
import unittest, spotify_bot

class TestInlineQueryHandling(unittest.TestCase):
    def setUp(self):
        self.emptyQuery = ''
        self.nonEmptyQuery = 'Coldplay'

    def test_empty_query(self):
        self.assertTrue(spotify_bot.is_empty_query(self.emptyQuery))

    def test_nonempty_query(self):
        self.assertFalse(spotify_bot.is_empty_query(self.nonEmptyQuery))

if __name__ == '__main__':
    unittest.main()

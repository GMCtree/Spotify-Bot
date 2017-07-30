import unittest, spotify_bot

class TestInlineQueryHandling(unittest.TestCase):
    def setUp(self):
        self.emptyQuery = ''
        self.nonEmptyQuery = 'Coldplay'
        self.emptyResults = []
        self.nonEmptyResults = [{"artist": "Coldplay"}]

    def test_empty_query(self):
        self.assertTrue(spotify_bot.is_empty_query(self.emptyQuery))

    def test_nonempty_query(self):
        self.assertFalse(spotify_bot.is_empty_query(self.nonEmptyQuery))

    def test_empty_results(self):
        self.assertTrue(spotify_bot.check_no_results(self.emptyResults))

    def test_nonempty_results(self):
        self.assertFalse(spotify_bot.check_no_results(self.nonEmptyResults))

if __name__ == '__main__':
    unittest.main()

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

    def test_get_thumbnail_noThumnail(self):
        response = {}
        empty_tuple = spotify_bot.get_thumbnail(response)
        self.assertTrue(empty_tuple[0] == None
                and empty_tuple[1] == None
                and empty_tuple[2] == None)

    def test_get_thumbnail_thumbnailExists(self):
        response = {
            'images' : [ {
                'url' : 'some_url',
                'width' : 123,
                'height' : 123
            }]
        }
        thumbnail_info = spotify_bot.get_thumbnail(response)
        self.assertTrue(thumbnail_info[0] != None
                and thumbnail_info[1] != None
                and thumbnail_info[2] != None)

    def test_build_inline_query_article_track_thumbnail(self):
        _type = 'Track'
        response = {
            'album' : {
                'images' : [ {
                    'url' : 'some_url',
                    'width' : 123,
                    'height' : 123
                }]
            },
            'external_urls': {
                'spotify' : 'some_spotify_link'
            },
            'name' : 'some_name'
        }
        inlineQuery = spotify_bot.build_inline_query_result_article(_type, response)
        self.assertIsNotNone(inlineQuery.thumb_url)

    def test_build_inline_query_article_not_track_thumbnail(self):
        _type = 'Album'
        response = {
            'images' : [{
                'url' : 'some_url',
                'width' : 123,
                'height' : 123
            }],
            'external_urls': {
                'spotify' : 'some_spotify_link'
            },
            'name' : 'some_name'
        }
        inlineQuery = spotify_bot.build_inline_query_result_article(_type, response)
        self.assertIsNotNone(inlineQuery.thumb_url)


if __name__ == '__main__':
    unittest.main()

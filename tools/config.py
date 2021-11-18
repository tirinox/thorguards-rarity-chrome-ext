import os


class Config:
    PATH_METADATA = './data/metadata'
    PATH_THUMB = './data/thumb'
    PATH_ALL_META = './data/allmeta.json'
    PATH_ONLY_RANKS = './data/ranks.json'
    PATH_ONLY_RANKS_JS = '../ranks.js'

    DOWNLOAD_IMAGES = False
    DOWNLOAD_METADATA = True

    DOWNLOAD_FROM_SCRATCH = False

    CONTRACT = '0xa98b29a8f5a247802149c268ecf860b8308b7291'

    # N = 100
    # DOWNLOAD_BATCH_SIZE = 10

    N = 10000
    DOWNLOAD_BATCH_SIZE = 500

    @staticmethod
    def url_for_metadata(i):
        return f'https://thorguards.nyc3.cdn.digitaloceanspaces.com/metadata/{i}.json'

    @staticmethod
    def url_for_thumb_pic(i):
        return f'https://dt6foqftxxnwm.cloudfront.net/thumb/{i}.png'

    def path_for_metadata(self, i):
        return os.path.join(self.PATH_METADATA, f'{i}.json')

    def path_for_thumb_pic(self, i):
        return os.path.join(self.PATH_THUMB, f'{i}.png')

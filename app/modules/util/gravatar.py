"""
Gravatar Module
"""

# standard library
from hashlib import md5
from urllib.parse import urlparse, urlencode


class Gravatar():

    DEFAULT_IMAGE_SIZE = 80

    DEFAULT_IMAGE = [
        '404',
        'mm',
        'identicon',
        'monsterid',
        'wavatar',
        'retro',
        'robohash',
        'blank',
    ]

    RATINGS = [
        'g',
        'pg',
        'r',
        'x',
    ]

    PROFILE_FORMATS = ['json', 'xml', 'php', 'vcf', 'qr']

    def __init__(self, email):
        self.email = self.__sanitize_email(email)
        self.email_hash = self.__md5_hash(self.email)

    def get_image(self, size=DEFAULT_IMAGE_SIZE, default="", force_default=False, rating="", filetype_extension=False, use_ssl=False):
        base_url = '{protocol}://{domain}/avatar/' \
            '{hash}{extension}{params}'

        params_dict = {
            'size': size,
            'default': default,
            'forcedefault': force_default,
            'rating': rating,
        }

        if params_dict['size'] == self.DEFAULT_IMAGE_SIZE:
            del params_dict['size']
        else:
            if not (0 < params_dict['size'] < 2048):
                raise ValueError('Invalid image size.')
        if params_dict['default'] == '':
            del params_dict['default']
        else:
            if not params_dict['default'] in self.DEFAULT_IMAGE:
                if not self.__default_url_is_valid(params_dict['default']):
                    raise ValueError('Your URL for the default image is not valid.')
        if params_dict['forcedefault']:
            params_dict['forcedefault'] = 'y'
        else:
            del params_dict['forcedefault']
        if params_dict['rating'] == '':
            del params_dict['rating']
        else:
            if not params_dict['rating'] in self.RATINGS:
                raise ValueError('Invalid rating value.')

        params = urlencode(params_dict)

        protocol = 'http'
        domain = 'www.gravatar.com'
        if use_ssl:
            protocol = 'https'
            domain = 'secure.gravatar.com'

        extension = '.jpg' if filetype_extension else ''
        params = '?%s' % params if params else ''
        data = {
            'protocol': protocol,
            'domain': domain,
            'hash': self.email_hash,
            'extension': extension,
            'params': params,
        }
        return base_url.format(**data)

    def get_profile(self, data_format=''):
        base_url = 'http://www.gravatar.com/{hash}{data_format}'

        if data_format and data_format in self.PROFILE_FORMATS:
            data_format = '.%s' % data_format

        data = {
            'hash': self.email_hash,
            'data_format': data_format,
        }
        return base_url.format(**data)

    def __sanitize_email(self, email):
        return email.lower().strip()

    def __md5_hash(self, string):
        return md5(string.encode('utf-8')).hexdigest()

    def __default_url_is_valid(self, url):
        result = urlparse(url)

        if result.scheme == 'http' or result.scheme == 'https':
            path = result.path.lower()
            if (path.endswith('.jpg') or path.endswith('.jpeg') or path.endswith('.gif') or path.endswith('.png')):
                if not result.query:
                    return True
        return False

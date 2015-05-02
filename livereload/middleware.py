"""
Middleware for injecting the live-reload script.
"""
from django.conf import settings

HEAD_END_TAG = '</head>'
SCRIPT_URL = 'django_livereload/livereload.js'
SCRIPT_TAG = '<script type="text/javascript" src="//{}{}{}?host={}&port={}"></script>'
LIVERELOAD_HOST = getattr(settings, 'LIVERELOAD_HOST', 'localhost')
LIVERELOAD_PORT = getattr(settings, 'LIVERELOAD_PORT', '35729')


class LiveReloadScript(object):
    """
    Inject the live-reload script into your webpages.
    """

    def process_response(self, request, response):
        if HEAD_END_TAG not in response.content:
            return response

        SCRIPT_TAG_STRING = SCRIPT_TAG.format(
            request.META['HTTP_HOST'],
            settings.STATIC_URL,
            SCRIPT_URL,
            LIVERELOAD_HOST,
            LIVERELOAD_PORT,
        )
        response.content = response.content.replace(
            HEAD_END_TAG, '{}{}'.format(SCRIPT_TAG_STRING, HEAD_END_TAG)
        )

        if response.get('Content-Length', None):
            response['Content-Length'] += len(SCRIPT_TAG_STRING)

        return response

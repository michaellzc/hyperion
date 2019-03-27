import requests
import humps

from hyperion.models import Server


class ForeignServerHttpUtils:
    @staticmethod
    def get(server: Server, url, **kwargs):
        foreign_url = "{}{}{}".format(
            server.endpoint, url, "/" if server.required_trailing_slash else ""
        )
        print("[%s] HTTP/1.1 GET %s" % (__name__, foreign_url))
        return requests.get(
            foreign_url, auth=(server.foreign_db_username, server.foreign_db_password), **kwargs
        )

    @staticmethod
    def post(server: Server, url, json, **kwargs):
        foreign_url = "{}{}{}".format(
            server.endpoint, url, "/" if server.required_trailing_slash else ""
        )
        print("[%s] HTTP/1.1 POST %s" % (__name__, foreign_url))
        camalized_json = humps.camelize([json])[0]
        return requests.post(
            foreign_url,
            auth=(server.foreign_db_username, server.foreign_db_password),
            json=camalized_json,
            **kwargs
        )

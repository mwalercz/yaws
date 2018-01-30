from requests import Request
from requests import Session


class BrokerRequester:
    def __init__(self, broker_url, auth, cookie_keeper):
        self.session = Session()
        self.broker_url = broker_url
        self.auth = auth
        self.cookie_keeper = cookie_keeper
        self.request = Request()
        self.auth.add_headers(self.request)

    def make_request(self, method, path, json=None, params=None):
        url = self.broker_url + path
        self.request.method = method
        self.request.url = url
        self.request.json = json
        self.request.params = params
        prepared_request = self.request.prepare()
        response = self.session.send(prepared_request, verify=False)
        cookie = response.cookies.get('YAWSM_SESSION')
        if cookie:
            self.cookie_keeper.save_cookie(cookie)

        response.raise_for_status()
        return response

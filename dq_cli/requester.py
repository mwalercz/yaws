from requests import Request
from requests import Session


class Requester:
    def __init__(self, base_url, auth, cookie_keeper):
        self.session = Session()
        self.base_url = base_url
        self.auth = auth
        self.cookie_keeper = cookie_keeper

    def request(self, method, path, json=None, params=None):
        url = self.base_url + path
        request = Request(method=method, url=url, json=json, params=params)
        self.auth.add_headers(request)
        prepared_request = request.prepare()
        response = self.session.send(prepared_request, verify=False)
        cookie = response.cookies.get('DQ_SESSION')
        if cookie:
            self.cookie_keeper.save_cookie(cookie)

        response.raise_for_status()
        return response

import requests


class BrokerRequester:
    def __init__(self, url, auth, cookie_keeper):
        self.cookie_keeper = cookie_keeper
        self.url = url
        self.auth = auth

    def make_request(self, method, path, json=None, params=None, credentials=None):
        args = dict(
            method=method,
            url=self.url + path,
            json=json,
            params=params,
            verify=False,
            **self.auth.get_headers(credentials)
        )
        response = requests.request(**args)
        cookie = response.cookies.get('YAWSM_SESSION')
        if cookie:
            self.cookie_keeper.save_cookie(cookie)
        if response.status_code == 401:
            self.cookie_keeper.remove_cookie()

        response.raise_for_status()
        return response

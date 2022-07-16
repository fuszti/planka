import json
import requests


class SocketToKanbanBoard:
    PROJECTS_ENDPOINT="api/projects"
    BOARDS_ENDPOINT="api/boards"
    USERS_ENDPOINT="api/users"
    CARDS_ENDPOINT="api/cards"

    def __init__(self, baseURL, username, password):
        self.baseURL = baseURL
        self.username = username
        self.password = password
        self.headers = None
         
    def __enter__(self):
        self.headers = self._login_and_get_authenticated_headers(
            self.baseURL, self.username, self.password
        )
        return self
     
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.headers = None
    
    def get(self, api_path: str) -> dict:
        assert self.headers is not None, "This class implements the ContextManager interface, so use it inside the 'with' scope."
        response = requests.get(self.baseURL + api_path, headers=self.headers)
        content = json.loads(response.content.decode('utf-8'), encoding='utf-8')
        return content

    def _login_and_get_authenticated_headers(self, baseURL, username, password):
        headers = 'empty'
        authentication = requests.post(baseURL+'api/access-tokens', 
                                    data={
                                        'emailOrUsername': username, 
                                        'password': password})
        headers = { 'Authorization': 'Bearer {}'.format(authentication.json()['item']) }
        return headers

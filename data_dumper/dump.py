# This script handles the communication with planka
# TODO: get about cards:
# * time/date of getting in WIP
# * time/date of gettin in Done
# * current column
from dataclasses import dataclass, field
import json
from typing import List, Optional
import requests

# Connection information
baseURL = 'http://planka:1337/'
username = 'grafana_user'
password = 'passwd'
project_name = 'Important project'
board_name = 'Kanban'

class SocketToKanbanBoard():
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

@dataclass
class Timer:
    total_seconds: int

    @property
    def hours(self):
        return self.total_seconds // 60 // 60
    
    @property
    def minutes(self):
        return (self.total_seconds % (60 * 60) // 60)
    
    @property
    def seconds(self):
        return self.total_seconds % 60

@dataclass
class Card:
    title: str
    timer: Optional[Timer]
    members: List[str] = field(default_factory=lambda : [])

def get_cards_from_board(socket: SocketToKanbanBoard,
                         project_name: str,
                         board_name: str):
    projects = socket.get('api/projects')
    required_project_id = [project["id"] for project in projects['items'] if project['name'] == project_name][0]
    boards = socket.get(f'api/projects/{required_project_id}')['included']['boards']
    required_board_id = [board["id"] for board in boards if board['name'] == board_name][0]
    cards_content = socket.get(f'api/boards/{required_board_id}/cards')
    cards = {}
    for card_content in cards_content['items']:
        timer = Timer(card_content['timer']['total']) \
            if card_content['timer'] else None
        current_card = Card(card_content['name'], timer)
        cards[card_content['id']] = current_card
    for membership in cards_content['included']['cardMemberships']:
        card_id = membership['cardId']
        user_content = socket.get(f"api/users/{membership['userId']}")
        username = user_content['item']['username']
        cards[card_id].members.append(username)
    return list(cards.values())

if __name__ == '__main__':
    with SocketToKanbanBoard(baseURL, username, password) as socket:
        cards = get_cards_from_board(socket, project_name, board_name)
    print(cards)
from datetime import datetime
from data_dumper.data_connector.socket import SocketToKanbanBoard
from data_dumper.models.timer import Timer
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class CardDescriptor:
    card_id: str
    title: str
    timer: Optional[Timer]
    description: str
    creation_time: datetime
    due_date: Optional[datetime]

class Cards:
    def __init__(self, socket: SocketToKanbanBoard):
        self.socket = socket
    
    def read_cards(self, project_name: str, board_name: str) -> Dict[str, CardDescriptor]:
        projects = self.socket.get(self.socket.PROJECTS_ENDPOINT)
        required_project_id = [project["id"] for project in projects['items'] if project['name'] == project_name][0]
        boards = self.socket.get(f'{self.socket.PROJECTS_ENDPOINT}/{required_project_id}')['included']['boards']
        required_board_id = [board["id"] for board in boards if board['name'] == board_name][0]
        cards_content = self.socket.get(f'{self.socket.BOARDS_ENDPOINT}/{required_board_id}/cards')
        cards = {}
        for card_content in cards_content['items']:
            current_card = self._convert_to_card_descriptor(card_content)
            cards[current_card.card_id] = current_card
        return cards
    
    @staticmethod
    def _convert_to_card_descriptor(card_content):
        timer = Timer(card_content['timer']['total']) \
                if card_content['timer'] else None
        creation_time = datetime.strptime(card_content['createdAt'].replace("T", " ").replace("Z", "").split(".")[0], "%Y-%m-%d %H:%M:%S")
        due_date = datetime.strptime(card_content['dueDate'].replace("T", " ").replace("Z", "").split(".")[0], "%Y-%m-%d %H:%M:%S") \
            if card_content['dueDate'] else None
        current_card = CardDescriptor(
            card_content['id'], card_content['name'], timer,
            card_content['description'], creation_time, due_date
        )
        return current_card

if __name__ == "__main__":
    with SocketToKanbanBoard("http://planka:1337/", "grafana_user", "passwd") as socket:
        actions_model = Cards(socket)
        actions = actions_model.read_cards("Important project", "Kanban")
        print("done") # TODO: add lists
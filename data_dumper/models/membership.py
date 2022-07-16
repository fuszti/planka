from data_dumper.data_connector.socket import SocketToKanbanBoard
import pandas as pd

class Memberships:
    USER_ID_KEY = 'user_id'
    CARD_ID_KEY = 'card_id'

    def __init__(self, socket: SocketToKanbanBoard):
        self.socket = socket
    
    def read(self, project_name: str, board_name: str) -> pd.DataFrame:
        projects = self.socket.get(self.socket.PROJECTS_ENDPOINT)
        required_project_id = [project["id"] for project in projects['items'] if project['name'] == project_name][0]
        boards = self.socket.get(f'{self.socket.PROJECTS_ENDPOINT}/{required_project_id}')['included']['boards']
        required_board_id = [board["id"] for board in boards if board['name'] == board_name][0]
        cards_content = self.socket.get(f'{self.socket.BOARDS_ENDPOINT}/{required_board_id}/cards')
        memberships_content =cards_content["included"]["cardMemberships"]
        memberships_dict = {"user_id": [], "card_id": []}
        for membership_content in memberships_content:
            memberships_dict[self.USER_ID_KEY].append(membership_content['userId'])
            memberships_dict[self.CARD_ID_KEY].append(membership_content['cardId'])
        return pd.DataFrame(memberships_dict)


from datetime import datetime
from data_dumper.data_connector.socket import SocketToKanbanBoard
import pandas as pd


class CardMoves:
    TIME_KEY = "time"
    USER_ID_KEY = "user_id"
    FROM_KEY = "from_list"
    TO_KEY = 'to_list'
    CARD_ID_KEY = 'card_id'

    def __init__(self, socket: SocketToKanbanBoard):
        self.socket = socket
    
    def read(self, card_id):
        actions_content = self.socket.get(self.socket.CARDS_ENDPOINT + f"/{card_id}/actions")
        card_moves_dict = {
            self.TIME_KEY: [],
            self.USER_ID_KEY: [],
            self.FROM_KEY: [],
            self.TO_KEY: [],
            self.CARD_ID_KEY: [],
        }
        for action_content in actions_content['items']:
            if action_content['type'] == 'moveCard':
                time = datetime.strptime(action_content['createdAt'].replace("T", " ").replace("Z", "").split(".")[0], "%Y-%m-%d %H:%M:%S") \
                    if action_content['createdAt'] else None
                card_moves_dict[self.TIME_KEY].append(time)
                card_moves_dict[self.USER_ID_KEY].append(action_content['userId'])
                card_moves_dict[self.CARD_ID_KEY].append(action_content['cardId'])
                card_moves_dict[self.FROM_KEY].append(action_content['data']['fromList']['name'])
                card_moves_dict[self.TO_KEY].append(action_content['data']['toList']['name'])
            elif action_content['type'] == 'createCard':
                time = datetime.strptime(action_content['createdAt'].replace("T", " ").replace("Z", "").split(".")[0], "%Y-%m-%d %H:%M:%S") \
                    if action_content['createdAt'] else None
                card_moves_dict[self.TIME_KEY].append(time)
                card_moves_dict[self.USER_ID_KEY].append(action_content['userId'])
                card_moves_dict[self.CARD_ID_KEY].append(action_content['cardId'])
                card_moves_dict[self.FROM_KEY].append(None)
                card_moves_dict[self.TO_KEY].append(action_content['data']['list']['name'])
        return pd.DataFrame(card_moves_dict)

if __name__ == "__main__":
    with SocketToKanbanBoard("http://planka:1337/", "grafana_user", "passwd") as socket:
        actions_model = CardMoves(socket)
        actions = actions_model.read("736793457657381902")
        print("done")
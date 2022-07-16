from data_dumper.data_connector.socket import SocketToKanbanBoard
import pandas as pd

class CardLabels:
    USER_ID_KEY = 'user_id'
    CARD_ID_KEY = 'card_id'

    def __init__(self, socket: SocketToKanbanBoard):
        self.socket = socket
    
    def read(self, project_name: str, board_name: str) -> pd.DataFrame:
        projects = self.socket.get(self.socket.PROJECTS_ENDPOINT)
        required_project_id = [project["id"] for project in projects['items'] if project['name'] == project_name][0]
        boards = self.socket.get(f'{self.socket.PROJECTS_ENDPOINT}/{required_project_id}')['included']['boards']
        required_board_id = [board["id"] for board in boards if board['name'] == board_name][0]
        boards_content = self.socket.get(f'{self.socket.BOARDS_ENDPOINT}/{required_board_id}')
        labels_dict = {"label_id": [], "label_name": [], "label_color": []}
        for label_content in boards_content['included']['labels']:
            labels_dict["label_id"].append(label_content['id'])
            labels_dict["label_name"].append(label_content['name'])
            labels_dict["label_color"].append(label_content['color'])
        label_to_card = {'card_id': [], 'label_id': []}
        for card_to_label_content in boards_content['included']['cardLabels']:
            label_to_card['card_id'].append(card_to_label_content['cardId'])
            label_to_card['label_id'].append(card_to_label_content['labelId'])
        labels_df = pd.DataFrame(labels_dict)
        label_to_card_df = pd.DataFrame(label_to_card)
        return pd.merge([labels_df, label_to_card_df])

if __name__ == "__main__": # for quick test runs
    with SocketToKanbanBoard("http://planka:1337/", "grafana_user", "passwd") as socket:
        cards_label = CardLabels(socket)
        cards_label_df = cards_label.read("Important project", "Kanban")
        print("done") 

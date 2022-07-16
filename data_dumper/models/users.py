from datetime import datetime
from data_dumper.data_connector.socket import SocketToKanbanBoard
import pandas as pd


class Users:
    USER_ID_KEY = "user_id"
    USER_NAME_KEY = "user_name"
    NAME_KEY = "name"
    EMAIL_KEY = 'email'
    CREATION_TIME_KEY = 'creation_time'
    DELETION_TIME_KEY = 'deletion_time'
    ORGANIZATION_KEY = 'organization'

    def __init__(self, socket: SocketToKanbanBoard):
        self.socket = socket
    
    def read(self):
        users_content = self.socket.get(self.socket.USERS_ENDPOINT)
        users_dict ={
            self.USER_ID_KEY: [],
            self.USER_NAME_KEY: [],
            self.NAME_KEY: [],
            self.EMAIL_KEY: [],
            self.CREATION_TIME_KEY: [],
            self.DELETION_TIME_KEY: [],
            self.ORGANIZATION_KEY: [],
        }
        for user_content in users_content['items']:
            users_dict[self.USER_ID_KEY].append(user_content['id'])
            users_dict[self.USER_NAME_KEY].append(user_content['username'])
            users_dict[self.NAME_KEY].append(user_content['name'])
            users_dict[self.EMAIL_KEY].append(user_content['email'])
            creation_time = datetime.strptime(user_content['createdAt'].replace("T", " ").replace("Z", "").split(".")[0], "%Y-%m-%d %H:%M:%S") \
                if user_content['createdAt'] else None
            users_dict[self.CREATION_TIME_KEY].append(creation_time)
            deletion_time = datetime.strptime(user_content['deletedAt'].replace("T", " ").replace("Z", "").split(".")[0], "%Y-%m-%d %H:%M:%S") \
                if user_content['deletedAt'] else None
            users_dict[self.DELETION_TIME_KEY].append(deletion_time)
            users_dict[self.ORGANIZATION_KEY].append(user_content['organization'])
        return pd.DataFrame(users_dict)

if __name__ == "__main__":
    with SocketToKanbanBoard("http://planka:1337/", "grafana_user", "passwd") as socket:
        users_model = Users(socket)
        users = users_model.read()
        print("done")
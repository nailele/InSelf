import sqlite3


class Database:

    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def add_queue(self, chat_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `queue` ('chat_id') VALUES (?)", (chat_id,))

    def delete_queue(self, chat_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `queue` WHERE `chat_id` = ?", (chat_id,))

    def add_psyho(self, id_psy):
        with self.connection:
            return self.cursor.execute("INSERT INTO `psyho` ('id_psy') VALUES (?)", (id_psy,))

    def delete_psyho(self, id_psy):
        with self.connection:
            return self.cursor.execute("DELETE FROM `psyho` WHERE `id_psy` = ?", (id_psy,))

    def delete_chat(self, id_chat):
        with self.connection:
            return self.cursor.execute("DELETE FROM `chats` WHERE `id` = ?", (id_chat,))

    def get_chat(self):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM `queue`", ()).fetchmany(1)
            if (bool(len(chat))):
                for row in chat:
                    return row[1]
            else:
                return False

    def create_chat(self, chat_one, chat_two):
        with self.connection:
            if chat_two != 0:  # создание чата
                self.cursor.execute("DELETE FROM `queue` where `chat_id` = ?", (chat_one,))
                self.cursor.execute("DELETE FROM `psyho` WHERE `id_psy` = ?", (chat_two,))  #

                self.cursor.execute("insert into `chats` (`chat_one`, `chat_two`) values (?,?)", (chat_one, chat_two))
                return True

            else:
                return False

    def get_active_chat(self, chat_id):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM `chats` WHERE `chat_one` = ?", (chat_id,))
            id_chat = 0
            for row in chat:
                id_chat = row[0]
                chat_info = [row[0], row[2]]

            if id_chat == 0:
                chat = self.cursor.execute("SELECT * FROM `chats` WHERE `chat_two` = ?", (chat_id,))
                for row in chat:
                    id_chat = row[0]
                    chat_info = [row[0], row[1]]
                if id_chat == 0:
                    return False
                else:
                    return chat_info
            else:
                return chat_info

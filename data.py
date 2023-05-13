import sqlite3, datetime

class DataBase:
    def __init__(self):
        self.data = sqlite3.connect("database.db")
        self.cursor = self.data.cursor()
        self.today = datetime.datetime.today()
        self.data_time = self.today.strftime("%H:%M %Y-%m-%d")

    def get_history_numbers(self):
        with self.data:
            get_numbers = self.cursor.execute("SELECT number, date_time FROM history_numbers").fetchall()
            count = 1
            lists = "История номеров от старых до новых\n\n"
            for i in get_numbers:
                lists += f"{count}: {i}"
                count +=1
            return lists.replace("'", "").replace("(", "").replace(",", "").replace(")", "\n")

    def add_numbers(self, number):
        with self.data:
            self.cursor.execute(f"INSERT INTO history_numbers (number, date_time) VALUES (?, ?)", (number, self.data_time))

    def clear_database_history(self):
        with self.data:
            self.cursor.execute("DELETE FROM history_numbers")

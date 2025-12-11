class Storage:
    def __init__(self):
        self.db = []

    def insert(self, item):
        print("Storing item:", item)
        self.db.append(item)

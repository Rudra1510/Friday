import os
import random
import pymongo


class App:
    def __init__(self):
        self.menu = {}
        self.client = pymongo.MongoClient("mongodb://localhost:27017")
        self.client.drop_database("Porn")
        self.db = self.client["Porn"]

    def Run(self):
        categories = []
        path = r"F:/Mark-I/7839/Locker/Dash"
        i = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                category = file.split(" - ")[0]
                if category not in categories:
                    i += 1
                    print(f"{i}:{category}")
                    self.menu[f"{i}"] = category
                    categories.append(category)
                col = self.db[category]
                insertable = {"file": file}
                col.insert_one(insertable)
        while True:
            selection = input("Input : ")
            if selection != "":
                selected_category = self.menu[selection]
            elif selection == "q":
                quit()
            else:
                selection = random.randint(1, 16)
                selected_category = self.menu[str(selection)]

            selected_collection = self.db[selected_category]
            cursor = selected_collection.find()
            files = [x["file"] for x in cursor]
            r = random.choice(files)
            video = path + "/" + r
            os.system(f'start "" "{video}"')


App().Run()
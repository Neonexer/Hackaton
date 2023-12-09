from bs4 import BeautifulSoup
import requests, json, time, sqlite3, os

class Data:
    pageNumber = 0
    url = "https://structure.sfu-kras.ru/people?page="

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    dict = {}

    count = 0

    progress = 0


    def getProgress(self):
        return round((self.progress / (self.countOfPages / 100)))


    def findCountOfPages(self) -> int:

        req = requests.get(self.url + str(self.pageNumber), headers=self.headers)
        soup = BeautifulSoup(req.text, "html.parser")

        pages = soup.find("ul", class_="items pages-list").find_all_next("a", class_="item-link active")[-1].text
        pages = int(pages)
        return pages


    def parsePage(self, pageNumber):
        self.count
        req = requests.get(self.url + str(pageNumber), headers=self.headers)
        soup = BeautifulSoup(req.text, "html.parser")

        a = soup.find("table")
        b = a.find_all_next("tr")
        for i in b:
            name = i.find_next("a").text
            i = i.find_all_next("td")[1]
            dep = i.find_next("small").text
            contacts = i.find_next("span").text
            dep = dep.replace(contacts, "")

            contacts = contacts.replace(" [at] ", "@")
            contacts = contacts.replace(" [dot] ", ".")
            dep = dep.replace(" [at] ", "@")
            dep = dep.replace(" [dot] ", ".")
            if "@" in dep:
                contacts = [dep.split(",")[-1].strip(), contacts.strip()]
                dep = dep.split(",")[:-1]
                dep_ = ""
                for i in dep:
                    dep_ += ", " + i
                dep = dep_
                if dep.startswith(", "):
                    dep = dep[2:]
            else:
                contacts = [contacts]
            dep = dep.split(",", maxsplit=1)
            contacts.insert(0, dep[0].strip())
            try:
                contacts.insert(1, dep[1].strip())
            except:
                None
            # contacts.insert(1, dep[1])
            # print(a)
            # print(name)
            # print(dep)
            # print(contacts)

            contacts.insert(0, self.count)

            self.dict[name] = [contacts]

            self.count += 1


    def writeJson(self):
        with open("data.json", "w") as file:
            json.dump(self.dict, file, indent=4, ensure_ascii=False)

    def main(self):
        for i in range(0, self.countOfPages):
            self.parsePage(i)
            self.progress = i
            # print(i)
            print(self.getProgress(), "%")
        self.writeJson()

    def getData(self):
        for i in range(0, self.countOfPages):
        # for i in range(0, 5):
            self.progress = i
            self.parsePage(i)
            # print(i)
            print(self.getProgress(), "%")
        return self.dict

    def __init__(self):
        self.countOfPages = self.findCountOfPages()

    def getDataFromTable(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Выбираем всех пользователей
        cursor.execute('SELECT * FROM Users')
        users = cursor.fetchall()

        # Выводим результаты
        # for user in users:
        #     print(user.id)

        # Закрываем соединение
        connection.close()
        return users


    def saveData(self, data):

        try:
            os.remove("data.db")
        except:
            None

        # print(data)
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Создаем таблицу Users
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                department TEXT NOT NULL
                )
                ''')

        for i in data:
            id = data.get(i)[0][0]
            name = i
            # print(name)
            email = ""
            phone = ""
            department = data.get(i)[0][1]

            for j in data.get(i)[0]:
                if "@" in str(j):
                    email = j
                elif "+7" in str(j):
                    phone = j

            # Добавляем нового пользователя
            cursor.execute('INSERT INTO Users (id, username, email, phone, department) VALUES (?, ?, ?, ?, ?)',
                           (id, name, email, phone, department))

        # Сохраняем изменения и закрываем соединение
        connection.commit()
        connection.close()


if __name__ == "__main__":
    time_ = time.time()
    a = Data()
    # a.main()
    a.dict = a.getData()
    a.saveData(a.dict)
    a.writeJson()
    for k, v in a.dict.items():
        print(k, v)
    print(time.time() - time_)

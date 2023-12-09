from bs4 import BeautifulSoup
import requests, json, time

class Data:
    pageNumber = 0
    url = "https://structure.sfu-kras.ru/people?page="

    dict = {}

    count = 0


    def findCountOfPages(self) -> int:
        req = requests.get(self.url + str(self.pageNumber))
        soup = BeautifulSoup(req.text, "html.parser")

        pages = soup.find("ul", class_="items pages-list").find_all_next("a", class_="item-link active")[-1].text
        pages = int(pages)
        return pages


    def parsePage(self, pageNumber):
        self.count
        req = requests.get(self.url + str(pageNumber))
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
                contacts = [dep.split(",")[-1], contacts]
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
            contacts.insert(0, dep[0])
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
            json.dump(dict, file, indent=4, ensure_ascii=False)

    def main(self):
        for i in range(0, self.findCountOfPages()):
            self.parsePage(i)
            print(i)
        self.writeJson()

    def getData(self):
        for i in range(0, self.findCountOfPages()):
            self.parsePage(i)
            print(i)
        return self.dict


if __name__ == "__main__":
    time_ = time.time()
    a = Data()
    a.main()
    for k, v in dict.items():
        print(k, v)
    print(time.time() - time_)

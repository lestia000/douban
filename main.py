import re
import sqlOp
import urlReq
from bs4 import BeautifulSoup


def deal_text(parent_ele, ele, tag):
    element = parent_ele.find(ele, tag)
    if element:
        return element.text
    else:
        return str()


def deal_data(element):
    link = element.find("a")["href"]
    img_link = element.find("img")["src"]
    name = element.findAll("span", class_="title")
    if len(name) > 1:
        cname = name[0].text
        e_name = re.sub(f"[/|\xa0]", "", name[1].text)
    else:
        cname = name[0].text
        e_name = str()
    score = deal_text(element, "span", "rating_num")
    info = re.sub(f'\n\\s+', "", re.sub("[\xa0+]", " ",
                                        re.findall(f'\n.*(?=\n)', element.find("div", "bd").find("p").text)[0]))
    person = re.sub(f'人评价', "", element.find("div", "star").findAll("span")[
        len(element.find("div", "star").findAll("span")) - 1].text)
    profile = deal_text(element, "span", "inq")
    return [link, img_link, cname, e_name, score, person, info, profile]


class Movie:
    @staticmethod
    def get_obj():
        return ["link", "imgLink", "c_name", "e_name", "score", "person", "info", "profile"]

    @staticmethod
    def get_types(length):
        return (("varchar(255)," * (length - 1)) + "varchar(255)").split(",")


if __name__ == '__main__':
    conn = sqlOp.create_con("localhost", "username", "password", "database")
    cursor = conn.cursor()
    data = []
    for i in range(0, 250, 25):
        url = f"https://movie.douban.com/top250?start={i}&filter="
        page_data = urlReq.get_page(url)
        soup = BeautifulSoup(page_data, "html.parser")
        all_div = soup.findAll("div", class_="item")
        for div in all_div:
            divSoup = BeautifulSoup(str(div), "html.parser")
            data.append(deal_data(divSoup))
    sqlOp.insert_data(conn, cursor, 'movie', [Movie.get_obj(), Movie.get_types(len(Movie.get_obj()))], data, close=True)

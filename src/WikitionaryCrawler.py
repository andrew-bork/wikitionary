import requests
from bs4 import BeautifulSoup, Tag
from typing import Callable
import re
import copy

# class WikitionaryParser:

#     def __init__(self):

# class RequestResult:
#     def __init__(self):
#         self.time = 0
#         self.content
#         pass

def get(url:str):
    return requests.get(url).content

def with_id(id:str) -> Callable[[Tag], bool]:
    return lambda tag : tag.has_attr("id") and tag["id"] == id

def elements_between_ids(document:BeautifulSoup, start:str, end:str) -> Tag:
    start = None
    curr = document.find_all(with_id(start))
    print(curr)
    
    has_end_id = with_id(end)
    while curr is not None and not has_end_id(curr):
        if(start == None):
            start = copy.copy(curr)
        else:
            start.append(copy.copy(curr))
        print(curr)
        curr = curr.next_sibling

    return start
# class parse_pronounciation()


def get_term(term:str=""):
    content = get(f"https://en.wiktionary.org/wiki/{term}")
    soup  = BeautifulSoup(content, "html.parser")
    # print(soup.find_all(lambda tag : tag.has_attr("role") and tag["role"] == "navigation")[0])

    nav_table = soup.find_all(lambda tag : tag.has_attr("role") and tag["role"] == "navigation")[0]

    def with_href(href:str) -> Callable[[Tag], bool]:
        return lambda tag : tag.has_attr("href") and tag["href"] == href
    
    def part_of_table_of_contents(href:str) -> Callable[[Tag], bool]:
        return lambda tag : tag.find(with_href(href),recursive=False) != None
        
    def pronounciations(tag:Tag):
        def a(tag:Tag):
            return tag.has_attr("href") and tag["href"].startswith("#Pronunciation_")
        return tag.find(a) != None

    def pronounciation_link(tag:Tag):
        return tag.has_attr("href") and tag["href"].startswith("#Pronunciation_")


    a = nav_table.find(part_of_table_of_contents("#Chinese"))
    
    # print(a)
    print(soup.find(with_id("Pronunciation_1")))
    print([a["href"] for a in a.find_all(pronounciation_link)])
    print(elements_between_ids(soup, "Pronunciation_1", "Pronunciation_2"))
    # a = nav_table.find(part_of_table_of_contents("#Japanese"))
    # print(a)
    # links = nav_table.find_all("a")
    # links
    # translingual_begin = links.index("#Translingual")
    # chinese_begin = links.index("#Chinese")
    # japanese_begin = links.index("#Japanese")
    # korean_begin = links.index("#Korean")

    # translingual = links[translingual_begin:chinese_begin]
    # chinese = links[chinese_begin:japanese_begin]
    # chinese_pronounciations = [ i.starts_with("#Pronunciation_") for i in chinese]
    # japanese = links[japanese_begin:korean_begin]
    # korean = links[korean_begin:]

    # print(chinese_pronounciations)

    with open(f"{term}.txt", "w") as a:
        a.write(soup.text)



if __name__ == "__main__":
    print(get_term("朝"))
    print(get_term("民"))
    print(get_term("平"))
    print(get_term("本"))
    print(get_term("日"))
    print(get_term("日本"))
    print(get_term("民權"))
    print(get_term("忠孝"))
    print(get_term("復興"))
    print(get_term("東京"))
    print(get_term("南京"))

    # print(get_term("朝四暮三"))
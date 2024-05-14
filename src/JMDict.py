import xml.etree.ElementTree as ET
import coloredlogs
import logging
import time
import romkan
import MeCab

logger = logging.getLogger(__name__)
coloredlogs.install()




class JMDict:
    def __init__(self, filepath):
        self.filepath = filepath
        self.load()
    

    def load(self):
        start = time.perf_counter()
        logging.info("Loading dictionary...")
        with open(self.filepath, "r") as file:
            root = ET.fromstring(file.read())

        self.entries = {}
        for entry in root[:]:
            kanji_ele = entry.find("k_ele")
            reading_ele = entry.find("r_ele")
            sense_ele = entry.find("sense")
            if(entry.find("k_ele") is not None):
                gloss_ele = sense_ele.find("gloss")
                hiragana = reading_ele.find("reb").text
                romaji = romkan.to_roma(hiragana)
                kanji = kanji_ele.find("keb").text
                if(kanji in self.entries):
                    self.entries[kanji].append((hiragana, gloss_ele.text))
                else:
                    self.entries[kanji] = [(hiragana, gloss_ele.text)]

                # print(kanji_ele.find("keb").text + " - (" + hiragana + " " + romaji + ") - " + gloss_ele.text)

        self.tokenizer = MeCab.Tagger("-Owakati")

        elapsed = time.perf_counter() - start
        logging.info("Dictionary Loaded. Took %ds.", elapsed)
        logging.info("%d entries loaded.", len(root))

    def search(self, kanji):
        print(self.entries[kanji])



if __name__ == "__main__":
    dict = JMDict("/Users/borky/Downloads/JMdict_e.xml")
    # dict.search("あの日が私の人生で最高の日だった")
    input_sentence = "あの日が私の人生で最高の日だった"
    # input_sentence = '10日放送の「中居正広のミになる図書館」（テレビ朝日系）で、SMAPの中居正広が、篠原信一の過去の勘違いを明かす一幕があった。'
    # ipadic is well-maintained dictionary #
    print(dict.tokenizer.parse(input_sentence).split())
    # mecab_wrapper = JapaneseTokenizer.MecabWrapper(dictType='ipadic')
    # print(mecab_wrapper.tokenize(input_sentence).convert_list_object())

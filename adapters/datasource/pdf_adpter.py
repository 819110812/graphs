import time
from pdfminer.high_level import extract_text
from tqdm import tqdm

from adapters.datasource.datasource_base_adapter import BaseAdapter
from tools.parser import *
from adapters.database.mongo_adapter import *
import base64

class PdfAdapter(BaseAdapter):
    def __init__(self, path: str):
        super().__init__(path)

    def get_content(self) -> str:
        pass

    def get_sentences(self) -> list:
        pass

    def get_words(self) -> list:
        pass

    @staticmethod
    def extract_text_from_pdf(path) -> str:
        text = extract_text(path)
        return text

    def get_all_words_from_pdf(self) -> list[str]:
        pass

    def build_map_from_word_to_image(self):
        # step1 提取所有的图片
        byte_list = extract_image_bytes_from_pdf(self.path)
        mongodb_client = MongoDB("graphs", "localhost", 27017, "root", "root")
        mongodb_client.create_collection("data")
        # step2 提取所有的文字
        # O(mn) TODO: 优化
        start = time.time()
        logging.info("start to process")
        for item in tqdm(byte_list):
            base64_str = base64.b64encode(item)
            plain_text = clean_sentence(extract_text_from_image_bytes(item))
            words = parse_words(plain_text)
            for word in words:
                temp = {"word": word, "image": [item]}
                if mongodb_client.find_one("data", {"word": word}) is None:
                    mongodb_client.insert_one("data", temp)
                else:
                    mongodb_client.update_one("data", {"word": word}, {"$push": {"image": item}})

        end = time.time()
        logging.info("end to process")
        logging.info("time cost: {}".format(end - start))

        # step3 将文字和图片进行匹配

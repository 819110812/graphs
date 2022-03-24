import os
import time
import base64
from tqdm import tqdm
from tools.parser import *
from multiprocessing import Process, Pool
from pdfminer.high_level import extract_text
from adapters.database.mongo_adapter import *
from adapters.datasource.datasource_base_adapter import BaseAdapter


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
        logging.info("Number of cpu: {}".format(os.cpu_count()))

        # TODO: 并行计算
        for item in tqdm(byte_list[:10]):
            plain_text = clean_sentence(extract_text_from_image_bytes(item))
            words = parse_words(plain_text)
            for word in words:
                try:
                    self.store_data(mongodb_client, word, item)
                except Exception as e:
                    logging.error(e)
                    for i in range(3):
                        logging.error("retry")
                        try:
                            self.store_data(mongodb_client, word, item)
                            break
                        except Exception as e:
                            logging.error(e)
                            break

        end = time.time()
        logging.info("end to process")
        logging.info("time cost: {}".format(end - start))

        # step3 将文字和图片进行匹配

    def store_data(self, mongodb_client, word, item):
        time.sleep(0.5)
        temp = {"word": word, "image": [item]}
        if mongodb_client.find_one("data", {"word": word}) is None:
            mongodb_client.insert_one("data", temp)
        else:
            mongodb_client.update_one("data", {"word": word}, {"$push": {"image": item}})


if __name__ == '__main__':
    cur = os.path.abspath(os.path.dirname(__file__))
    root = os.path.abspath(os.path.join(cur, '../../'))
    filepath = os.path.join(root, 'test_data/明源云采招系统操作手册.pdf')
    pdf_adapter = PdfAdapter(filepath)
    pdf_adapter.build_map_from_word_to_image()

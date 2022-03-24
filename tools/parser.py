import logging
import re
import os
import fitz
import jieba
import pytesseract
from PIL import Image
from io import BytesIO

cur = os.path.abspath(os.path.dirname(__file__))
root = os.path.abspath(os.path.join(cur, '..'))


# O(n)
def get_stopwords(file: str) -> list[str]:
    with open(file, 'r', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f.readlines()]
    return stopwords


# O(n)
def parse_sentences(file_content: str) -> list:
    """
    :param file_content: 文件读出来的内容
    :return: 分句后的列表
    """
    sentences = re.split("(。|！|\!|\.|？|\?|\n)", file_content)
    res = []
    for sent in sentences:
        res.append(clean_sentence(sent))
    return sentences


def clean_sentence(sent: str, mode=None) -> str:
    # 去除空格和回车
    sent = sent.replace("\n", "").replace(" ", "")
    # 去除数字
    sent = clean_all_numbers(sent)
    if mode == "key":
        pass
    return sent


def only_include_key_word_in_sentence(sent: str) -> str:
    raise NotImplementedError


def clean_all_numbers(content: str) -> str:
    return re.sub(r'\d+', '', content)


# O(n)
# 判断是否是停用词
def is_stopwords(word: str) -> bool:
    stopwords_files = [os.path.join(root, "data/cn_stopwords.txt"), os.path.join(root, "data/hit_stopwords.txt"),
                       os.path.join(root, "data/scu_stopwords.txt")]
    stopwords = []
    for file in stopwords_files:
        stopwords += get_stopwords(file)
    return word in stopwords


# O(n)
def parse_words(str_content: str) -> list[str]:
    """
    :param str_content: 字符输入，建议输入句子级别的字符
    :return: 分词结果
    """
    word_generator = jieba.cut(str_content)
    return [w for w in word_generator if not is_stopwords(w)]


def extract_image_from_pdf_file(filepath: str, target_dir: str):
    raise NotImplementedError


def extract_image_bytes_from_pdf(filepath: str) -> list[bytes]:
    res = []
    pdf_file = fitz.open(filepath)
    for page_index in range(len(pdf_file)):

        # get the page itself
        page = pdf_file[page_index]
        image_list = page.getImageList()

        # printing number of images found in this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            print("[!] No images found on page", page_index)
        for image_index, img in enumerate(page.getImageList(), start=1):
            # get the XREF of the image
            xref = img[0]

            # extract the image bytes
            base_image = pdf_file.extractImage(xref)
            image_bytes = base_image["image"]
            res.append(image_bytes)
    return res


def extract_text_from_image(from_file: str, mode="chi_sim+eng") -> str:
    if from_file.split(".")[-1] not in ["jpg", "png", "jpeg"]:
        raise Exception("文件名不是图片")
    text = pytesseract.image_to_string(Image.open(from_file), lang=mode)
    assert type(text) == str
    return text


def extract_text_from_image_bytes(image_bytes: bytes, mode="chi_sim+eng") -> str:
    stream = BytesIO(image_bytes)
    text = pytesseract.image_to_string(Image.open(stream), lang=mode)
    assert type(text) == str
    return text


def save_to_file_image(file_name: str, content: bytes):
    with open(file_name, "wb") as f:
        f.write(content)


def save_to_file_text(file_name: str, content: str):
    with open(file_name, "a+", encoding="utf-8") as f:
        logging.info("写入文件：{}".format(file_name))
        f.write(content)
        f.write("\n")

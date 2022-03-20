import logging
import re
import fitz
import jieba
import subprocess


def parse_sentences(file_content: str) -> list:
    """
    :param file_content: 文件读出来的内容
    :return: 分句后的列表
    """
    sentences = re.split("(。|！|\!|\.|？|\?|\n)", file_content)
    return sentences


def parse_tokenization(str_content: str) -> list[str]:
    """
    :param str_content: 字符输入，建议输入句子级别的字符
    :return: 分词结果
    """
    word_generator = jieba.cut(str_content)
    return [w for w in word_generator]


def extract_image_from_pdf_file(filepath: str, target_dir: str):
    pass


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


def extract_text_from_image(from_file: str, to_file: str, mode="chi_sim+eng") -> subprocess.CompletedProcess:
    p = subprocess.run(["tesseract", from_file, to_file, "-l", mode], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode == 0:
        print("[+] Tesseract OCR Success")
        return p
    else:
        raise Exception(f"[-] Tesseract OCR Failed: {p.stderr.decode('utf-8')}")


def save_to_file_image(file_name: str, content: bytes):
    with open(file_name, "wb") as f:
        f.write(content)


def save_to_file_text(file_name: str, content: str):
    with open(file_name, "a+", encoding="utf-8") as f:
        logging.info("写入文件：{}".format(file_name))
        f.write(content)
        f.write("\n")

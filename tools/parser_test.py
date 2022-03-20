from pdfminer.high_level import extract_text
from tools.parser import *
import os

cur = os.path.abspath(os.path.dirname(__file__))
root = os.path.abspath(os.path.join(cur, '..'))


def test_should_get_sentences():
    data = os.path.join(root, 'test_data/明源云采招系统操作手册.pdf')
    file_content = extract_text(data)
    sentences = parse_sentences(file_content)
    assert type(sentences) == list
    if len(sentences) > 0:
        assert type(sentences[0]) == str


def test_should_get_tokenized_sentence():
    inputs = "这是一条测试语句"
    tokens = parse_tokenization(inputs)
    assert type(tokens) == list
    if len(tokens) > 0:
        assert type(tokens[0]) == str


def test_should_extract_image_successfully():
    filepath = os.path.join(root, 'test_data/明源云采招系统操作手册.pdf')
    bytes_list = extract_image_bytes_from_pdf(filepath)
    assert type(bytes_list) == list
    if len(bytes_list) > 0:
        assert type(bytes_list[0]) == bytes


def test_should_save_file_successfully():
    filepath = os.path.join(root, 'test_data/明源云采招系统操作手册.pdf')
    bytes_list = extract_image_bytes_from_pdf(filepath)
    filename = "test.png"
    save_to_file_image(filename, bytes_list[0])
    file = open(filename, 'rb')
    assert file.read() == bytes_list[0]


def test_should_run_command_successfully():
    # from_file = "../test_data/1.png"
    from_file = os.path.join(root, 'test_data/1.png')
    to_file = "test"
    res = extract_text_from_image(from_file, to_file)
    assert res.returncode == 0




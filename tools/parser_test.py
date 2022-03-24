import os
import pytest
from tools.parser import *
from pdfminer.high_level import extract_text


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
    tokens = parse_words(inputs)
    assert type(tokens) == list
    if len(tokens) > 0:
        assert type(tokens[0]) == str


def test_should_extract_image_successfully():
    filepath = os.path.join(root, 'test_data/明源云采招系统操作手册.pdf')
    bytes_list = extract_image_bytes_from_pdf(filepath)
    assert type(bytes_list) == list
    if len(bytes_list) > 0:
        assert type(bytes_list[0]) == bytes


@pytest.mark.skip(reason="not implemented")
def test_should_map_word_to_image_successfully():
    pass



def test_should_save_file_successfully():
    filepath = os.path.join(root, 'test_data/明源云采招系统操作手册.pdf')
    bytes_list = extract_image_bytes_from_pdf(filepath)
    filename = "test.png"
    save_to_file_image(filename, bytes_list[0])
    file = open(filename, 'rb')
    assert file.read() == bytes_list[0]


def test_should_extract_text_from_image_path_successfully():
    filepath = os.path.join(root, "test_data/1.png")
    text = extract_text_from_image(filepath)
    assert type(text) == str





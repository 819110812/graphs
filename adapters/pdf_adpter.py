from pdfminer.high_level import extract_text

from adapters.base_adapter import BaseAdapter


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

    def get_all_sentences_from_pdf(self) -> list[str]:
        pass


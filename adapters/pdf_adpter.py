from pdfminer.high_level import extract_text

from adapters.base_adapter import BaseAdapter


class PdfAdapter(BaseAdapter):
    def __init__(self, path: str):
        super().__init__(path)

    def get_content(self) -> str:
        pass

    def get_sentences(self) -> list:
        pass

    def extract_text_from_pdf(self) -> str:
        text = extract_text(self.path)
        return text

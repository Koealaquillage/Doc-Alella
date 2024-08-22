import fitz 
import mammoth 
import docx  

class FileTextLoader():
    def load_txt_files(self, files):
        data = []
        for file in files:
            with open(file.name, 'r') as f:
                data.append(f.read())
        return data

    def load_pdf_files(self, files):
        data = []
        for file in files:
            text = self._extract_text_from_pdf(file.name)
            data.append(text)
        return data

    def _extract_text_from_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def load_doc_files(self, files):
        data = []
        for file in files:
            text = self._extract_text_from_doc(file.name)
            data.append(text)
        return data

    def _extract_text_from_doc(self, doc_path):
        with open(doc_path, "rb") as doc_file:
            result = mammoth.convert_to_text(doc_file)
            return result.value

    def load_docx_files(self, files):
        data = []
        for file in files:
            text = self._extract_text_from_docx(file.name)
            data.append(text)
        return data

    def _extract_text_from_docx(self, docx_path):
        doc = docx.Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    def load_all_files(self, files):
        txt_files = [file for file in files if file.name.endswith('.txt')]
        pdf_files = [file for file in files if file.name.endswith('.pdf')]
        docx_files = [file for file in files if file.name.endswith('.docx')]
        doc_files = [file for file in files if file.name.endswith('.doc')]

        txt_data = self.load_txt_files(txt_files)
        pdf_data = self.load_pdf_files(pdf_files)
        docx_data = self.load_docx_files(docx_files)
        doc_data = self.load_doc_files(doc_files)

        all_data = txt_data + pdf_data + docx_data + doc_data
        return all_data
import fitz 
import mammoth 
import docx  

import fitz  # PyMuPDF
import mammoth
import docx

class FileTextLoader:

    def __init__(self):
        pass

    def load_txt_files(self, files):
        return self._load_files(files, self._read_txt)

    def load_pdf_files(self, files):
        return self._load_files(files, self._extract_text_from_pdf)

    def load_docx_files(self, files):
        return self._load_files(files, self._extract_text_from_docx)

    def load_doc_files(self, files):
        return self._load_files(files, self._extract_text_from_doc)

    def load_all_files(self, files):
        loaders = {
            '.txt': self.load_txt_files,
            '.pdf': self.load_pdf_files,
            '.docx': self.load_docx_files,
            '.doc': self.load_doc_files
        }

        all_data = []
        for ext, loader in loaders.items():
            filtered_files = [file for file in files if file.name.endswith(ext)]
            all_data.extend(loader(filtered_files))

        return all_data

    def _load_files(self, files, reader):
        data = []
        for file in files:
            try:
                data.append(reader(file.name))
            except Exception as e:
                print(f"Error reading {file.name}: {e}")
        return data

    def _read_txt(self, file_path):
        with open(file_path, 'r') as f:
            return f.read()

    def _extract_text_from_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def _extract_text_from_docx(self, docx_path):
        doc = docx.Document(docx_path)
        return "\n".join([para.text for para in doc.paragraphs])

    def _extract_text_from_doc(self, doc_path):
        with open(doc_path, "rb") as doc_file:
            result = mammoth.convert_to_text(doc_file)
            return result.value

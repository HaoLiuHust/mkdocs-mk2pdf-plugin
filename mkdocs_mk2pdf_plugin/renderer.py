
import pypandoc
from rst2pdf import createpdf
from PyPDF2 import PdfFileMerger

class Renderer(object):
    def __init__(self, combined: bool):
        self.combined = combined
        self.page_order = []
        self.pgnum = 0
        self.pages = []

    def write_pdf(self,  mk_filename: str, rst_filename: str, pdf_filename: str, style=None):
        pypandoc.convert_file(mk_filename,'rst',outputfile=rst_filename)
        if style is None:
            createpdf.main([rst_filename,pdf_filename])
        else:
            createpdf.main([rst_filename,pdf_filename,'-s',style])

    def add_doc(self, rel_path: str, abs_path: str):
        pos = self.page_order.index(rel_path)
        self.pages[pos] =  abs_path

    def write_combined_pdf(self, output_path: str):
        file_lst=[]
        pdf_merger = PdfFileMerger()
        for p in self.pages:
            if p is None:
                print('Unexpected error - not all pages were rendered properly')
                continue

            file_lst.append(open(p,'rb'))

        for f in file_lst:
            pdf_merger.append(f)

        with open(output_path,'wb') as f:
            pdf_merger.write(f)

        for f in file_lst:
            f.close()
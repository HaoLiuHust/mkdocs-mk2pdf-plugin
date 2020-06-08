import os
class Renderer(object):
    def __init__(self, combined: bool, template: str=""):
        self.combined = combined
        self.page_order = []
        self.pgnum = 0
        self.pages = []
        self.template=template

    def write_pdf(self,  mk_filename: str, pdf_filename: str):
        if os.path.isfile(self.template) and os.path.exists(self.template):
            os.system('pandoc --pdf-engine=xelatex --template=%s  %s -o %s'%(self.template,mk_filename,pdf_filename))
        else:
            os.system('pandoc --pdf-engine=xelatex %s -o %s'%(mk_filename,pdf_filename))

    def add_doc(self, rel_path: str, abs_path: str):
        try:
            pos = self.page_order.index(rel_path)
            self.pages[pos] =  abs_path
        except:
            pass

    def write_combined_pdf(self, output_path: str):
        combined_md=output_path.replace(".pdf",".md")

        with open(combined_md,'w') as f:
            for p in self.pages:
                if p is None:
                    print('Unexpected error - not all pages were rendered properly')
                    continue

                with open(p,'r') as rf:
                    lines=rf.readlines()
                    f.writelines(lines)
                    if not lines[-1].endswith('\n'):
                        f.write('\n')

        self.write_pdf(combined_md,output_path)
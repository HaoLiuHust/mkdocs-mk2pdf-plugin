import os
import sys
from timeit import default_timer as timer

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs import utils
import traceback
from .utils import modify_html

class MK2PdfPlugin(BasePlugin):
    config_scheme = (
        ('enabled_if_env', config_options.Type(utils.string_types)),
        ('combined', config_options.Type(bool, default=False)),
        ('combined_output_path', config_options.Type(utils.string_types, default="pdf/combined.pdf")),
        ('style_path', config_options.Type(utils.string_types, default=None))
    )

    def __init__(self):
        self.renderer = None
        self.enabled = True
        self.combined = False
        self.num_files = 0
        self.num_errors = 0
        self.total_time = 0

    def on_config(self, config):
        if 'enabled_if_env' in self.config:
            env_name = self.config['enabled_if_env']
            if env_name:
                self.enabled = os.environ.get(env_name) == '1'
                if not self.enabled:
                    print('PDF export is disabled (set environment variable {} to 1 to enable)'.format(env_name))
                    return

        self.combined = self.config['combined']
        if self.combined:
            print('Combined PDF export is enabled')

        from .renderer import Renderer
        self.renderer = Renderer(self.combined)

    def on_nav(self, nav, config, files):
        if not self.enabled:
            return nav

        self.renderer.pages = [None] * len(nav.pages)
        for page in nav.pages:
            self.renderer.page_order.append(page.file.src_path)

        return nav

    def on_post_page(self, output_content, page, config):
        if not self.enabled:
            return output_content

        start = timer()

        self.num_files += 1

        try:
            abs_dest_path = page.file.abs_dest_path
            src_path = page.file.src_path
        except AttributeError:
            # Support for mkdocs <1.0
            abs_dest_path = page.abs_output_path
            src_path = page.input_path

        site_dir=config.data['site_dir']
        path = os.path.dirname(abs_dest_path)

        rel_path=os.path.relpath(path,site_dir)
        pdf_path=os.path.join(site_dir,'pdf',rel_path,)
        rst_path=os.path.join(site_dir,'rst',rel_path)

        os.makedirs(pdf_path,exist_ok=True)
        os.makedirs(rst_path,exist_ok=True)

        filename = os.path.splitext(os.path.basename(src_path))[0]
        pdf_file = os.path.join(pdf_path,filename+".pdf")
        rst_file = os.path.join(rst_path,filename+".rst")

        try:
            if self.combined:
                self.renderer.add_doc(page.file.src_path, pdf_file)
                combined_pdf_path = self.config['combined_output_path']
                output_content = modify_html(output_content, os.path.join('pdf', combined_pdf_path),
                                             label=os.path.basename(combined_pdf_path))

            if self.config['style_path'] is not None:
                self.renderer.write_pdf(page.file.abs_src_path, rst_file,pdf_file,style=os.path.join(config.data['docs_dir'],self.config['style_path']))
            else:
                self.renderer.write_pdf(page.file.abs_src_path, rst_file,pdf_file)

            output_content = modify_html(output_content,os.path.join('pdf',rel_path,filename+".pdf"),label=filename+".pdf")

        except Exception as e:
            print('Error converting {} to PDF: {}'.format(src_path, e), file=sys.stderr)
            traceback.print_exc()
            self.num_errors += 1

        end = timer()
        self.total_time += (end - start)

        return output_content

    def on_post_build(self, config):
        if not self.enabled:
            return

        if self.combined:
            start = timer()

            abs_pdf_path = os.path.join(config['site_dir'], self.config['combined_output_path'])
            os.makedirs(os.path.dirname(abs_pdf_path), exist_ok=True)
            self.renderer.write_combined_pdf(abs_pdf_path)

            end = timer()
            self.total_time += (end - start)
            self.num_files+=1

        print('Converting {} files to PDF took {:.1f}s'.format(self.num_files, self.total_time))
        if self.num_errors > 0:
            print('{} conversion errors occurred (see above)'.format(self.num_errors))
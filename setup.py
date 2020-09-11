from setuptools import setup, find_packages
try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements

from os import path as os_path
this_directory = os_path.abspath(os_path.dirname(__file__))

def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [str(ir.req) for ir in reqs]

# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

setup(
    name='mkdocs-mk2pdf-plugin',
    version='0.1.6',
    description='An MkDocs plugin to export content pages as PDF files',
   
    long_description=read_file('README.md'), # 读取的Readme文档内容
    long_description_content_type="text/markdown",  # 指定包文档格式为markdown
    keywords='mkdocs pdf export',
    url='https://github.com/HaoLiuHust/mkdocs-mk2pdf-plugin',
    author='Liu, Hao',
    author_email='haoliuhust@hotmail.com',
    license='MIT',
    python_requires='>=3.4',
    install_requires=[
        'mkdocs>=1.1.2',
        'beautifulsoup4>=4.6.3',
    ],
    #install_requires=load_requirements("requirements.txt"),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'mk2pdf-export = mkdocs_mk2pdf_plugin.plugin:MK2PdfPlugin'
        ]
    }
)

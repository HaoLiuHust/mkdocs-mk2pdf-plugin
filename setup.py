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


def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding="utf-8") as f:
        long_description = f.read()
    return long_description


setup(
    name="mkdocs-pandoc-plugin",
    version="1.0.0",
    description="An MkDocs plugin to export content pages to any files that pandoc can handle",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    keywords="mkdocs pandoc export",
    url="https://github.com/alexandre-perrin/mkdocs-pandoc-plugin",
    author="Alexandre, Perrin",
    author_email="alexandreperr@gmail.com",
    license="MIT",
    python_requires=">=3.4",
    install_requires=load_requirements("requirements.txt"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    entry_points={"mkdocs.plugins": ["pandoc = mkdocs_pandoc.plugin:PandocPlugin"]},
)

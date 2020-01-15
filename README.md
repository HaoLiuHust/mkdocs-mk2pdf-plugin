# MkDocs PDF Export Plugin
*The plugin is based on https://github.com/zhaoterryy/mkdocs-pdf-export-plugin/ ,the main change is use rst2pdf to convert doc to PDFs which support PDF navigation, another change is add a download icon on the page*


*An MkDocs plugin to export content pages as PDF files*

The pdf-export plugin will export all markdown pages in your MkDocs repository as PDF files using pandoc and rst2pdf. The exported documents support many advanced features missing in most other PDF exports, such as PDF navigation.

## Requirements

1. This package requires MkDocs version 1.0 or higher (0.17 works as well)
2. Python 3.4 or higher
3. pandoc, rst2pdf and PyPDF2

## Installation

Install the package with pip:

```bash
pip install mkdocs-pdf-export-plugin
```

Enable the plugin in your `mkdocs.yml`:

```yaml
plugins:
    - search
    - mk2pdf-export
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [MkDocs documentation][mkdocs-plugins].

## Testing

When building your repository with `mkdocs build`, you should now see the following message at the end of your build output:

> Converting 17 files to PDF took 15.6s

In your `site_dir` you should now have a PDF file for every markdown page.

## Options

You may customize the plugin by passing options in `mkdocs.yml`:

```yaml
plugins:
    - mk2pdf-export:
        enabled_if_env: ENABLE_PDF_EXPORT
```

### `enabled_if_env`

Setting this option will enable the build only if there is an environment variable set to 1. This is useful to disable building the PDF files during development, since it can take a long time to export all files. Default is not set.

### `combined`

Setting this to `true` will combine all pages into a single PDF file. All download links will point to this file. Default is `false`.

### `combined_output_path`

This option allows you to use a different destination for the combined PDF file. Has no effect when `combined` is set to `false`. Default is `pdf/combined.pdf`.

### `style_path`

This option allows you to specify a custom rst2pdf style(refer to rst2pdf). This path must be **relative to your docs root** (See example below). Default is not set.

`mkdocs.yml`:
```yaml
plugins:
    - mk2pdf-export:
        style_path: chinese.style
```
```bash
project-root
├── docs
├── mkdocs.yml
├── site
.
.
```

## Contributing

From reporting a bug to submitting a pull request: every contribution is appreciated and welcome. Report bugs, ask questions and request features using [Github issues][github-issues].
If you want to contribute to the code of this project, please read the [Contribution Guidelines][contributing].

## Special thanks

Special thanks go to [Lukas Geiter][lukasgeiter] for developing the [mkdocs-awesome-pages-plugin][awesome-pages-plugin] which was used as a base and for convincing [Stephan Hauser][shauser] to write a plugin for this.
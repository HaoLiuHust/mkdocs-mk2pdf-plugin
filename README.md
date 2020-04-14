# Mkdoc Pandoc Plugin

*This plugin is based on https://github.com/HaoLiuHust/mkdocs-mk2pdf-plugin and aims to
use pandoc as a generic engine to convert to many document format that pandoc suports.*

*An MkDocs plugin to convert content pages to many format*

The plugin will use pandoc to export all markdown pages in your MkDocs repository.

## Requirements

1. This package requires MkDocs version 1.0 or higher (0.17 works as well)
2. Python 3.4 or higher
3. pandoc, xelatex(to support Chinese)
   ```
   sudo apt install pandoc
   sudo apt install texlive texlive-latex-extra texlive-latex-recommended texlive-xetex
   ```

## Installation

Install the package with pip:

```bash
pip install mkdocs-pandoc-plugin
```

Enable the plugin in your `mkdocs.yml`:

```yaml
plugins:
    - search
    - pandoc
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
    - pandoc:
        enabled_if_env: ENABLE_PDF_EXPORT
```

### `enabled_if_env`

Setting this option will enable the build only if there is an environment variable set to 1. This is useful to disable building the PDF files during development, since it can take a long time to export all files. Default is not set.

### `combined`

Setting this to `true` will combine all pages into a single PDF file. All download links will point to this file. Default is `false`.

### `combined_output_path`

This option allows you to use a different destination for the combined PDF file. Has no effect when `combined` is set to `false`. Default is `pdf/combined.pdf`.

### `pandoc_template`

This option allows you to use a custom pandoc template to convert markdown file to pdf files.

`mkdocs.yml`:
```yaml
plugins:
    - pandoc:
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

Special thanks go to [HaoLiuHust](https://github.com/haoliuhust) for developing the [mkdocs-mk2pdf-plugin](https://github.com/HaoLiuHust/mkdocs-mk2pdf-plugin).

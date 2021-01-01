import os
import logging
import contextlib

log = logging.getLogger("mkdocs.plugins.pandoc")


@contextlib.contextmanager
def run_in_path(p):
    saved = os.getcwd()
    os.chdir(p)
    try:
        yield p
    finally:
        os.chdir(saved)


class Pandoc(object):
    def __init__(self, in_file, out_file, work_dir, extra_args: str = "", **opts):
        self.opts = opts
        self.in_file = in_file
        self.out_file = out_file
        self.work_dir = work_dir
        self.extra_args = extra_args

    @property
    def args(self):
        args = []
        for opt, val in self.opts.items():
            opt = opt.replace("_", "-")
            log.debug(f"Pandoc arg: --{opt}={val}")
            args.append(f"--{opt}={val}")
        return args

    def write(self, *args):
        args = [self.extra_args] + list(args) + self.args
        self.run(args, "-o", self.out_file, self.in_file)

    def run(self, args, *argv):
        args = [args] if isinstance(args, str) else args
        args = ["pandoc"] + args + list(argv)
        command = " ".join(args)
        with run_in_path(self.work_dir):
            log.debug(f"{os.getcwd()}> {command}")
            os.system(command)


class Renderer(object):
    def __init__(
        self,
        combined: bool,
        docs_dir: str = "",
        extra_args: str = "",
        template: str = "",
        **args,
    ):
        self.combined = combined
        self.docs_dir = docs_dir
        self.page_order = []
        self.pgnum = 0
        self.pages = []
        self.args = args
        self.extra_args = extra_args

        if os.path.isfile(template) and os.path.exists(template):
            self.args["template"] = template

    def write_pandoc(self, mk_filename: str, out_filename: str):
        pandoc = Pandoc(
            mk_filename,
            out_filename,
            self.docs_dir,
            extra_args=self.extra_args,
            **self.args,
        )
        pandoc.write()

    def add_doc(self, rel_path: str, abs_path: str):
        try:
            pos = self.page_order.index(rel_path)
            self.pages[pos] = abs_path
        except:
            pass

    def write_combined_pandoc(self, output_path: str):
        combined_md = output_path + ".md"

        with open(combined_md, "w") as f:
            for p in self.pages:
                if p is None:
                    log.error("Unexpected error - not all pages were rendered properly")
                    continue

                with open(p, "r") as rf:
                    lines = rf.readlines()
                    f.writelines(lines)
                    if not lines[-1].endswith("\n"):
                        f.write("\n")
                    f.write("\n")

        self.write_pandoc(combined_md, output_path)

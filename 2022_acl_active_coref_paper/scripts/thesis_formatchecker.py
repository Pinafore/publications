"""
python3 formatchecker.py [-h] [--paper_type {long,short,other}] file_or_dir [file_or_dir ...]
"""

# TODO: make the script pip installable

import argparse
import json
from collections import defaultdict
from enum import Enum
from os import walk
from os.path import isfile, join

import pdfplumber
from termcolor import colored
from tqdm import tqdm


class Error(Enum):
    SIZE = "Size"
    PARSING = "Parsing"
    MARGIN = "Margin"
    SPELLING = "Spelling"
    FONT = "Font"
    PAGELIMIT = "Page Limit"


class Warn(Enum):
    BIB = "Bibliography"


class Page(Enum):
    # 595 pixels (72ppi) = 21cm
    WIDTH = 595
    # 842 pixels (72ppi) = 29.7cm
    HEIGHT = 842


class Margin(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    RIGHT = "right"
    LEFT = "left"


class Formatter(object):
    def __init__(self):
        # TODO: these should be constants
        self.right_offset = 4.5
        self.left_offset = 2
        self.top_offset = 1

    def format_check(self, submission, paper_type):
        print(f"Checking {submission}")

        # TOOD: make this less of a hackg
        self.number = submission.split("/")[-1].split("_")[0].replace(".pdf", "")
        self.pdf = pdfplumber.open(submission)
        self.logs = defaultdict(
            list
        )  # reset log before calling the format-checking functions
        self.page_errors = set()

        # TODO: A few papers take hours to check. Consider using a timeout
        self.check_page_size()
        self.check_page_margin()
        self.check_font()

        # TOOD: put json dump back on
        output_file = "errors-{0}.json".format(self.number)
        # string conversion for json dump
        logs_json = {}
        for k, v in self.logs.items():
            logs_json[str(k)] = v
        json.dump(
            logs_json, open(output_file, "w")
        )  # always write a log file even if it is empty
        if self.logs:
            print(f"Errors. Check {output_file} for details.")

        errors, warnings = 0, 0
        if self.logs.items():
            for e, ms in self.logs.items():
                for m in ms:
                    if isinstance(e, Error) and e != Error.PARSING:
                        print(colored("Error ({0}):".format(e.value), "red") + " " + m)
                        errors += 1
                    elif e == Error.PARSING:
                        print(
                            colored("Parsing Error:".format(e.value), "yellow")
                            + " "
                            + m
                        )
                    else:
                        print(
                            colored("Warning ({0}):".format(e.value), "yellow")
                            + " "
                            + m
                        )
                        warnings += 1

            # English nominal morphology
            error_text = "errors"
            if errors == 1:
                error_text = "error"
            warning_text = "warnings"
            if warnings == 1:
                warning_text = "warning"

            # display to user
            print()
            print(
                "We detected {0} {1} and {2} {3} in your paper.".format(
                    *(errors, error_text, warnings, warning_text)
                )
            )
            print(
                "In general, it is required that you fix errors for your paper to be published. Fixing warnings is optional, but recommended."
            )
            print(
                "Important: Some of the margin errors may be spurious. The library detects the location of images, but not whether they have a white background that blends in."
            )

        else:
            print(colored("All Clear!", "green"))

    def check_page_size(self):
        """Checks the paper size (A4) of each pages in the submission."""

        pages = []
        for i, page in enumerate(self.pdf.pages):

            if (round(page.width), round(page.height)) != (
                Page.WIDTH.value,
                Page.HEIGHT.value,
            ):
                pages.append(i + 1)
        for page in pages:
            error = "Page #{} is not A4.".format(page)
            self.logs[Error.SIZE] += [error]
        self.page_errors.update(pages)

    def check_page_margin(self):
        """Checks if any text or figure is in the margin of pages."""

        pages_image = defaultdict(list)
        pages_text = defaultdict(list)
        perror = []
        for i, p in enumerate(self.pdf.pages):
            if i + 1 in self.page_errors:
                continue
            try:
                # Parse images
                # 57 pixels (72ppi) = 2cm; 71 pixels (72ppi) = 2.5cm.
                for image in p.images:
                    violation = None
                    if float(image["top"]) < (57 - self.top_offset):
                        violation = Margin.TOP
                    elif float(image["x0"]) < (71 - self.left_offset):
                        violation = Margin.LEFT
                    elif Page.WIDTH.value - float(image["x1"]) < (
                        71 - self.right_offset
                    ):
                        violation = Margin.RIGHT

                    if violation:
                        pages_image[i] += [(image, violation)]

                # Parse texts
                for j, word in enumerate(p.extract_words()):
                    violation = None
                    if float(word["top"]) < (57 - self.top_offset):
                        violation = Margin.TOP
                    elif float(word["x0"]) < (71 - self.left_offset):
                        violation = Margin.LEFT
                    elif Page.WIDTH.value - float(word["x1"]) < (
                        71 - self.right_offset
                    ):
                        violation = Margin.RIGHT

                    if violation:
                        pages_text[i] += [(word, violation)]
            except:
                perror.append(i + 1)

        if perror:
            self.page_errors.update(perror)
            self.logs[Error.PARSING] = [
                "Error occurs when parsing page {}.".format(perror)
            ]

        if pages_text or pages_image:
            pages = sorted(set(pages_text.keys()).union(set((pages_image.keys()))))
            for page in pages:
                im = self.pdf.pages[page].to_image(resolution=150)
                for (word, violation) in pages_text[page]:

                    bbox = None
                    if violation == Margin.RIGHT:
                        self.logs[Error.MARGIN] += [
                            "Text on page {} bleeds into the right margin.".format(
                                page + 1
                            )
                        ]
                        bbox = (
                            Page.WIDTH.value - 80,
                            int(word["top"] - 20),
                            Page.WIDTH.value - 20,
                            int(word["bottom"] + 20),
                        )
                        im.draw_rect(bbox, fill=None, stroke="red", stroke_width=5)
                    elif violation == Margin.LEFT:
                        self.logs[Error.MARGIN] += [
                            "Text on page {} bleeds into the left margin.".format(
                                page + 1
                            )
                        ]
                        bbox = (20, int(word["top"] - 20), 80, int(word["bottom"] + 20))
                        im.draw_rect(bbox, fill=None, stroke="red", stroke_width=5)
                    elif violation == Margin.TOP:
                        self.logs[Error.MARGIN] += [
                            "Text on page {} bleeds into the top margin.".format(
                                page + 1
                            )
                        ]
                        bbox = (20, int(word["top"] - 20), 80, int(word["bottom"] + 20))
                        im.draw_rect(bbox, fill=None, stroke="red", stroke_width=5)
                    else:
                        # TODO: add bottom margin violations
                        pass

                for (image, violation) in pages_image[page]:

                    self.logs[Error.MARGIN] += [
                        "An image on page {} bleeds into the margin.".format(page + 1)
                    ]
                    bbox = (image["x0"], image["top"], image["x1"], image["bottom"])
                    im.draw_rect(bbox, fill=None, stroke="red", stroke_width=5)

                im.save(
                    "errors-{0}-page-{1}.png".format(*(self.number, page + 1)),
                    format="PNG",
                )
                # + "Specific text: "+str([v for k, v in pages_text.values()])]

    def check_font(self):
        """Check the font"""

        correct_fontname = "NimbusRomNo9L-Regu"
        fonts = defaultdict(int)
        for i, page in enumerate(self.pdf.pages):
            try:
                for char in page.chars:
                    fonts[char["fontname"]] += 1
            except:
                self.logs[Error.FONT] += [f"Can't parse page #{i+1}"]
        max_font_count, max_font_name = max(
            (count, name) for name, count in fonts.items()
        )  # find most used font
        sum_char_count = sum(fonts.values())
        # TODO: make this a command line argument
        if (
            max_font_count / sum_char_count < 0.35
        ):  # the most used font should be used more than 35% of the time
            self.logs[Error.FONT] += ["Can't find the main font"]

        if not max_font_name.endswith(
            correct_fontname
        ):  # the most used font should be `correct_fontname`
            self.logs[Error.FONT] += [
                f"Wrong font. The main font used is {max_font_name} when it should be {correct_fontname}."
            ]


args = None


def worker(pdf_path):
    """ process one pdf """
    Formatter().format_check(submission=pdf_path, paper_type=args.paper_type)


def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "submission_paths", metavar="file_or_dir", nargs="+", default=[]
    )
    parser.add_argument(
        "--paper_type", choices={"short", "long", "other"}, default="long"
    )
    parser.add_argument("--num_workers", type=int, default=1)

    args = parser.parse_args()

    # retrieve file paths
    paths = {
        join(root, file_name)
        for path in args.submission_paths
        for root, _, file_names in walk(path)
        for file_name in file_names
    }
    paths.update(args.submission_paths)

    # retrieve files
    fileset = sorted([p for p in paths if isfile(p) and p.endswith(".pdf")])

    if not fileset:
        print(f"No PDF files found in {paths}")

    if args.num_workers > 1:
        from multiprocessing.pool import Pool

        with Pool(args.num_workers) as p:
            list(tqdm(p.imap(worker, fileset), total=len(fileset)))
    else:
        # TODO: make the tqdm togglable
        # for submission in tqdm(fileset):
        for submission in fileset:
            worker(submission)


if __name__ == "__main__":
    main()

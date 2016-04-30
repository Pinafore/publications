Main Idea
================

In the interest of transparency and blind accessibility, we release the LaTeX
source of our publications along with the R/Python code to generate the figures
from the paper's data.

Organization
================

Each paper has its own directory of the form

> YEAR_VENUE_KEYWORDS

Year is the year of publication, venue is where it was published, and keywords
are some uniquely identifying terms (not always the title, which can sometimes
be more cutesy).

Compiling
================

To compile the PDF of a paper (e.g., 2015_naacl_qb_coref) run the command

> make 2015_naacl_qb_coref.paper.pdf

This generates the PDF, compiles the bibliography, and creates any figures
needed by the file.

Screenreaders
================

To use a screenreader to read the source, open the main file:

> 2015_naacl_qb_coref.tex

And then follow the input commands to find any included files.

Or you can go to the "sections" subdirectory within a paper and read the LaTeX
files in order (prefixed by number to help you read in order).

Requirements
================

To compile papers, you'll need pdflatex, Rscript, python, ruby, and bibtex.

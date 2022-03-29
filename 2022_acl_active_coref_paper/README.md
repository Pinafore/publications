# Installation
## LaTeX
To compile Latex locally, you need to install LaTeX distribution compatible with your system. We use [latexmk](https://mg.readthedocs.io/latexmk.html) to run LaTeX, which is included if you install MacTeX or MikTeX.
## Python
Create Python 3 virtual environment and install packages in `requirements.txt` either through pip or conda. 

# Compiling Papers
The main tex file for your paper is `YEAR_VENUE_NAME.tex`. 

Run `make YEAR_VENUE_NAME.pdf` to compile `YEAR_VENUE_NAME.tex` with latexmk.

Other useful commands from Makefile include: `make clean`, `make NAME.arxiv.tgz` (for arxiv submissions).

## Generate figures
When you make your paper, it will automatically run `figures.py`	to generate figures from `data` and place them in `auto_fig`. These figures in `auto_fig` will not be tracked by Git. 

# Collaborating with Others
## Token Tracking
**At all times, only one person should be editing a file to avoid merge conflicts!!!**

Use the token tracking sheet to indicate who is working on which section: [https://docs.google.com/spreadsheets/d/1wPZ4M7FGIYyMbGIsYil23qT2mfW-RecyY2-Nl5hW5Mo/edit?usp=sharing](https://docs.google.com/spreadsheets/d/1wPZ4M7FGIYyMbGIsYil23qT2mfW-RecyY2-Nl5hW5Mo/edit?usp=sharing)

If the cell is empty, you may fill your initial and work on the section. After you are finished, push all changes and remove your initial. 

## Share individual paper repos
The advantage of this modular system and github submodules is that the external collaborators don't need to clone the entire `papers` repository. You may just share the individual paper repository with them.

## Sync with Overleaf
1. On Overleaf, log into your Github account and import your individual paper repository. Overleaf will automatically create a copy that is synced with this Github repository.
2. On Overleaf, you can directly push and pull commits.
3. **Overleaf users must make sure no one else is working on paper offline and that they have pulled all the most recent commits. After they are done, they must make sure to push everything. Use token tracking to coordinate.**

### Generate figures
Figures can't be generated on Overleaf. In this case, authors must make sure all generated figures are committed. You can place final versions of figures in `auto_fig` into `figures` (or choose to put them in a separate directory). 

Currently, `graphicspath` in the main tex file points to `figures` first and then `auto_fig`. Modify this line to make sure that final versions of figures will committed and successfully compiled for Overleaf users.


TEX = $(wildcard *.tex */*.tex)
BIB = $(wildcard *.bib)
#FIG = $(wildcard */figures.*)

clean:
	rm -f *.aux *.log *.bbl *~ *.out *.nav *.toc *.snm *.blg *.fls *.fdb_latexmk
	rm -fR auto_fig

#auto_fig: figures.py
	#mkdir -p auto_fig
	#python figures.py

%.pdf: %.tex $(TEX) auto_fig
	latexmk -pdf -pv $*

slides:
	mkdir slides
	cp template.tex title.tex thanks.tex references.tex beamerthemeUFG.sty Makefile slides
	cp -a lib slides

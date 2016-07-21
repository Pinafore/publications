
TEX = $(wildcard */sections/*.tex *.tex */*.tex)
GFX = $(wildcard */figures/*.*)
DATA = $(wildcard */data/*.*)
BIB = $(wildcard bib/*.bib)

%.tgz: %.tex
	tar cvfz $(<:.tex=.tgz) Makefile style/*.sty style/*.bst style/*.cls $(<:.tex=.tex) bib/*.bib style/preamble.tex $(<:.tex=)/*.png $(<:.tex=)/*.pdf $(<:.tex=)/*.tex

clean:
	rm -f *.aux *.dvi *.log *.bbl *.pdf *~ *.out *.blg
	rm -f */*.aux */*.dvi */*.log */*.bbl */*.pdf */*~ */*.out */*.blg */*/*~
	rm -fR */auto_fig

%.bbl: $(BIB) $(TEX)
	pdflatex $*
	bibtex $*

%/figures.R:
	touch $@

%/auto_fig/res.txt: %/figures.R
	mkdir -p $(<:figures.R=auto_fig)
	Rscript $< > $@

# %.tex needs to be the first dependency or it will cause an error
%.paper.pdf: %.tex %/auto_fig/res.txt %.bbl $(GFX)
	pdflatex $*
	pdflatex $*
	mkdir -p ~/public_html/temp
	cp $(<:.tex=.pdf) $@
	cp $@ ~/public_html/temp
	./scripts/style-check.rb $(<:.tex=)/*.tex $(<:.tex=)/sections/*.tex

# cd $(<:.paper.pdf=)/supporting && pdflatex summary
%.nsf.pdf: %.paper.pdf
	cd $(<:.paper.pdf=)/supporting && pdflatex facilities
	cd $(<:.paper.pdf=)/supporting && pdflatex jbg_bio
	cd $(<:.paper.pdf=)/supporting && pdflatex collaborators
	cd $(<:.paper.pdf=)/supporting && pdflatex data_plan
	cd $(<:.paper.pdf=)/supporting && pdflatex justification
	cd $(<:.paper.pdf=)/supporting && pdflatex jbg_current_and_pending
	mkdir -p $(<:.paper.pdf=)/output
	mv $(<:.paper.pdf=)/supporting/*.pdf $(<:.paper.pdf=)/output
	scripts/split_pdf.py $< 15
	mv $(<:.paper.pdf=).paper.part*.pdf $(<:.paper.pdf=)/output
	wc $(<:.paper.pdf=)/supporting/summary.txt
	cat $(<:.paper.pdf=)/supporting/summary.txt
	cp $(<:.paper.pdf=)/supporting/summary.txt $(<:.paper.pdf=)/output

%.paper.ps: %.tex %.bbl style/preamble.tex $(TEX) $(GFX)
	latex $<
	latex $<
	mkdir -p ~/public_html/temp
	dvips $(<:.tex=.dvi) -t letter
	mv $(<:.tex=.ps) $@
	cp $@ ~/public_html/temp

# We don't want make to delete bibliography files or the figures, so we need this rule
.SECONDARY:

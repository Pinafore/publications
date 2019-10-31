
TEX = $(wildcard */sections/*.tex *.tex */*.tex */tables/*.tex)
BIB = $(wildcard bib/*.bib)
FIG = $(wildcard */figures.*)

clean:
	rm -f *.aux *.dvi *.log *.bbl *.pdf *~ *.out *.blg *.nav *.toc *.snm *.fdb_latexmk *.fls *.synctex.gz
	rm -f */*.aux */*.dvi */*.log */*.bbl */*.pdf */*~ */*.out */*.blg */*/*~
	rm -fR */auto_fig
	rm -R *.tgz

%/auto_fig/res.txt: $(FIG)
	mkdir -p $(@:/res.txt=)
	./scripts/rscript_if_ne.sh $(@:/auto_fig/res.txt=) > $@

%.pdf: %/auto_fig/res.txt %.tex $(TEX)
	pdflatex $*

%.bbl: %.pdf $(BIB)
	bibtex $*

%.paper.pdf: %.pdf %.bbl 
	pdflatex $*
	pdflatex $*
	cp $(<:.tex=.pdf) $@
	cp $@ ~/public_html/temp || true
	./scripts/style-check.rb $(<:.tex=)/*.tex $(<:.tex=)/sections/*.tex

2020_aaai_sense.appendix.pdf: 2020_aaai_sense.paper.pdf
	python scripts/split_pdf.py 2020_aaai_sense.paper.pdf 8
	mv 2020_aaai_sense_page_8.pdf 2020_aaai_sense.appendix.pdf
	mv 2020_aaai_sense_page_0.pdf 2020_aaai_sense.submission.pdf


# cd $(<:.paper.pdf=)/supporting && pdflatex summary
%.nsf.pdf: %.paper.pdf
	cd $(<:.paper.pdf=)/supporting && pdflatex jbg_bio
	cd $(<:.paper.pdf=)/supporting && pdflatex collaborators
	cd $(<:.paper.pdf=)/supporting && pdflatex data_plan
	cd $(<:.paper.pdf=)/supporting && pdflatex jbg_current_and_pending
	mkdir -p $(<:.paper.pdf=)/output
	mv $(<:.paper.pdf=)/supporting/*.pdf $(<:.paper.pdf=)/output
	rm -f *.part*.*.pdf
	/usr/bin/python -E scripts/split_pdf.py $< 8 9 10 12
	mv $(<:.paper.pdf=).paper.part1.1_8.pdf $(<:.paper.pdf=)/output/project_description.pdf
	mv $(<:.paper.pdf=).paper.part2.9_9.pdf $(<:.paper.pdf=)/output/summary.pdf
	mv $(<:.paper.pdf=).paper.part3.10_10.pdf $(<:.paper.pdf=)/output/data_plan.pdf
	mv $(<:.paper.pdf=).paper.part4.11_12.pdf $(<:.paper.pdf=)/output/collaboration_plan.pdf
	mv $(<:.paper.pdf=).paper.part5.*.pdf $(<:.paper.pdf=)/output/works_cited.pdf

%.tgz: %.bbl
	tar cvfz $(<:.bbl=.tgz) Makefile $< style/*.sty style/*.bst style/*.cls $(<:.bbl=.tex) bib/*.bib style/preamble.tex $(<:.bbl=)/figures/* $(<:.bbl=)/auto_fig/* $(<:.bbl=)/sections/*.tex

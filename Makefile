TEX = $(wildcard */sections/*.tex *.tex */*.tex)
GFX = $(wildcard */figures/*.*)
DATA = $(wildcard */data/*.*)
BIB = $(wildcard bib/*.bib)
FIG = $(wildcard */figures.R */figures.py)

%.tgz: %.tex
	tar cvfz $(<:.tex=.tgz) Makefile style/*.sty style/*.bst style/*.cls $(<:.tex=.tex) bib/*.bib style/preamble.tex $(<:.tex=)/*.png $(<:.tex=)/*.pdf $(<:.tex=)/*.tex

clean:
	rm -f *.aux *.dvi *.log *.bbl *.pdf *~ *.out *.blg *.nav *.toc *.snm *.fdb_latexmk *.fls *.synctex.gz
	rm -f */*.aux */*.dvi */*.log */*.bbl */*.pdf */*~ */*.out */*.blg */*/*~
	rm -fR */auto_fig

%.bbl: $(BIB) $(TEX)
	pdflatex $*
	bibtex $*

%/figures.R:
	touch $@

%/auto_fig:
	mkdir -p $@

%/auto_fig/res.txt: %/auto_fig $(DATA) $(FIG)
	./scripts/rscript_if_ne.sh $(<:/auto_fig=) > $@

# %.tex needs to be the first dependency or it will cause an error
%.paper.pdf: %.tex %/auto_fig/res.txt %.bbl $(GFX)
	pdflatex $*
	pdflatex $*
	cp $(<:.tex=.pdf) $@
	cp $@ ~/public_html/temp || true
	./scripts/style-check.rb $(<:.tex=)/*.tex $(<:.tex=)/sections/*.tex

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

%.paper.ps: %.tex %.bbl style/preamble.tex $(TEX) $(GFX)
	latex $<
	latex $<
	mkdir -p ~/public_html/temp
	dvips $(<:.tex=.dvi) -t letter
	mv $(<:.tex=.ps) $@
	cp $@ ~/public_html/temp

# We don't want make to delete bibliography files or the figures, so we need this rule
.SECONDARY:

# Specific rules for individual conferences / papers

2019_emnlp_gumbel_sense.appendix.pdf: 2019_emnlp_gumbel_sense.paper.pdf
	python scripts/split_pdf.py 2019_emnlp_gumbel_sense.paper.pdf 11
	mv 2019_emnlp_gumbel_sense_page_11.pdf 2019_emnlp_gumbel_sense.appendix.pdf
	mv 2019_emnlp_gumbel_sense_page_0.pdf 2019_emnlp_gumbel_sense.submission.pdf

emnlp: 2019_emnlp_clime.paper.pdf 2019_emnlp_diplomacy.paper.pdf 2019_emnlp_graph_clwe.paper.pdf 2019_emnlp_influence.paper.pdf 2019_emnlp_qbaudio.paper.pdf 2019_emnlp_zero.paper.pdf 2019_emnlp_sequentialqa.paper.pdf 2019_emnlp_gumbel_sense.paper.pdf 2019_emnlp_gumbel.appendix.pdf

acl: 2019_acl_modularity.paper.pdf 2019_acl_flipside.paper.pdf 2019_acl_clwe.paper.pdf
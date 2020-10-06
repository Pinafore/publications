TEX = $(wildcard */sections/*.tex *.tex */*.tex */tables/*.tex)
BIB = $(wildcard bib/*.bib)
FIG = $(wildcard */figures.*)

clean:
	rm -f *.aux *.dvi *.log *.bbl *.pdf *~ *.out *.blg *.nav *.toc *.snm *.fdb_latexmk *.fls *.synctex.gz
	rm -f */*.aux */*.dvi */*.log */*.bbl */*.pdf */*~ */*.out */*.blg */*/*~
	rm -fR */auto_fig
	rm -fR *.tgz

.PRECIOUS: %/auto_fig/res.txt

clean_proposal:
	rm -f *.aux *.dvi *.log *.bbl *.pdf *~ *.out *.blg *.nav *.toc *.snm *.fdb_latexmk *.fls *.synctex.gz
	rm -f pedro_proposal/*.aux pedro_proposal/*.dvi pedro_proposal/*.log pedro_proposal/*.bbl pedro_proposal/*.pdf pedro_proposal/*~ pedro_proposal/*.out pedro_proposal/*.blg pedro_proposal/*/*~
	rm -fR pedro_proposal/auto_fig
	mkdir -pp pedro_proposal/auto_fig

scripts/hunspell_dictionary.dic: scripts/dictionary.txt
	wc -l $< > $@
	sort $< | uniq >> $@

%.spell: %.pdf scripts/hunspell_dictionary.dic
	python3 scripts/spell.py --files $(<:.pdf=)/*.tex $(<:.pdf=)/sections/*.tex

# TODO: make it so that this actually runs if the figure file (R or python) or data are updated.  Perhaps requires messing with the script.
%/auto_fig/res.txt: %/figures.py
	mkdir -p $(@:/res.txt=)
	./scripts/rscript_if_ne.sh $(@:/auto_fig/res.txt=) > $@

%.pdf: %/auto_fig/res.txt %.tex $(TEX)
	pdflatex $*

%.bbl: %.pdf $(BIB)
	bibtex $*

%.paper.pdf: %.pdf %.bbl
	pdflatex $*
	pdflatex -halt-on-error $*
	cp $< $@
	cp $@ ~/public_html/temp || true
	./scripts/style-check.rb $(<:.pdf=)/*.tex $(<:.pdf=)/sections/*.tex

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


# These targets should remain in sync (e.g., if you fix one, do the same for the other).  Except for the .tgz target should have all the bib files but the arxiv target should have the bbl file ($<)
%.tgz: %.bbl
	tar cvfz $@ Makefile style/*.sty style/*.bst style/*.cls $(<:.bbl=.tex) bib/*.bib style/*.tex $(<:.bbl=)/figures/* $(<:.bbl=)/auto_fig/* $(<:.bbl=)/sections/*.tex

%.arxiv.tgz: %.bbl
	tar cvfz $@ Makefile $< style/*.sty style/*.bst style/*.cls $(<:.bbl=.tex) style/*.tex $(<:.bbl=)/figures/* $(<:.bbl=)/auto_fig/* $(<:.bbl=)/sections/*.tex

2020_emnlp_metaanswer.appendix.pdf: 2020_emnlp_metaanswer.paper.pdf
	python3 scripts/split_pdf.py 2020_emnlp_metaanswer.paper.pdf 10
	mv 2020_emnlp_metaanswer_page_10.pdf 2020_emnlp_metaanswer.appendix.pdf
	mv 2020_emnlp_metaanswer_page_0.pdf 2020_emnlp_metaanswer.submission.pdf

2020_emnlp_qa_fairness.appendix.pdf: 2020_emnlp_qa_fairness.paper.pdf
	python3 scripts/split_pdf.py 2020_emnlp_qa_fairness.paper.pdf 6
	mv 2020_emnlp_qa_fairness_page_6.pdf 2020_emnlp_qa_fairness.appendix.pdf
	mv 2020_emnlp_qa_fairness_page_0.pdf 2020_emnlp_qa_fairness.submission.pdf

2020_emnlp_simint.appendix.pdf: 2020_emnlp_simint.paper.pdf
	python3 scripts/split_pdf.py 2020_emnlp_simint.paper.pdf 5
	mv 2020_emnlp_simint_page_5.pdf 2020_emnlp_simint.appendix.pdf
	mv 2020_emnlp_simint_page_0.pdf 2020_emnlp_simint.submission.pdf


acl: 2020_acl_clime.paper.pdf 2020_acl_diplomacy.paper.pdf 2020_acl_refine_clwe.paper.pdf 2020_acl_trivia_tournament.appendix.pdf 

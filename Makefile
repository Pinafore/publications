TEX = $(wildcard */sections/*.tex *.tex */*.tex */tables/*.tex)
BIB = $(wildcard bib/*.bib)
FIG = $(wildcard */figures.*)

.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

clean:
	rm -f *.aux *.dvi *.log *.bbl *.pdf *~ *.out *.blg *.nav *.toc *.snm *.fdb_latexmk *.fls *.synctex.gz
	rm -f */*.aux */*.dvi */*.log */*.bbl */*.pdf */*~ */*.out */*.blg */*/*~
	rm -fR */auto_fig
	rm -fR *.tgz

.PRECIOUS: %/auto_fig/res.txt

clean_proposal:
	rm -f *.aux *.dvi *.log *.bbl *.pdf *~ *.out *.blg *.nav *.toc *.snm *.fdb_latexmk *.fls *.synctex.gz
	rm -f pedro_thesis/*.aux pedro_thesis/*.dvi pedro_thesis/*.log pedro_thesis/*.bbl pedro_thesis/*.pdf pedro_thesis/*~ pedro_thesis/*.out pedro_thesis/*.blg pedro_thesis/*/*~
	rm -fR pedro_thesis/auto_fig
	mkdir -pp pedro_thesis/auto_fig

scripts/hunspell_dictionary.dic: scripts/dictionary.txt
	wc -l $< > $@
	sort $< | uniq >> $@

%.spell: %.pdf scripts/hunspell_dictionary.dic
	python3 scripts/spell.py --files $(<:.pdf=)/*.tex $(<:.pdf=)/sections/*.tex

# TODO: make it so that this actually runs if the figure file (R or python) or data are updated.  Perhaps requires messing with the script.
%/auto_fig/res.txt: %/figures.py
	mkdir -p $(@:/res.txt=)
	out=$$(./scripts/rscript_if_ne.sh $(@:/auto_fig/res.txt=)) && echo "$$out" > $@

%.pdf: %/auto_fig/res.txt %.tex $(TEX)
	pdflatex $*

%.bbl: %.pdf $(BIB)
	bibtex $*

%.paper.pdf: %.pdf %.bbl
	pdflatex $*
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

2021_emnlp_qa_fairness.appendix.pdf: 2021_emnlp_qa_fairness.paper.pdf
	python3 scripts/split_pdf.py 2021_emnlp_qa_fairness.paper.pdf 6
	mv 2021_emnlp_qa_fairness_page_6.pdf 2021_emnlp_qa_fairness.appendix.pdf
	mv 2021_emnlp_qa_fairness_page_0.pdf 2021_emnlp_qa_fairness.submission.pdf

2021_emnlp_simint.appendix.pdf: 2021_emnlp_simint.paper.pdf
	python3 scripts/split_pdf.py 2021_emnlp_simint.paper.pdf 5
	mv 2021_emnlp_simint_page_5.pdf 2021_emnlp_simint.appendix.pdf
	mv 2021_emnlp_simint_page_0.pdf 2021_emnlp_simint.submission.pdf

2021_emnlp_paradigms.submission.pdf: 2021_emnlp_paradigms.paper.pdf
	python3 scripts/split_pdf.py 2021_emnlp_paradigms.paper.pdf 10
	mv 2021_emnlp_paradigms_page_0.pdf 2021_emnlp_paradigms.submission.pdf

2021_emnlp_paradigms.appendix.pdf: 2021_emnlp_paradigms.submission.pdf
	mv 2021_emnlp_paradigms_page_10.pdf 2021_emnlp_paradigms.appendix.pdf

2021_emnlp_adaptation.appendix.pdf: 2021_emnlp_adaptation.paper.pdf
	python3 scripts/split_pdf.py 2021_emnlp_adaptation.paper.pdf 6
	mv 2021_emnlp_adaptation_page_6.pdf 2021_emnlp_adaptation.appendix.pdf
	mv 2021_emnlp_adaptation_page_0.pdf 2021_emnlp_adaptation.submission.pdf

2021_neurips_topics.appendix.pdf: 2021_neurips_topics.paper.pdf
	python3 scripts/split_pdf.py 2021_neurips_topics.paper.pdf 15
	mv 2021_neurips_topics_page_15.pdf 2021_neurips_topics.appendix.pdf
	mv 2021_neurips_topics_page_0.pdf 2021_neurips_topics.submission.pdf

2021_acl_leaderboard.submission.pdf: 2021_acl_leaderboard.paper.pdf
	python3 scripts/split_pdf.py 2021_acl_leaderboard.paper.pdf 14
	mv 2021_acl_leaderboard_page_0.pdf 2021_acl_leaderboard.submission.pdf

2021_acl_leaderboard.appendix.pdf: 2021_acl_leaderboard.submission.pdf
	mv 2021_acl_leaderboard_page_14.pdf 2021_acl_leaderboard.appendix.pdf

annotated_squad_examples.pdf:
	latexmk -pdf 2021_acl_leaderboard/supplementary.tex
	mv supplementary.pdf annotated_squad_examples.pdf

2021_acl_leaderboard.supplementary.zip: 2021_acl_leaderboard/data/label-studio.json annotated_squad_examples.pdf
	mkdir -p /tmp/papers-tmp/supplementary/
	cp 2021_acl_leaderboard/data/label-studio.json /tmp/papers-tmp/supplementary
	cp 2021_acl_leaderboard/examples.toml /tmp/papers-tmp/supplementary
	cp 2021_acl_leaderboard/squad-annotation-instructions.pdf /tmp/papers-tmp/supplementary
	cp annotated_squad_examples.pdf /tmp/papers-tmp/supplementary
	zip -j -r 2021_acl_leaderboard.supplementary.zip /tmp/papers-tmp/supplementary

leaderboard: 2021_acl_leaderboard.paper.pdf 2021_acl_leaderboard.submission.pdf 2021_acl_leaderboard.appendix.pdf 2021_acl_leaderboard.supplementary.zip


paradigms: 2021_emnlp_paradigms.submission.pdf 2021_emnlp_paradigms.appendix.pdf




acl: 2020_acl_clime.paper.pdf 2020_acl_diplomacy.paper.pdf 2020_acl_refine_clwe.paper.pdf 2020_acl_trivia_tournament.appendix.pdf

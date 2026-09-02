PDF=main.pdf
all: $(PDF)
$(PDF): main.tex refs.bib aaai2026.sty aaai2026.bst $(wildcard figs/*.pdf)
	latexmk -pdf -bibtex main.tex
arxiv.zip: $(PDF)
	zip -r arxiv.zip main.tex refs.bib aaai2026.sty aaai2026.bst figs/ -x "*.git*"
clean:
	latexmk -C; rm -f *.aux *.bbl *.blg *.log *.out *.fls *.fdb_latexmk

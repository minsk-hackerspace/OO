%.pdf: %.ps
	ps2pdf $<

%.ps: %.dvi
	dvips $<

%.dvi: %.tex
	latex $<
	# generate pdf index
	latex $<

%.tex: %.md md2tex.py md2tex/* 
	./md2tex.py < $< > $@

SRC := constitution.md

all: $(SRC:.md=.pdf) $(SRC:.md=.tex)

clean:
	rm -f *.pdf *.log *.aux *.dvi *.ps *.out *.tex constitution.tex

remake: clean all

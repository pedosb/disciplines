#####
# Autor: Pedro Batista
# Data: 10/04/2011
#####

LATEX = latex
BIBTEX = bibtex
DVIPDF = dvipdf
RM = rm -f

MAIN = anteprojeto
TARGET = $(MAIN).pdf
DVI = $(MAIN).dvi

SOURCE = anteprojeto.tex \
		 ufpaanteprojeto.cls \
		 bibliografia.bib

all : $(TARGET)

$(TARGET) : $(DVI)
	$(DVIPDF) $(MAIN)

$(DVI) : $(SOURCE)
	$(LATEX) $(MAIN)
	-$(BIBTEX) $(MAIN)
	$(LATEX) $(MAIN)
	$(LATEX) $(MAIN)

clean :
	$(RM) *.aux *.bbl *.blg *.dvi *.log *~

distclean :
	$(RM) $(TARGET)

#####
# Autor: Pedro Batista
# Data: 10/04/2011
#####

LATEX = latex -shell-escape
BIBTEX = bibtex
DVIPDF = dvipdf
RM = rm -f

MAIN = main
TARGET = $(MAIN).pdf
DVI = $(MAIN).dvi

SOURCE = $(MAIN).tex \
		 makefile \
		 *.eps

all : $(TARGET)

$(TARGET) : $(DVI)
	$(DVIPDF) $(MAIN)

$(DVI) : $(SOURCE)
	$(LATEX) $(MAIN)
	-$(BIBTEX) $(MAIN)
	$(LATEX) $(MAIN)
	$(LATEX) $(MAIN)

clean :
	$(RM) *.aux *.bbl *.blg *.dvi *.log *~ *.pyg *.lof *.lot *.toc

distclean :
	$(RM) $(TARGET)

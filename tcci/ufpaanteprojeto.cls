%%%%%
% Autor: Pedro Batista - pedro@ufpa.br
% Data: 10/04/2010
%%%%%

%%%%%
% Deve ser usando como:
% \documentclass{ufpaanteprojeto}
% \usepackage{multirow}
% \usepackage[table]{xcolor}
% 
% \titulo{título}
% \autor{autor}
% \orientador{Orientador}
% \coorientador{Coorientador} %Opcional
% \linhapesquisa{Linha de Pesquisa}
% \section{Resumo}
% \section{Objetivos}
% \section{Justificativa}
% \section{Relevância do estudo}
% \section{Problema da pesquisa a ser investigado}
% \section{Metas}
% \section{Metodologia}
% \section{Cronograma de execução}
% \begin{table}[htp]
% 	\centering
% 	\begin{tabular}{|p{8cm}|c|c|c|c|c|c|}
% 		\hline
% 		\multirow{2}{*}{\textbf{Atividades}} & \multicolumn{6}{|c|}{\textbf{Meses de execução TCC I}} \\\cline{2-7}
% 		& 01 & 02 & 03 & 04 & 05 & 06 \\\hline
% 		Atividade X & \cellcolor{black} & & & & & \\\hline
% 	\end{tabular}
% 	\caption{Cronograma de execução do TCC I}
% 	\label{tab:cronogramatcci}
% \end{table}
% 
% \begin{table}[htp]
% 	\centering
% 	\begin{tabular}{|p{8cm}|c|c|c|c|c|c|}
% 		\hline
% 		\multirow{2}{*}{\textbf{Atividades}} & \multicolumn{6}{|c|}{\textbf{Meses de execução TCC II}} \\\cline{2-7}
% 		& 01 & 02 & 03 & 04 & 05 & 06 \\\hline
% 		Atividade X & \cellcolor{black} & & & & & \\\hline
% 	\end{tabular}
% 	\caption{Cronograma de execução do TCC II}
% 	\label{tab:cronogramatccii}
% \end{table}
% \bibliographystyle{plain}
% \bibliography{bibliografia}
%%%%%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ufpaanteprojeto}[10/04/2011 v0.1 Baseado em RESOLU??O EngComp 02/ 2008 - DE 05 de setembro de 2008]

\LoadClass[12pt,a4paper]{article}
%\RequirePackage[inner=30mm,outer=20mm,bottom=20mm]{geometry}
\RequirePackage[brazil]{babel}
%Fonte arial
\renewcommand{\rmdefault}{phv}

\RequirePackage[latin1]{inputenc}
\RequirePackage{ifthen}

\newcommand{\defspace}{\\[8pt]}

\newcommand*{\@titulo}{}
\newcommand*{\titulo}[1]{\renewcommand*{\@titulo}{#1}}

\newcommand*{\@autor}{}
\newcommand*{\autor}[1]{\renewcommand*{\@autor}{#1}}

\newcommand*{\@orientador}{}
\newcommand*{\orientador}[1]{\renewcommand*{\@orientador}{#1}}

\newcommand*{\@coorientador}{}
\newcommand*{\coorientador}[1]{\renewcommand*{\@coorientador}{#1}}

\newcommand*{\@linhapesquisa}{}
\newcommand*{\linhapesquisa}[1]{\renewcommand*{\@linhapesquisa}{#1}}

\newcommand{\fazercapa}{
	\singlespacing
	{
	\Large
	\begin{center}
		\textbf{Relatório de Trabalho de Conclusão de Curso I} \\
	\end{center}
	}

	{
	\noindent
	\textbf{Título do projeto de pesquisa:} \\
	\@titulo \defspace
	\textbf{Aluno:} \\
	\@autor \defspace
	\textbf{Orientador:} \\
	\@orientador \defspace
	\ifthenelse{\equal{\@coorientador}{}}{}{
	\textbf{Co-orientador:} \\
	\@coorientador \defspace
	}
	\textbf{Linha de pesquisa:} \\
	\@linhapesquisa
	}
}

\AtEndDocument{
%\vspace{30pt}
\begin{noindent}
\begin{center}
\rule{10cm}{0.2mm}\\
\textbf{Orientador:} \@orientador

%\vspace{30pt}
\vspace{13pt}
\ifthenelse{\equal{\@coorientador}{}}{}{
\rule{10cm}{0.2mm}\\
\textbf{Co-orientador:} \@coorientador
}

%\vspace{30pt}
\vspace{13pt}
\rule{10cm}{0.2mm}\\
\textbf{Aluno:} \@autor
\end{center}

\begin{flushright}
%\vspace{30pt}
\vspace{5pt}
Belém do Pará, \rule{1.3cm}{0.2mm} de \rule{4cm}{0.2mm} de \rule{2.6cm}{0.2mm}
\end{flushright}
\end{noindent}
}

%a4 size 21cm x 29.7cm
%header 3cm
\setlength{\topmargin}{0pt}
\setlength{\voffset}{-2.3cm}%0.24cm
\setlength{\headsep}{0.24cm}%0.24cm
\setlength{\headheight}{2.52cm}
%right 3cm
\setlength{\hoffset}{-1.04cm}%1.5cm
\setlength{\oddsidemargin}{1.5cm}%1.5cm
\addtolength{\marginparsep}{-10pt}
\setlength{\marginparsep}{0.35cm}
\setlength{\marginparwidth}{2.7cm}%2.7cm
%footer 2cm
\setlength{\footskip}{1.25cm}
%left 2cm
\setlength{\textwidth}{16cm}
\setlength{\textheight}{24.7cm}

\RequirePackage{fancyhdr}
\pagestyle{fancy}
% remove everything 
\fancyhf{}
% remove lines as well
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\fancyfoot[CEO]{\thepage}

%\fancyhead{}
%\fancyhead[EOHL]{
%\fancyplain{}\includegraphics[height=2cm]{logo_ufpa}
%}
\RequirePackage{wrapfig}
\fancyhead[LEO]{
	\begin{wrapfigure}{L}{1.57cm}
		\vspace{-1cm}
		\includegraphics[height=2cm]{logo_ufpa}
	\end{wrapfigure}
	\footnotesize
	\textbf{Universidade Federal do Pará \\
	Instituto de Tecnologia \\
	Faculdade de Engenharia da Computação\\}
}


\endinput

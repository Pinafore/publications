%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%       This File               : clv3.cls
%       Version         : 3
%
%       Developed By    : Krishan Gopal Goswami
%       Date                    : 21-Oct-2005
%
%       Developed for   : SPI Publisher Services
%       Copyright (c)   : 
%
%       Remarks         : This is based on MIT - Computational Linguistics
%                         Standard Typesetting Instructions
%
%       Note            : 
%
%       1) Do not make any change in this file with out prior information
%       2) Update History for the changes in the format given below
%       
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%       Version : V1.2
%
%       Updated By      : Narayan Piyush
%       Date            : 26-Nov-2005
%
%       Updated for     : 
%
%       1) Italic Greek (Lowercase & Uppercase) Characters
%       
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%       Version : V3
%
%       Updated By      : Daniel Gildea
%       Date            : 15-Jun-2016
%
%       Updated for     : 
%
%       1) use natbib.  Fixes incompatibility with hyperref, for clickable pdfs.
%		allows for more flexible citation commands.  Requires use
%		use compling.bst in place of fullname.bst.
%	2) use amsthm.  Fixes problem with no demarcation of the end
%		of a theorem/lemma/proposition.  Fixes problem with small extra 
%		space at beginning of a theorem/lemma/proposition
%		if the \begin{theorem} is followed by a \label command.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Fonts: 
%
% Palatino
% Helvetica
%       
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Standard Sizes: 
%
% normalsize -- 10/12
% footnotesize -- 8/9
% small -- 9/10
% scriptsize -- 7/8
% tiny -- 5/6
% large -- 12/13
% Large -- 16/20
% LARGE -- 17/20
% huge -- 20/25
% Huge -- 25/30
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{clv3}[2016/06/15 v2 LaTeX document class for MIT - Computational Linguistics Journals]
%
%\xdef\jobtag{MIT --- Computational Linguistics\qquad (Typeset by spi publisher services, Delhi)}%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Job Options %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\newdimen\draftrule\draftrule0pt
\newdimen\trimrule\trimrule.1pt
%
\newif\ifindex
\newif\ifdiscussion
\newif\ifbookreview
\newif\ifbrief
\newif\ifpubrec
\newif\ifshortpaper
\newif\ifmanuscript
%
\DeclareOption{manuscript}{\AtBeginDocument{\setlength{\baselineskip}{2\baselineskip}\global\manuscripttrue}}
\DeclareOption{discussion}{\discussiontrue}
\DeclareOption{bookreview}{\bookreviewtrue}
\DeclareOption{brief}{\brieftrue\shortpapertrue}
\DeclareOption{pubrec}{\pubrectrue\shortpapertrue}
\DeclareOption{index}{\indextrue}
\DeclareOption{final}{}
\ExecuteOptions{final}
\ProcessOptions
%
\@twosidetrue\@mparswitchtrue\ifshortpaper\@twocolumntrue\else\@twocolumnfalse\fi
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Variable Declarations %%%%%%%%%%%%%%%%%%%%%
%
% \newlength Declarations
%
\newlength\trimwidth
\newlength\trimheight
\newlength\typewidth
\newlength\typeheight
\newlength\normaltextheight
\newlength\blindfoliodrop
\newlength\figheight
\newlength\figwidth
\newlength\tabledim
%
%%%%% \newdimen Declarations %%%%%
%
\newdimen\tempdimen
\newdimen\enumdim
\newdimen\mathindent
\newdimen\emathindent
\newdimen\bibindent
%
% \newskip Declarations
%
\newskip\normalbaselineskip
\newskip\tableleftskip
\newskip\tablerightskip
%
%%%%% \newbox Declarations %%%%%
%
\newbox\tempbox
%
%%%%% \newif Declarations %%%%%
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%% Variable Initialization %%%%%%%%%%%%%%%%%%%%%%
%
%
%%
\setlength\trimheight{10in}
\setlength\trimwidth{6.75in}
%
\setlength\typeheight{56pc}
%
\setlength\headheight{6.5\p@}%
\setlength\headsep   {31pt}%
\setlength\topskip   {7\p@}%
%
\setlength\textheight{49.61pc}%
%\addtolength\textheight{\topskip}% \textheight = 49\baselineskip + \topskip
%
\setlength\normaltextheight{\textheight}
\setlength\textwidth{32pc}
%
\setlength\typewidth{\textwidth}
%
\setlength\topmargin{26.7pt}%25.35pt}
\setlength\oddsidemargin{54pt}
%
\setlength\evensidemargin\trimwidth
\addtolength\evensidemargin{-\textwidth}
\addtolength\evensidemargin{-\oddsidemargin}
%\addtolength\oddsidemargin{4.5pc}
\setlength\footskip{36pt}
\setlength\maxdepth{4\p@}
%
\setlength\blindfoliodrop{\trimheight}
\addtolength\blindfoliodrop{-\typeheight}
\addtolength\blindfoliodrop{-\topmargin}
%\addtolength\blindfoliodrop{-\footskip}
\addtolength\blindfoliodrop{18pt}
%
\ifshortpaper
   \setlength\parindent{9pt}
\else
   \setlength\parindent{18pt}
\fi
%
\setlength\marginparwidth {5pc}
\setlength\marginparsep{6\p@}
\setlength\marginparpush{5\p@}
%
\setlength\footnotesep{6.65\p@}
\setlength{\skip\footins}{23\p@ \@plus 8\p@}% \@minus 8\p@}%
\skip\@mpfootins = \skip\footins
%
\setlength\floatsep    {19\p@ \@plus 2\p@}% \@minus 2\p@}
\setlength\textfloatsep{30\p@ \@plus 2\p@}% \@minus 4\p@}
\setlength\intextsep   {12\p@ \@plus 2\p@}% \@minus 2\p@}
\setlength\dblfloatsep    {12\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\dbltextfloatsep{20\p@ \@plus 2\p@ \@minus 4\p@}
\setlength\@fptop{0\p@}
\setlength\@fpsep{8\p@ \@plus 1fil}
\setlength\@fpbot{0\p@ \@plus 1fil}
\setlength\@dblfptop{0\p@}
\setlength\@dblfpsep{8\p@ \@plus 1fil}
\setlength\@dblfpbot{0\p@ \@plus 1fil}
%
\setlength\partopsep{0pt}
\setlength\lineskip{1\p@}% check if it can be flexible
\setlength\normallineskip{1\p@}%
\renewcommand\baselinestretch{}
\ifpubrec
   \setlength\parskip{10pt plus.1pt}%{0\p@ \@plus \p@}
\else
   \setlength\parskip{\z@}%{0\p@ \@plus \p@}
\fi
\@lowpenalty   51
\@medpenalty  151
\@highpenalty 301
%
\@beginparpenalty -\@lowpenalty
\@endparpenalty   -\@lowpenalty
\@itempenalty     -\@lowpenalty
%
\clubpenalty\@M
\widowpenalty\@M
\hyphenpenalty400
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%% Fonts Size Definitions %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\def\@viiipt{8}
\def\@ixpt{9}
\def\@xpt{10}
\def\@xhpt{10.5}
\def\@xiipt{12}
\def\@xvpt{15}
\def\@xvipt{16}
\def\@xviipt{17}
\def\@xviiipt{18}
\def\@xxivpt{24}
%
\normalbaselineskip12pt
%
\ifpubrec
 \renewcommand\normalsize{%
   \@setfontsize\normalsize\@ixpt{10}%
   \abovedisplayskip 11\p@ \@plus2\p@% \@minus\p@
   \belowdisplayskip      \abovedisplayskip
   \abovedisplayshortskip \abovedisplayskip
   \belowdisplayshortskip \abovedisplayskip
   \let\@listi\@listI}
\else
\ifbrief
 \renewcommand\normalsize{%
   \@setfontsize\normalsize\@ixpt{11}%
   \abovedisplayskip 11\p@ \@plus2\p@% \@minus\p@
   \belowdisplayskip      \abovedisplayskip
   \abovedisplayshortskip \abovedisplayskip
   \belowdisplayshortskip \abovedisplayskip
   \let\@listi\@listI}
\else
 \renewcommand\normalsize{%
   \@setfontsize\normalsize\@xpt{12}%
   \abovedisplayskip 12\p@ \@plus2\p@% \@minus\p@
   \belowdisplayskip      \abovedisplayskip
   \abovedisplayshortskip \abovedisplayskip
   \belowdisplayshortskip \abovedisplayskip
   \let\@listi\@listI}
\fi\fi
\def\biggg#1{{\hbox{$\left#1\vbox to20.5\p@{}\right.\n@space$}}}
\def\Biggg#1{{\hbox{$\left#1\vbox to23.5\p@{}\right.\n@space$}}}
\normalsize
%
\newcommand\small{%
   \@setfontsize\small\@ixpt{10}%
   \abovedisplayskip 10\p@ \@plus2\p@% \@minus\p@
   \belowdisplayskip      \abovedisplayskip
   \abovedisplayshortskip \abovedisplayskip
   \belowdisplayshortskip \abovedisplayskip
   \def\@listi{\leftmargin\leftmargini
               \topsep 5\p@ \@plus2\p@% \@minus\p@
               \parsep 0\p@% \@plus\p@% \@minus\p@
               \itemsep \parsep}%
   \abovedisplayshortskip\abovedisplayskip
   \belowdisplayshortskip\abovedisplayshortskip
   \belowdisplayskip \abovedisplayskip
   \setSmallDelims}
%
\def\setSmallDelims{%
\def\big##1{{\hbox{$\left##1\vbox to7.5\p@{}\right.\n@space$}}}%
\def\Big##1{{\hbox{$\left##1\vbox to10.5\p@{}\right.\n@space$}}}%
\def\bigg##1{{\hbox{$\left##1\vbox to13.5\p@{}\right.\n@space$}}}%
\def\Bigg##1{{\hbox{$\left##1\vbox to16.5\p@{}\right.\n@space$}}}%
\def\biggg##1{{\hbox{$\left##1\vbox to19.5\p@{}\right.\n@space$}}}%
\def\Biggg##1{{\hbox{$\left##1\vbox to22.5\p@{}\right.\n@space$}}}%
}
%
\newcommand\footnotesize{%
   \@setfontsize\footnotesize\@viiipt{9}%
   \abovedisplayskip 9\p@ \@plus2\p@% \@minus\p@
   \belowdisplayskip      \abovedisplayskip
   \abovedisplayshortskip \abovedisplayskip
   \belowdisplayshortskip \abovedisplayskip
   \def\@listi{\leftmargin\leftmargini
               \topsep 4.5\p@ \@plus\p@% \@minus\p@
               \parsep 0\p@% \@plus\p@% \@minus\p@
               \itemsep \parsep}%
   \setFootnotesizeDelims}
%
\def\setFootnotesizeDelims{%
\def\big##1{{\hbox{$\left##1\vbox to6.5\p@{}\right.\n@space$}}}%
\def\Big##1{{\hbox{$\left##1\vbox to9.5\p@{}\right.\n@space$}}}%
\def\bigg##1{{\hbox{$\left##1\vbox to12.5\p@{}\right.\n@space$}}}%
\def\Bigg##1{{\hbox{$\left##1\vbox to15.5\p@{}\right.\n@space$}}}%
\def\biggg##1{{\hbox{$\left##1\vbox to18.5\p@{}\right.\n@space$}}}%
\def\Biggg##1{{\hbox{$\left##1\vbox to21.5\p@{}\right.\n@space$}}}%
}
%   
\newcommand\tiny{\@setfontsize\tiny\@vpt{6}}
\newcommand\scriptsize{\@setfontsize\scriptsize\@viipt{8}}
\newcommand\large{\@setfontsize\large\@xiipt{13}}
\newcommand\Large{\@setfontsize\Large\@xvipt{20}}
\newcommand\LARGE{\@setfontsize\LARGE\@xviipt{20}}
\newcommand\huge{\@setfontsize\huge\@xxpt{25}}
\newcommand\Huge{\@setfontsize\Huge\@xxvpt{30}}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%% headings
\def\rhfont{\small}
\def\rffont{\footnotesize}
\def\foliofont{\normalsize}
\def\dropfoliofont{\normalsize}
%% Title
\def\sptitlefont{\LARGE\bfseries\ifdiscussion\rightskip4pc plus1fill\else\raggedright\fi\mathversion{bold}}
\ifbrief
   \def\titlefont{\fontsize{10}{11}\selectfont\bfseries\raggedright\mathversion{bold}}
\else\ifbookreview
   \def\titlefont{\fontsize{12}{12}\selectfont\bfseries\raggedright\mathversion{bold}}
\else\ifdiscussion
   \def\titlefont{\Large\bfseries\raggedright\mathversion{bold}}
\else
   \def\titlefont{\Large\bfseries\rightskip4pc plus1fill\mathversion{bold}}
\fi\fi\fi
\def\subtitlefont{\large\bfseries}
%% Author/Affil
\ifbrief
   \def\authorfont{\small\bfseries\raggedright}
\else\ifbookreview
   \def\authorfont{\normalsize\bfseries\raggedright}
\else
   \def\authorfont{\large\raggedright}
\fi\fi
\ifbrief
   \def\affilfont{\small\raggedright}
\else
   \def\affilfont{\normalsize\raggedright}
\fi
\ifbrief
   \def\pubinfofont{\small\raggedright}
\else
   \def\pubinfofont{\normalsize\raggedright}
\fi
\def\reviewerfont{\normalsize\itshape}
\ifbrief
   \def\biofont{\normalsize}
\else
   \def\biofont{\small}%\itshape}
\fi
%%
\def\abstractfont{\normalsize\setlength\baselineskip{13pt}\itshape}
\def\keywordfont{\normalsize\raggedright}
%% section
\def\sectionfont{\normalsize\bfseries\mathversion{bold}}
\def\sectionnumfont{\normalsize\bfseries}
\def\subsectionfont{\normalsize\bfseries\mathversion{bold}}
\def\subsectionnumfont{\normalsize\bfseries}
\def\subsubsectionfont{\normalsize\bfseries\mathversion{bold}}
\def\paragraphfont{\normalsize\itshape}%
\def\subparagraphfont{}%
\def\subsubparagraphfont{}%
\def\xheadfont{\normalsize\bfseries}
%% figure
\def\figcaptionfont{\small\raggedright}%\mathversion{sfnormal}}
\def\figcaptionnumfont{\small\bfseries}
\def\figsourcefont{\reset@font\fontsize{8.5}{10}\selectfont}
%% table
\def\tablefont{\small}%\leftskip\tableleftskip\rightskip\tablerightskip use plus 1fill if needed
\def\tablecaptionfont{\small\raggedright}%\mathversion{sfnormal}}%
\def\tablecaptionnumfont{\small\bfseries}%
\def\TCHfont{\small}%
\def\tabnotefont{\leftskip\tableleftskip\rightskip\tablerightskip}% use plus 1fill if needed
%% BM
\def\indexfont{\fontsize{9}{10}\selectfont\raggedright}
\def\ackfont{\small\raggedright}
%
\def\listfont{\raggedright}
\def\listdevicefont{}
%
\ifbrief
   \def\extractfont{\small\leftskip2pc}
\else\ifbookreview
   \def\extractfont{\normalsize\itshape}
\else
   \def\extractfont{\small\leftskip1.5pc\rightskip1.5pc plus1fill}%
\fi\fi
\def\sourcefont{\reset@font\normalsize}
%
%
%%%%%%%  For Times family  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\DeclareOldFontCommand{\rm}{\normalfont\rmfamily}{\mathrm}
\DeclareOldFontCommand{\sf}{\normalfont\sffamily}{\mathsf}
\DeclareOldFontCommand{\tt}{\normalfont\ttfamily}{\mathtt}
\DeclareOldFontCommand{\bf}{\normalfont\bfseries}{\mathbf}
\DeclareOldFontCommand{\it}{\normalfont\itshape}{\mathit}
\DeclareOldFontCommand{\sl}{\normalfont\slshape}{\@nomath\sl}
\DeclareOldFontCommand{\sc}{\normalfont\scshape}{\@nomath\sc}
\DeclareOldFontCommand{\bi}{\bfseries\itshape}{\bfseries\itshape}
\newcommand{\cal}{\protect\pcal}
\newcommand{\pcal}{\@fontswitch{\relax}{\mathcal}}
\newcommand{\mit}{\protect\pmit}
\newcommand{\pmit}{\@fontswitch{\relax}{\mathnormal}}
%
%\renewcommand\rmdefault{Times}
%\newcommand\rmmathdefault{TimesMath}
%
%\renewcommand\sfdefault{Officina}
%\newcommand\sfmathdefault{HelveticaMath}
%\renewcommand{\ttdefault}{Courier}
%%
\def\scitdefault{scit}% All scit
\def\capsitdefault{capsit}% all capsit 
%
\def\capsdefault{caps}% all caps
\DeclareRobustCommand\capsshape
        {\not@math@alphabet\capsshape\mathrm
         \ifx\f@shape\itdefaultabbrev\fontshape\capsitdefault\else\fontshape\capsdefault\fi\selectfont}
%
\def\itdefaultabbrev{it}
\DeclareRobustCommand\itshape
        {\not@math@alphabet\itshape\mathit
         \ifx\f@shape\scdefaultabbrev\fontshape\scitdefault\else\ifx\f@shape\capsdefault\fontshape\capsitdefault\else\fontshape\itdefault\fi\fi\selectfont}
%
\def\scdefaultabbrev{sc}
\DeclareRobustCommand\scshape
        {\not@math@alphabet\scshape\relax
         \ifx\f@shape\itdefaultabbrev\fontshape\scitdefault\else\fontshape\scdefault\fi\selectfont}
%
%%%%%%%%%%%%%%%%%%%% Times %%%%%%%%%%%%%%%%%%
%
\DeclareFontFamily{OML}{TimesMath}{\skewchar\font127 }
\DeclareFontShape{OML}{TimesMath}{m}{it}{<-> MTMI }{}
\DeclareFontShape{OML}{TimesMath}{bx}{it}{<->  MTMIB }{}
\DeclareFontShape{OML}{TimesMath}{b}{it}{<->ssub*TimesMath/bx/it}{}
%
\DeclareFontFamily{OMS}{TimesMath}{\skewchar\font48 }
\DeclareFontShape{OMS}{TimesMath}{m}{n}{<->  MTSY }{}
\DeclareFontShape{OMS}{TimesMath}{bx}{n}{<->  MTSYB }{}
%
\DeclareFontFamily{OMX}{TimesMath}{}
\DeclareFontShape{OMX}{TimesMath}{m}{n}{<->  MTEX }{}
%
\DeclareFontFamily{OT1}{Times}{}
\DeclareFontShape{OT1}{Times}{m}{n}{ <-> ptmr }{}
\DeclareFontShape{OT1}{Times}{m}{it}{ <-> ptmri }{}
%
\DeclareFontShape{OT1}{Times}{bx}{n}{ <-> ptmb }{}
\DeclareFontShape{OT1}{Times}{bx}{it}{ <-> ptmbi }{}
%
%%%%%%%%%%%%%%%%%%%% Helvetica %%%%%%%%%%%%%%%%%%
%
\DeclareFontFamily{OML}{HelveticaMath}{\skewchar\font127 }
\DeclareFontShape{OML}{HelveticaMath}{m}{it}{<-> HelMTMI }{}
\DeclareFontShape{OML}{HelveticaMath}{bx}{it}{<->  HelMTMIB }{}
\DeclareFontShape{OML}{HelveticaMath}{b}{it}{<->ssub*HelveticaMath/bx/it}{}
%
\DeclareFontFamily{OMS}{HelveticaMath}{\skewchar\font48 }
\DeclareFontShape{OMS}{HelveticaMath}{m}{n}{<->  MTSY }{}
\DeclareFontShape{OMS}{HelveticaMath}{bx}{n}{<->  MTSYB }{}
%
\DeclareFontFamily{OMX}{HelveticaMath}{}
\DeclareFontShape{OMX}{HelveticaMath}{m}{n}{<->  MTEX }{}
%
\DeclareFontFamily{OT1}{Helvetica}{}
\DeclareFontShape{OT1}{Helvetica}{m}{n}{ <-> phvr }{}
\DeclareFontShape{OT1}{Helvetica}{m}{it}{ <-> phvro }{}
\DeclareFontShape{OT1}{Helvetica}{bx}{n}{ <-> phvb }{}
\DeclareFontShape{OT1}{Helvetica}{bx}{it}{ <-> phvbo }{}
%
%
\DeclareFontFamily{OT1}{ams}{}
\DeclareFontShape{OT1}{ams}{m}{n}{ <-> msam10 }{}
\DeclareFontShape{OT1}{ams}{m}{it}{ <-> msam10 }{}
\DeclareFontShape{OT1}{ams}{bx}{n}{ <-> msbm10 }{}
\DeclareFontShape{OT1}{ams}{bx}{it}{ <-> msbm10 }{}
%
%
\DeclareFontShape{OMS}{cmsy}{m}{n}{ <-> cmsy10 }{}
\DeclareFontShape{OMS}{cmsy}{b}{n}{ <-> cmbsy10 }{}
%
%
\newcommand\sfboldmath{\@nomath\sfboldmath\mathversion{sfbold}}
%%%%% define bold math font %%%%%
\newcommand\bm[1]{\mathchoice
   {\mbox{\boldmath$\displaystyle#1$}}%
   {\mbox{\boldmath$#1$}}%
   {\mbox{\boldmath$\scriptstyle#1$}}%
   {\mbox{\boldmath$\scriptscriptstyle#1$}}}
%
\usepackage[T1]{fontenc}
\usepackage{textcomp}
\usepackage{palatino,helvet}%,zeupplv1}%,mathptm}%
%
\DeclareFontFamily{OML}{euppl}{\skewchar \font =127}
\DeclareFontShape{OML}{euppl}{m}{it}{<8-> pplre7m <6-8> pplre7m7 <-6> pplre7m5}{}
\DeclareFontShape{OML}{euppl}{m}{sl}{<->ssub * euppl/m/it}{}
\DeclareFontShape{OML}{euppl}{b}{it}{<-> pplbe7m}{}
\DeclareFontShape{OML}{euppl}{bx}{it}{<->ssub * euppl/b/it}{}
%
\DeclareFontFamily{OML}{euphv}{\skewchar \font =127}
\DeclareFontShape{OML}{euphv}{m}{it}{<8-> phvre7m <6-8> phvre7m7 <-6> phvre7m5}{}
\DeclareFontShape{OML}{euphv}{m}{sl}{<->ssub * euphv/m/it}{}
\DeclareFontShape{OML}{euphv}{b}{it}{<-> phvbe7m}{}
\DeclareFontShape{OML}{euphv}{bx}{it}{<->ssub * euphv/b/it}{}
%
\DeclareFontFamily{U}{bbnum}{}
\DeclareFontShape{U}{bbnum}{m}{n}{<-> CASLOB}{}
\DeclareMathAlphabet{\mathbbnum}{U}{bbnum}{m}{n}
%
%\DeclareMathSymbol{,}{\mathpunct}{operators}{`,}
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%% General Commands %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\newcommand\contentsname{Contents}
\newcommand\listfigurename{List of Figures}
\newcommand\listtablename{List of Tables}
\newcommand\bibname{References}
\newcommand\indexname{Index}
\newcommand\figurename{Figure}
\newcommand\tablename{Table}
\newcommand\appendixname{Appendix}
%
\newcommand\today{\ifcase\month\or
  January\or February\or March\or April\or May\or June\or
  July\or August\or September\or October\or November\or December\fi
  \space\number\day, \number\year}
%
\newcount\minute
\newcount\hour
\def\currenttime{%
     \minute\time
     \hour\minute
     \divide\hour60
     \the\hour:\multiply\hour60\advance\minute-\hour\the\minute}
%
\def\spreadoutfactor{1}
%
\def\spreadout#1{%
  \gdef\temp{#1}\dimen0 = \spreadoutfactor pt
  \expandafter\dospreadout\temp\endmark\kern-\dimen0}
%
\def\dospreadout{%
  \afterassignment\findospreadout
  \let\next= }
%
\def\findospreadout{%
   \ifx\next\endmark
      \let\nextaction = \relax
   \else
      \let\nextaction = \dospreadout
      \next
      \kern\dimen0
   \fi
   \nextaction}
%
%%%%%%%%%%%%%%%%%%%%%%%%%% Make Title %%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\def\jname#1{\gdef\@jname{#1}}
\def\jinfo#1{\gdef\@jinfo{#1}}
\def\jvol#1{\gdef\@jvol{#1}}\def\@jvol{xx}
\def\jnum#1{\gdef\@jnum{#1}}\def\@jnum{xx}
\def\jyear#1{\gdef\@jyear{#1}}\def\@jyear{2005}
\def\rtitle#1{\gdef\@rtitle{#1}}\def\@rtitle{Running Title}
\def\rauthor#1{\gdef\@rauthor{#1}}\def\@rauthor{Running Author}
%
\def\issue #1#2#3{\jvol{#1}\jnum{#2}\jyear{#3}}
\def\runningtitle#1{\rtitle{#1}}
\def\runningauthor#1{\rauthor{#1}}
%
\jname{Computational Linguistics}
\jinfo{Volume \@jvol, Number \@jnum}
%
\def\@sptitle{}
\def\sptitle#1{\gdef\@sptitle{#1}}
%
\def\@title{}
\def\title{\@dblarg{\@@title}}
\def\@@title[#1]#2{\gdef\@title{#2}}
%
\newcount\aucount
\newcount\tempcount
%
\def\author{\@dblarg{\@author}}
\def\@author[#1]#2{\global\advance\aucount\@ne
   \expandafter\gdef\csname author\romannumeral\aucount\endcsname{#2}}
%
\def\affil#1{\expandafter\gdef\csname affil\romannumeral\aucount\endcsname{#1}}
%
\def\printauthors{%
   \ifnum\aucount=\z@
      \gdef\@authors{}
   \else
      \gdef\@authors{%
         \tempcount\@ne
         \@whilenum\aucount>\z@
         \do{%
            \ifbrief
               {\authorfont\csname author\romannumeral\tempcount\endcsname\vphantom{pl}\par}
               {\reset@font\affilfont\csname affil\romannumeral\tempcount\endcsname\vphantom{pl}\par}%
            \else\ifbookreview
               {\authorfont\csname author\romannumeral\tempcount\endcsname\vphantom{pl}\par
               {\reset@font\affilfont\csname affil\romannumeral\tempcount\endcsname\vphantom{pl}\par}}%
            \else
               \ifnum\tempcount=\@ne\noindent\else\ifodd\tempcount\vskip13.5pt\noindent\else\hskip2pc\fi\fi
               \parbox[t]{15pc}{\authorfont
               \csname author\romannumeral\tempcount\endcsname\vphantom{pl}\par
               {\affilfont\setlength\baselineskip{13pt}\csname affil\romannumeral\tempcount\endcsname\vphantom{pl}\par}}%
            \fi\fi
            \advance\aucount\m@ne\advance\tempcount\@ne
         }%
      }
   \fi
}
%
\def\@historydates{}
\def\historydates#1{\gdef\@historydates{#1}}%\thanks{#1}}
%
\def\@pubinfo{}
\def\pubinfo#1{\gdef\@pubinfo{#1}}
%
\def\@reviewer{}
\def\reviewer#1{\gdef\@reviewer{#1}}
%
\def\endbody{\ifx\@reviewer\@empty\else\unskip---{\itshape\@reviewer}\fi}%\par\addvspace{10pt}}
%
\def\@biography{}
\def\biography#1{\gdef\@biography{#1}}
%
\ifpubrec
  \def\@maketitle{\cleardoublepage%
   \thispagestyle{pageonly}%titlepage
   \parindent\z@
   \ifx\@sptitle\@empty\else
      \null\vskip -56.3pt
      {\sptitlefont\@sptitle\vphantom{y}\par}%
      \vskip 16.5pt
   \fi
}
\else
\ifbrief
  \def\@maketitle{\cleardoublepage%
   \thispagestyle{pageonly}%titlepage
   \parindent\z@
   \ifx\@sptitle\@empty\else
      \null\vskip -56.3pt
      {\sptitlefont\@sptitle\vphantom{y}\par}%
      \vskip 17.5pt
   \fi
   \gdef\mktout@after@twocol{\parindent\z@%
   \ifx\@title\@empty\else
      {\titlefont\@title\vphantom{y}\par}
   \fi
   \printauthors
   \ifx\@authors\@empty\else\vskip 6pt
      {\authorfont\@authors\par}
   \fi
   \ifx\@pubinfo\@empty\else\vskip 6pt
      {\pubinfofont\@pubinfo\par}
   \fi
%   \ifx\@reviewer\@empty\else\vskip 12pt
%      {\reviewerfont Reviewed by\par\@reviewer\par}
%   \fi
   \par\addvspace{13pt}%
   }\aftergroup\mktout@after@twocol
}
\else\ifbookreview
  \def\@maketitle{\cleardoublepage%
   \thispagestyle{empty}%titlepage
   \parindent\z@
   \ifx\@sptitle\@empty\else
      \null\vskip -52.5pt
      {\sptitlefont\@sptitle\vphantom{y}\par}%
      \vskip 42.5pt
   \fi
   \ifx\@title\@empty\else
      {\titlefont\@title\vphantom{y}\par}\vskip 12pt
   \fi
   \printauthors
   \ifx\@authors\@empty\else
      {\authorfont\@authors\par}
   \fi
   \ifx\@pubinfo\@empty\else\vskip 12pt
      {\pubinfofont\@pubinfo\par}
   \fi
   \ifx\@reviewer\@empty\else\vskip 12pt
      {\reviewerfont Reviewed by\par\@reviewer\par}
   \fi
   \par\addvspace{12pt}%
   \gdef\@reviewer{}
}
\else
  \def\@maketitle{\cleardoublepage%
   \thispagestyle{titlepage}%
   \parindent\z@
   \ifx\@sptitle\@empty\else
      \null\vskip -52.5pt
      {\sptitlefont\@sptitle\vphantom{y}\par}%
      \vskip 39.5pt
   \fi
   \ifx\@title\@empty\else
      {\titlefont\@title\vphantom{y}\par}\vskip 29pt
   \fi
   \printauthors
   \ifx\@authors\@empty\else
      {\authorfont\@authors\par}
   \fi
   \par\addvspace{31pt}%
}
\fi\fi\fi
%
\def\maketitle{\par
 \begingroup
   \def\thefootnote{\fnsymbol{footnote}}
   \if@twocolumn 
      \twocolumn[\@maketitle] 
   \else
      \@maketitle 
   \fi
   \@thanks
   \ifx\@historydates\@empty\else\let\domkfnmark\relax\def\dofnformat{\vskip\baselineskip}\@footnotetext{\@historydates}\fi
 \endgroup
 \setcounter{footnote}{0}
 \let\maketitle\relax
 \let\@maketitle\relax
 \gdef\@thanks{}\gdef\@authors{}\gdef\@title{}\gdef\@pubinfo{}\let\thanks\relax\@afterindentfalse\@afterheading}
%
\newenvironment{abstract}{\par\abstractfont\noindent\ignorespaces}{\par\addvspace{12pt}\@afterindentfalse\@afterheading}
\newcommand{\keywords}[1]{{\keywordfont Keywords: #1\par\addvspace{12pt}}}
%
\def\bookinfospace{\vskip10pt plus1pt}
\long\def\bookinfo#1#2{{\raggedright{\bfseries #1}\\#2\par\bookinfospace}}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Sectioning commands %%%%%%%%%%%%%%%%%%%%%%%%%%
%
\setcounter{secnumdepth}{3}
\newcounter {part}
\newcounter {chapter}
\newcounter {section}[chapter]
\newcounter {subsection}[section]
\newcounter {subsubsection}[subsection]
\newcounter {paragraph}[subsubsection]
\newcounter {subparagraph}[paragraph]
\renewcommand\thepart          {\Roman{part}}
\renewcommand\thechapter       {\arabic{chapter}}
\renewcommand\thesection       {\arabic{section}}
\renewcommand\thesubsection    {\thesection.\arabic{subsection}}
\renewcommand\thesubsubsection {\thesubsection .\arabic{subsubsection}}
\renewcommand\theparagraph     {\thesubsubsection.\arabic{paragraph}}
\renewcommand\thesubparagraph  {\theparagraph.\arabic{subparagraph}}
%
\def\@sectioncntformat#1{{\csname #1numfont\endcsname\csname the#1\endcsname.}\nobreakspace}
\def\@seccntformat#1{\csname #1numfont\endcsname\csname the#1\endcsname\nobreakspace}
%
\newcommand\section{\@startsection {section}{1}{\z@}{-12pt \@plus -2pt}{12pt}{\def\@afterhead{}\sectionfont}}%
\newcommand\subsection{\@startsection{subsection}{2}{\z@}{-12pt \@plus -2pt}{12pt}{\def\@afterhead{}\subsectionfont}}%
\newcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}{-12pt \@plus -2pt}{0pt}{\def\@afterhead{. }\subsubsectionfont}}%
\newcommand\paragraph{\def\@afterhead{.}\@startsection{paragraph}{4}{\z@}{-12pt \@plus -2pt}{-0pt}{\def\@afterhead{. }\paragraphfont}}%
\newcommand\subparagraph{\@startsection{subparagraph}{5}{\parindent}{-6pt \@plus -2pt}{-1em}{\def\@afterhead{. }\subparagraphfont}}%
\newcommand\subsubparagraph{\@startsection{subsubparagraph}{6}{\parindent}{-6pt \@plus -2pt}{-1em}{\def\@afterhead{. }\subsubparagraphfont}}%
\newcommand\xhead{\@startsection{xhead}{7}{\z@}{-14pt \@plus -2pt}{2pt}%{0.0001pt}
                                        {\def\@afterhead{}\xheadfont}}%
\let\xheadmark\@gobble
%
\def\@startsection#1#2#3#4#5#6{%
  \if@noskipsec \leavevmode \fi
  \par
  \@tempskipa #4\relax
  \@afterindenttrue
  \ifdim \@tempskipa <\z@
    \@tempskipa -\@tempskipa \@afterindentfalse
  \fi
  \if@nobreak
%    \ifnum#2=2\fi
    \ifnum#2=3\vskip-12pt\fi
    \everypar{}%
  \else
    \addpenalty\@secpenalty\addvspace\@tempskipa
  \fi
  \@ifstar
    {\@ssect{#3}{#4}{#5}{#6}}%
    {\@dblarg{\@sect{#1}{#2}{#3}{#4}{#5}{#6}}}}
%
\def\@afterhead{}
\def\@sect#1#2#3#4#5#6[#7]#8{\ifnum #2>\c@secnumdepth
     \let\@svsec\@empty\else
     \refstepcounter{#1}%
     \let\@@protect\protect
     \def\protect{\noexpand\protect\noexpand}%
     \ifnum#2=1
        \edef\@svsec{\@sectioncntformat{#1}}%
     \else
        \edef\@svsec{\@seccntformat{#1}}%
     \fi
     \let\protect\@@protect\fi
     \@tempskipa #5\relax
      \ifdim \@tempskipa>\z@
        \begingroup #6\relax
          \@hangfrom{\hskip #3\relax\@svsec}%
                    {\interlinepenalty \@M #8\@afterhead\par}%
        \endgroup
       \csname #1mark\endcsname{#7}\addcontentsline
         {toc}{#1}{\ifnum #2>\c@secnumdepth \else
                      \protect\numberline{\csname the#1\endcsname}\fi
                    #7}\else
        \def\@svsechd{#6\hskip #3\relax
                   \@svsec #8\@afterhead\csname #1mark\endcsname
                      {#7}\addcontentsline
                           {toc}{#1}{\ifnum #2>\c@secnumdepth \else
                           \protect\numberline{\csname the#1\endcsname}%
                                     \fi
                       #7}}\fi
     \@xsect{#5}}
%
\def\@ssect#1#2#3#4#5{\@tempskipa #3\relax
   \ifdim \@tempskipa>\z@
     \begingroup #4\@hangfrom{\hskip #1}{\interlinepenalty \@M #5\par}\endgroup
   \else \def\@svsechd{#4\hskip #1\relax #5\@afterhead\null}\fi
    \@xsect{#3}}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%  Lists Variable Initialisation %%%%%%%%%%%%%%%%%%%%%%%
%
\newskip\topsepi \topsepi6\p@ \@plus2\p@% \@minus.5\p@
\newskip\topsepii \topsepii2pt% \@plus1\p@ 
\newskip\topsepiii \topsepiii2pt% \@plus1\p@ 
\newskip\itemsepi \itemsepi0pt
\newskip\itemsepii \itemsepii0pt
\newskip\itemsepiii \itemsepiii0pt
\newdimen\LabelSep \LabelSep4.7pt
%
\def\@listI{\leftmargin\leftmargini
            \labelwidth\leftmargini
            \advance\labelwidth-\labelsep
            \parsep 0\p@%
            \topsep \topsepi
            \itemsep\itemsepi}%
\let\@listi\@listI
\@listi
\def\@listii {\leftmargin\leftmarginii
              \labelwidth\leftmarginii
              \advance\labelwidth-\labelsep
              \topsep\topsepii
              \parsep 0pt
              \itemsep\itemsepii}
\def\@listiii {\leftmargin\leftmarginiii
              \labelwidth\leftmarginiii
              \advance\labelwidth-\labelsep
              \topsep\topsepiii
              \parsep 0pt
              \itemsep\itemsepiii}
\def\@listiv {\leftmargin\leftmarginiv
              \labelwidth\leftmarginiv
              \advance\labelwidth-\labelsep}
\def\@listv  {\leftmargin\leftmarginv
              \labelwidth\leftmarginv
              \advance\labelwidth-\labelsep}
\def\@listvi {\leftmargin\leftmarginvi
              \labelwidth\leftmarginvi
              \advance\labelwidth-\labelsep}
%
\setlength\leftmargini  {2.5em}
\setlength\leftmarginii  {2.2em}
\setlength\leftmarginiii {1.87em}
\setlength\leftmarginiv  {1.7em}
\setlength\leftmarginv  {1em}
\setlength\leftmarginvi {1em}
\setlength\leftmargin    {\leftmargini}
%
\setlength  \labelsep  {\LabelSep}
\setlength  \labelwidth{\leftmargini}
\addtolength\labelwidth{-\labelsep}
%
\renewcommand\theenumi{\arabic{enumi}}
\renewcommand\theenumii{\alph{enumii}}
\renewcommand\theenumiii{\roman{enumiii}}
\renewcommand\theenumiv{\Alph{enumiv}}
\newcommand\labelenumi{\theenumi.}
\newcommand\labelenumii{(\theenumii)}
\newcommand\labelenumiii{\theenumiii.}
\newcommand\labelenumiv{\theenumiv.}
\renewcommand\p@enumii{\theenumi}
\renewcommand\p@enumiii{\theenumi(\theenumii)}
\renewcommand\p@enumiv{\p@enumiii\theenumiii}
\font\lcir = lcircle10 at 12pt
\newcommand\bulls{\hbox{\lcir\char'162}}
\def\textbullet{\leavevmode\raise3.5pt\bulls\hskip-2pt}
\def\textendash{{\bf--}}
\def\textasteriskcentered{\leavevmode\raise-1.5pt\hbox{*}}
\def\textperiodcentered{\leavevmode\raise1.5pt\hbox{\bulls}}
\newcommand\labelitemi{\textbullet}
\newcommand\labelitemii{\normalfont\bfseries \textendash}
%
\newenvironment{description}
               {\list{}{\labelwidth\z@ \itemindent-\leftmargin
                        \let\makelabel\descriptionlabel}}
               {\endlist}
\newcommand*\descriptionlabel[1]{\hspace\labelsep
                                \normalfont\bfseries #1}
%
\newenvironment{verse}
               {\let\\\@centercr
                \list{}{\itemsep      \z@
                        \itemindent   -1.5em%
                        \listparindent\itemindent
                        \rightmargin  \leftmargin
                        \advance\leftmargin 1.5em}%
                \item\relax}
               {\endlist}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Enumerate list %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\newskip\listtopsepi
\newskip\listtopsepii
\newskip\listtopsepiii
\newskip\listitemsepi
\newskip\listitemsepii
\newskip\listitemsepiii
\newlength\listleftmargini
\newlength\listleftmarginii
\newlength\listleftmarginiii
\newlength\listlabelwidthi
\newlength\listlabelwidthii
\newlength\listlabelwidthiii
\newlength\listlabelsepi
\newlength\listlabelsepii
\newlength\listlabelsepiii
\newlength\listrightmargin
%
\newcount\listdepth
%
\newif\if@nomainitem
\def\nomainitem{\global\@nomainitemtrue}
\newlength\lpalignmaxwd
\newif\if@lpalign
\def\lpalign#1{\global\@lpaligntrue\global\settowidth\lpalignmaxwd{#1}}
%
\ifbrief
   \listtopsepi 5pt plus2pt% minus1pt
   \listtopsepii 0pt
   \listtopsepiii 0pt
   \listleftmargini 25pt
   \listleftmarginii 25pt
   \listleftmarginiii 25pt
   \listlabelwidthi 12pt
   \listlabelwidthii 12pt
   \listlabelwidthiii 12pt
   \listlabelsepi 13pt
   \listlabelsepii 13pt
   \listlabelsepiii 13pt
   \listrightmargin 0pt
   \listitemsepi 3pt
   \listitemsepii 0pt
   \listitemsepiii 0pt
\else
   \listtopsepi 12pt plus2pt% minus1pt
   \listtopsepii 0pt
   \listtopsepiii 0pt
   \listleftmargini 36pt
   \listleftmarginii 14pt
   \listleftmarginiii 8pt
   \listlabelwidthi 18pt
   \listlabelwidthii 32pt
   \listlabelwidthiii 40pt
   \listlabelsepi 18pt
   \listlabelsepii 18pt
   \listlabelsepiii 18pt
   \listrightmargin 18pt
   \listitemsepi 6pt
   \listitemsepii 0pt
   \listitemsepiii 0pt
\fi
%
\def\enumerate{\@ifnextchar[{\@enumerate}{\@enumerate[1]}}% 
%
\def\@enumerate[#1]{\par
   \ifnum\@enumdepth >\thr@@\@toodeep\else
      \advance\@enumdepth\@ne\advance\listdepth\@ne
      \edef\@listcounter{enum\romannumeral\the\@enumdepth}%
      \setcounter{\@listcounter}{1}%
   \fi
   \list{\csname labelenum\romannumeral\the\@enumdepth\endcsname}{\listfont%
      \usecounter{\@listcounter}%
      \topsep\csname listtopsep\romannumeral\the\listdepth\endcsname
      \leftmargin\csname listleftmargin\romannumeral\the\listdepth\endcsname
      \labelwidth\csname listlabelwidth\romannumeral\the\listdepth\endcsname
      \labelsep\csname listlabelsep\romannumeral\the\listdepth\endcsname
      \itemsep\csname listitemsep\romannumeral\the\listdepth\endcsname
      \rightmargin\listrightmargin\advance\leftmargin\leftskip
      \if@lpalign
         \global\@lpalignfalse
         \def\makelabel##1{\hbox to \labelwidth{\hss\hbox to\lpalignmaxwd{##1\hss}\hskip-.6pt}}
      \else
         \def\makelabel##1{\hbox to \labelwidth{\hss##1\hskip-.6pt}}
      \fi
      \if@nomainitem
         \global\@nomainitemfalse
         \leftmargin 10pt
         \labelwidth 10pt
         \labelsep 0pt
         \def\makelabel##1{##1 }%
      \fi
      }%
  }%
%
\def\endenumerate{\endlist}%
%
\newenvironment{arabiclist}{%
  \def\theenumi{\arabic{enumi}}\def\labelenumi{\theenumi.}
  \def\theenumii{\arabic{enumii}}\def\labelenumii{\theenumii.}%
  \def\theenumiii{\arabic{enumiii}}\def\labelenumiii{\theenumiii.}%
  \begin{enumerate}%
}{%
  \end{enumerate}}
%
\newenvironment{romanlist}{%
  \def\theenumi{\roman{enumi}}\def\labelenumi{\theenumi.}%
  \def\theenumii{\roman{enumii}}\def\labelenumii{\theenumii.}%
  \def\theenumiii{\roman{enumiii}}\def\labelenumiii{\theenumiii.}%
  \begin{enumerate}%
}{%
  \end{enumerate}}
%
\newenvironment{alphalist}{%
  \def\theenumi{\alph{enumi}}\def\labelenumi{(\theenumi)}%
  \def\theenumii{\alph{enumii}}\def\labelenumii{(\theenumii)}%
  \def\theenumiii{\alph{enumiii}}\def\labelenumiii{(\theenumiii)}%
  \begin{enumerate}%
}{%
  \end{enumerate}}
%
\newenvironment{Romanlist}{%
  \def\theenumi{\Roman{enumi}}\def\labelenumi{\theenumi.}%
  \def\theenumii{\Roman{enumii}}\def\labelenumii{\theenumii.}%
  \def\theenumiii{\Roman{enumiii}}\def\labelenumiii{\theenumiii.}%
  \begin{enumerate}%
}{%
  \end{enumerate}}
%
\newenvironment{Alphalist}{%
  \def\theenumi{\Alph{enumi}}\def\labelenumi{(\theenumi)}%
  \def\theenumii{\Alph{enumii}}\def\labelenumii{(\theenumii)}%
  \def\theenumiii{\Alph{enumiii}}\def\labelenumiii{(\theenumiii)}%
  \begin{enumerate}%
}{%
  \end{enumerate}}
%
\newenvironment{examples}{\begin{exlist}\item}{\end{exlist}}
%

\newcounter{eqnnosave}          % used in trick with equation number
\newenvironment{exlist}{%         % define "example" environment
   \listleftmargini 36pt
   \listlabelwidthi 30pt
   \listlabelsepi 6pt
   \listitemsepi12pt
   \def\labelenumi{(\theenumi)}
   \def\theenumii{\arabic{enumii}}\def\labelenumii{\theenumii.}%
   \begin{enumerate}%
   \setcounter{enumi}{\arabic{eqnnosave}}%   % restores previous value
}%
{\end{enumerate}%
\setcounter{eqnnosave}{\arabic{enumi}}%
}
%
\newenvironment{exoutlist}{\par%
   \listleftmarginii 20pt
   \listlabelwidthii 32pt
   \listlabelsepii 24pt
   \def\labelenumi{(\theenumi)}
   \def\theenumii{\arabic{enumii}}\def\labelenumii{\theenumii.}%
   \begin{enumerate}%
   \setcounter{enumi}{\arabic{eqnnosave}}%   % restores previous value
}%
{\end{enumerate}%
\setcounter{eqnnosave}{\arabic{enumi}}%
}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%% itemize (bullet) %%%%%%%%%%%%%%%%%%%%%%%%%%
%
\def\itemize{\par
   \ifnum\@itemdepth >\thr@@\@toodeep\else
      \advance\@itemdepth\@ne\advance\listdepth\@ne
   \fi
   \list{\csname labelitem\romannumeral\the\@itemdepth\endcsname}{\listfont%
      \topsep\csname listtopsep\romannumeral\the\listdepth\endcsname
      \labelwidth\csname listlabelwidth\romannumeral\the\listdepth\endcsname
      \labelsep\csname listlabelsep\romannumeral\the\listdepth\endcsname
      \leftmargin\csname listleftmargin\romannumeral\the\listdepth\endcsname
      \itemsep\csname listitemsep\romannumeral\the\listdepth\endcsname
      \rightmargin\listrightmargin\advance\leftmargin\leftskip
      \def\makelabel##1{\hbox to \labelwidth{\hss##1}}}%
   }%
%
\def\enditemize{\endlist}
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%% enumroman (i) %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\newenvironment{bulletlist}{%
   \renewcommand\labelitemi{\textbullet}\renewcommand\labelitemii{\textbullet}%
   \begin{itemize}
}{%
   \end{itemize}}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  unnumlist %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\newenvironment{unnumlist}{\par%
   \list{}{\listfont%
      \topsep12pt plus2pt% minus1pt
      \rightmargin18pt
      \leftmargin36pt%\itemindent-18pt
      \itemsep6pt\parsep0pt
      \partopsep0pt}
    \def\makelable##1{##1}%
   }{\endlist}%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Quotes %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\def\@source{}
\def\source#1{\gdef\@source{#1}}
%
\newenvironment{extract}{\par\ifbrief\addvspace{4pt plus2pt}\else\ifbookreview\addvspace{12pt plus2pt}\else\addvspace{14pt plus2pt}\fi\fi
      \extractfont\parindent18pt\noindent\ignorespaces
}{\par\ifx\@source\@empty\else{\sourcefont\noindent---\@source\par}\fi\gdef\@source{}\ifbrief\addvspace{3pt plus2pt}\else\addvspace{12pt plus2pt}\fi\@endparenv}
%
%%%%%%%%%%%%%%%%%%%%%% endpara and numberedpara %%%%%%%%%%%%%%%%%%%%%%%
%
\newenvironment{lastpara}{\par\addvspace{17pt plus2pt}%
      \noindent\ignorespaces}{\par}
%
\newenvironment{numpara}{\par
      \list{\arabic{enumi}}{\usecounter{enumi}\topsep\z@\itemsep\z@\leftmargin9pt\itemindent-9pt\labelwidth\z@\labelsep\z@\labelwidth\z@\listparindent12pt\def\makelabel##1{##1 }}}{\endlist}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Theorems %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\usepackage{amsthm}
\newtheoremstyle{break}%
 {}{}%
 {}{}%
 {\bfseries}{}% % Note that final punctuation is omitted.
 {\newline}{}

\theoremstyle{break}

\def\examplename{Example}
\newtheorem{example}{\examplename}
%
\def\theoremname{Theorem}
\newtheorem{theorem}{\theoremname}%[section]
%
\def\lemmaname{Lemma}
\newtheorem{lemma}{\lemmaname}%[section]
%
%\def\rulesname{Rule}
%\newtheorem{rules}{\rulesname}%[section]
%
\def\propositionname{Proposition}
\newtheorem{proposition}{\propositionname}%[section]
%
\def\corollaryname{Corollary}
\newtheorem{corollary}{\corollaryname}%[section]
%
\def\notationname{Notation}
\newtheorem{notation}{\notationname}%[section]
%
\def\assumptionname{Assumption}
\newtheorem{assumption}{\assumptionname}%[section]
%
\def\remarkname{Remark}
\newtheorem{remark}{\remarkname}%[section]
%
\newif\ifdefinition
\def\numdefname{Definition}
\newtheorem{numdef}{\numdefname}%[section]
%
\newtheorem{numtheorem}{Theorem}
%
\def\casename{Case}
\newtheorem{case}{\casename}%[section]
%
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Proof %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% proof* and proof are the same
% proof* is provided for compatibility with older cl style files
\newenvironment{proof*}{\begin{proof}}{\end{proof}}
%
\newenvironment{solution}{\begin{proof}[Solution.]}{\end{proof}}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Floats %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\setcounter{topnumber}{5}
\renewcommand\topfraction{.9}
\setcounter{bottomnumber}{5}
\renewcommand\bottomfraction{.9}
\setcounter{totalnumber}{10}
\renewcommand\textfraction{.09}
\renewcommand\floatpagefraction{.901}
\setcounter{dbltopnumber}{1}
\renewcommand\dbltopfraction{.9}
\renewcommand\dblfloatpagefraction{.901}
%
\newlength\abovecaptionskip
\newlength\belowcaptionskip
\setlength\abovecaptionskip{4.5\p@}
\setlength\belowcaptionskip{2.5\p@}
%
\def\FigName{figure}
%
\long\def\@makecaption#1#2{%
    \ifx\FigName\@captype
      \vskip\abovecaptionskip
      \@makefigurecaption{#1}{#2}%
    \else
      \@maketablecaption{#1}{#2}%
      \vskip\belowcaptionskip
    \fi
}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Figures %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\newcounter{figure}[chapter]
\renewcommand\thefigure{\@arabic\c@figure}
\def\fps@figure{tbp}
\def\ftype@figure{1}
\def\ext@figure{lof}
\def\fnum@figure{\figurename\nobreakspace\thefigure}
%
\newenvironment{figure}
               {\@float{figure}}
               {\end@float}
%
\newenvironment{figure*}
               {\@dblfloat{figure}}
               {\end@dblfloat}
%
\def\figlabelsep{.5em}
%
\def\@makefigurecaption#1#2{%
    {\figcaptionnumfont#1\par}
    {\figcaptionfont#2\vphantom{y}\par}\vskip-2.6pt}
%
\def\ArtDir{art/}%
%
\usepackage{epsfig}
\usepackage[figuresright]{rotating}
%
\newbox\figtempbox
\def\ArtPiece#1{\epsfbox{\ArtDir#1}}%
\let\figboxformat\leftline
%
\def\figurebox#1#2#3{%
    \@ifnextchar[{\@figurebox{#1}{#2}{#3}}{\@figurebox{#1}{#2}{#3}[]}}
%
\def\@figurebox#1#2#3[#4]{%
      \gdef\@figscale{#3}
      \gdef\@frtharg{#4}
      \ifx\@frtharg\empty
         \global\figheight=#1
         \global\figwidth=#2
      \else 
         \setbox\figtempbox=\hbox{\ifx\@figscale\empty\else\epsfxsize\@figscale\fi\epsfbox{\ArtDir#4}}%
         \global\figwidth=\wd\figtempbox
         \global\figheight=\ht\figtempbox
      \fi
      {\figboxformat{\figbox}}%%
}%
%
\def\figbox{%
     \ifx\@frtharg\empty  
       \noindent\vbox{\hsize\figwidth%
              \hrule\hbox to\figwidth{\vrule\hfill\vbox to\figheight{\hsize\figwidth\vfill}\vrule}\hrule}%
     \else
        \vbox{\vskip.8pt\hsize\figwidth
              \hbox to\figwidth{\vbox to\figheight{\hsize\figwidth\box\figtempbox}}}%
     \fi
}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Tables %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\newcounter{table}[chapter]
\renewcommand\thetable{\@arabic\c@table}
\def\fps@table{tbp}
\def\ftype@table{2}
\def\ext@table{lot}
\def\fnum@table{\tablename\nobreakspace\thetable}
%
\newenvironment{table}
               {\@float{table}}
               {\end@float}
%
\newenvironment{table*}
               {\@dblfloat{table}}
               {\end@dblfloat}
%
\def\@maketablecaption#1#2{%
    \hrule height1pt\par\vskip12pt
    {\tablecaptionnumfont#1\par}%
    {\tablecaptionfont#2\vphantom{y}\par}}
%
\def\tbl#1#2{\tablefont%
  \setbox\tempbox\hbox{\tablefont#2}%
  \tabledim\hsize
  \advance\tabledim-\wd\tempbox
  \ifdim\tabledim>0pt
        \divide\tabledim2
  \else
        \global\tabledim0pt
  \fi
  \global\tableleftskip\tabledim
  \global\tablerightskip\tabledim
  \caption{#1}%
  {\box\tempbox}}%
%
\def\TCH#1{\TCHfont#1}%
%
\def\x{@{\extracolsep{\fill}}}
\def\toprule{\Hline\\[-5.5pt]}
\def\colrule{\\[-7.5pt]\Hline\\[-5pt]}
\def\botrule{}
\def\crule#1{\\[-7.5pt]\CLINE{#1}\\[-5pt]}
%
\def\Hline{%
  \noalign{\ifnum0=`}\fi\hrule \@height .5pt \futurelet%\@height \arrayrulewidth
   \@tempa\@xhline}
%
\newenvironment{tabnote}{\par\tabnotefont
   }{\par}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  End Floats %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Math %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\def\arraystretch{1}
\setlength\arraycolsep{1.5\p@}
\setlength\tabcolsep{6\p@}
\setlength\arrayrulewidth{.4\p@}
\setlength\doublerulesep{2\p@}
\setlength\tabbingsep{\labelsep}
\setlength\fboxsep{3\p@}
\setlength\fboxrule{.4\p@}
%
\setlength\columnsep{24\p@}
\setlength\columnseprule{0\p@}
%
\@addtoreset{equation}{chapter}
\renewcommand\theequation{\arabic{equation}}
\def\@eqnnum{{\reset@font\rmfamily\quad (\theequation)}}
%
\def\bstrut{\vrule width0pt depth6pt}
\def\tstrut{\vrule width0pt height9pt}
\jot=6pt
%%
%
\def\text#1{\mathchoice
        {\hbox{\fontsize{\tf@size}{\tf@size}\selectfont#1}}%
        {\hbox{\fontsize{\tf@size}{\tf@size}\selectfont#1}}%
        {\hbox{\fontsize{\sf@size}{\sf@size}\selectfont#1}}%
        {\hbox{\fontsize{\ssf@size}{\ssf@size}\selectfont#1}}}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  End Math %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Footnote %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\def\thanks#1{\footnotemark
    \protected@xdef\@thanks{\@thanks\protect\footnotetext[\the\c@footnote]{#1}}}
%
\def\@makefnmark{\smash{\hbox{\@textsuperscript{\normalfont\@thefnmark}}}}
%
\renewcommand\footnoterule{%
  \kern-4\p@
  \hrule width 15pc height.5pt depth\z@
  \kern 3.5\p@}
%
\@addtoreset{footnote}{chapter}
\renewcommand\thefootnote{\arabic{footnote}}
%
\def\@fnsymbol#1{\ifcase#1\or \ensuremath{*}\or \ensuremath{**}\or\ensuremath{\dagger}\or\ensuremath{\ddagger}\or
   \S\or\|\or\#\or**\or\ensuremath{\dagger\dagger}\or\ensuremath{\ddagger\ddagger} 
   \or\S\S\or\|\hskip-1pt\|\or\#\#\or ***\or\ensuremath{\dagger\dagger\dagger}\or\ensuremath{\ddagger\ddagger\ddagger}\else\@ctrerr\fi\relax}
%
\newdimen\@footmax
\def\footmax#1{%
  \setbox\tempbox\hbox{\footnotesize#1}
  \global\@footmax\wd\tempbox}
%
\footmax{00}
%
\def\domkfnmark{\noindent\hskip-12pt\hbox to 12pt{\hbox to \@footmax{\hss$\@thefnmark$}\hss}}
\def\dofnformat{\parindent8pt\leftskip12pt\rightskip0pt plus1fill}
%
\long\def\@makefntext#1{\dofnformat%
    \domkfnmark#1}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  End Footnote %%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Page styles  %%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\def\cyanColor#1{\special{color push cmyk 1 0 0 0}#1\special{color pop}}
\def\whiteColor#1{\special{color push cmyk 0 0 0 0}#1\special{color pop}}
%
\def\folio{{\foliofont\thepage}}
%
\def\bookrev#1{\gdef\@bookrev{#1}}
\bookrev{Book Reviews}
%
\def\briefhead#1{\gdef\@briefhead{#1}}
\briefhead{Briefly Noted}
%
\def\ps@headings{%
    \def\@oddfoot{\hfill{\folio}}
    \def\@evenfoot{{\folio}\hfill}
    \def\@evenhead{{\rhfont\@jname\hfill\@jinfo}}%
    \def\@oddhead{\ifbookreview{\rhfont\hfill\@bookrev}\else\ifshortpaper{\rhfont\hfill\@sptitle}\else{\rhfont\@rauthor\hfill\@rtitle}\fi\fi}%
    \let\@mkboth\markboth
}
%
\def\ps@empty{%
      \def\@oddfoot{\hfill\lower\blindfoliodrop\hbox{\thepage}\hfill}
      \let\@evenfoot\@oddfoot
      \def\@evenhead{}%
      \def\@oddhead{}%
      \let\@mkboth\markboth
}
%
\newcommand{\footmark}{\copyright\ \@jyear\ Association for Computational Linguistics}
%
\def\ps@titlepage{\let\@mkboth\@gobbletwo%
  \def\@oddfoot{\footnotesize\footmark\hfill}
  \def\@evenfoot{\footnotesize\hfill\footmark}
  \def\@oddhead{}\let\@evenhead\@oddhead}
%
\def\ps@pageonly{\let\@mkboth\@gobbletwo%
    \def\@oddfoot{\hfill{\folio}}
    \def\@evenfoot{{\folio}\hfill}
  \def\@oddhead{}\let\@evenhead\@oddhead}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  End Page styles  %%%%%%%%%%%%%%%%%%%%%%%%
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Bibliography Section   %%%%%%%%%%%%%%%%%%
%
% Bibliography
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%% Citation forms:
%%%
%%% Macro       Output format
%%% ----------- -----------------------------------------
%%% \cite:      (Dewey, 1988)
%%%             (Dewey, 1988, page 15)
%%%             (Dewey, 1988; Cheatham, 1987; Howe, 1903)
%%% \namecite:  Dewey (1988)
%%%             Dewey (1988, page 15)
%

\newlength\bibleftmargin
\newlength\biblabelsep
\newlength\bibitemsep
\newlength\bibparsep
%
\setlength\bibleftmargin{9pt}
\setlength\biblabelsep  {3pt}
\setlength\bibitemsep   {0pt}
\setlength\bibparsep    {0pt}
%
\def\bibhead#1{\bibitem{}\null\par\bgroup\nobreak{\leftskip-\leftmargin\hskip\leftmargin\bfseries #1\par}\nobreak\egroup}
%
\newenvironment{thebibliography}[1]
   {\par%
   \ifx\withintwocol{true}\else%\starttwocolumn
   \fi
    \def\@tempa{#1}%
    \ifx\@tempa\@empty
       \list{}{%
          \labelwidth0pt\labelsep0pt
          \leftmargin\bibleftmargin
          \itemindent-\bibleftmargin
          \itemsep\bibitemsep
          \parsep\bibparsep
          \usecounter{enumiv}%
          \let\p@enumiv\@empty}%
    \else
       \setbox\tempbox\hbox{\@tempa.}
       \tempdimen\wd\tempbox
       \def\@biblabel##1{\hbox to \tempdimen{\hfill##1.}}
       \list{\@biblabel{\arabic{enumiv}}}%
          {\settowidth\labelwidth{\@biblabel{#1}}%
           \labelsep\biblabelsep\leftmargin\labelsep
           \advance\leftmargin\labelwidth
           \itemindent0pt
           \itemsep\bibitemsep
           \parsep\bibparsep
           \usecounter{enumiv}%
           \let\p@enumiv\@empty
           \renewcommand\theenumiv{\arabic{enumiv}}}%
    \fi
    \sloppy\clubpenalty4000\widowpenalty4000\sfcode`\.=\@m
   }{%
    \def\@noitemerr{\@latex@warning{Empty `thebibliography' environment}}%
    \endlist
   }

\def\@lbibitem[#1]#2{\item[]\if@filesw 
      { \def\protect##1{\string ##1\space}\immediate
        \write\@auxout{\string\bibcite{#2}{#1}}\fi\ignorespaces}}

\def\@bibitem#1{\item\if@filesw \immediate\write\@auxout
       {\string\bibcite{#1}{\the\c@enumi}}\fi\ignorespaces}


\usepackage{natbib}
 \setcitestyle{aysep={}}	% no comma between author and year
 \renewcommand{\cite}{\citep}	% to get "(Author Year)" with natbib
 \newcommand{\namecite}{\citet}	% to get "Author (Year)" with natbib
 \def\bibfont{\small\raggedright}
 \def\bibsection{\xhead*{References}}

% 
\newcommand\newblock{}
%
% endnotes; same environment as bibliography:
%
\def\theendnotes{\small\parindent=0pt\par\vspace{14pt}{\bf Notes}\par\vspace{2pt}\everypar{\hangindent=1em\hangafter=1}\raggedright}
\def\endtheendnotes{\par\vskip14pt plus4pt }
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  End Bibliography Section %%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Contents List  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\def\dotfill{%
  \leavevmode
  \cleaders \hb@xt@ .44em{\hss.\hss}\hfill
  \kern\z@}
%
\newcommand\@pnumwidth{1.55em}
\newcommand\@tocrmarg {2.55em}
\newcommand\@dotsep{4.5}
\setcounter{tocdepth}{2}
%
\newcommand\l@section      {\@dottedtocline{1}{1.5em}{2.3em}}
\newcommand\l@subsection   {\@dottedtocline{2}{3.8em}{3.2em}}
\newcommand\l@subsubsection{\@dottedtocline{3}{7.0em}{4.1em}}
\newcommand\l@paragraph    {\@dottedtocline{4}{10em}{5em}}
\newcommand\l@subparagraph {\@dottedtocline{5}{12em}{6em}}
\let\l@table\l@figure
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  Appendix  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% command to add a section to the appendix
\newcommand{\appendixsection}[1]{\addtocounter{section}{1}%
   \setcounter{table}{0}
   \setcounter{figure}{0}
   \setcounter{equation}{0}
  \section*{Appendix \Alph{section}: #1}%
}
%
\newcommand\appendix{%
   \setcounter{section}{0}
   \renewcommand{\theequation}{\Alph{section}.\arabic{equation}}
}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% End Appendix %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%% Document & End Document %%%%%%%%%%%%%%%%%%%%%
%
%\def\@watermark{\offinterlineskip\vbox to 0pt{\setlength\overfullrule{0pt}\vskip12pc\hskip2pc\begin{turn}{45}\hbox to \textheight{\hss\grayColor{{\sffamily\fontsize{107.5}{107.5pt}\selectfont\bfseries spi}\hskip16pt\raise10pt\hbox{\sffamily\fontsize{50}{50}\selectfont\bfseries publisher services}}\hss}\end{turn}}\vskip0pt}
%
\def\@questionmark{\vbox to 0pt{\vskip13pc\hskip-5pc
                  \hbox to \textwidth{\fontsize{570}{570}\selectfont ?\hss}}}
\def\questionmark#1{\xdef\@questionmark{#1}}%
%
%\def\draftnote{\vbox to 0pt{\offinterlineskip%
      %\hbox to \trimwidth{\hfill\footnotesize\jobname\vphantom{q}\qquad\today\qquad\currenttime\hfill}\par\@questionmark}}%
%
\def\document{\endgroup
  \ifx\@unusedoptionlist\@empty\else
    \@latex@warning@no@line{Unused global option(s):^^J%
            \@spaces[\@unusedoptionlist]}%
  \fi
  \@colht\textheight
  \@colroom\textheight \vsize\textheight
  \columnwidth\textwidth
  \@clubpenalty\clubpenalty
  \if@twocolumn
    \advance\columnwidth -\columnsep
    \divide\columnwidth\tw@ \hsize\columnwidth \@firstcolumntrue
  \fi
  \hsize\columnwidth \linewidth\hsize
  \begingroup\@floatplacement\@dblfloatplacement
    \makeatletter\let\@writefile\@gobbletwo
    \global \let \@multiplelabels \relax
    \@input{\jobname.aux}%
  \endgroup
  \if@filesw
    \immediate\openout\@mainaux\jobname.aux
    \immediate\openout\@mainqry=\jobname.qry
    \immediate\write\@mainaux{\relax}%
  \fi
  \process@table
  \let\glb@currsize\@empty  %% Force math initialisation.
  \normalsize
  \everypar{}%
  \@noskipsecfalse
  \let \@refundefined \relax
  \let\AtBeginDocument\@firstofone
  \@begindocumenthook
  \ifdim\topskip<1sp\global\topskip 1sp\relax\fi
  \global\@maxdepth\maxdepth
  \global\let\@begindocumenthook\@undefined
  \ifx\@listfiles\@undefined
    \global\let\@filelist\relax
    \global\let\@addtofilelist\@gobble
  \fi
  \gdef\do##1{\global\let ##1\@notprerr}%
  \@preamblecmds
  \global\let \@nodocument \relax
  \global\let\do\noexpand
  \ignorespaces}
%
\def\enddocument{%
   \ifx\@biography\@empty\else{\par\ifbrief\vskip10pt\fi\biofont\noindent\@biography\par}\fi
   \@enddocumenthook
   \@checkend{document}%
   \immediate\closeout\@mainqry
   %\ifquery
   %   \process@queries\clearpage
   %\else
      \ifodd\c@page\clearpage\thispagestyle{empty}\null\clearpage\else\clearpage\fi
   %\fi
%   \ifquery\clearpage\else\ifodd\c@page\clearpage\thispagestyle{empty}\null\clearpage\else\clearpage\fi\fi
   \begingroup
     \if@filesw
       \immediate\write\@mainaux{\string\questionmark{}}%
       \immediate\closeout\@mainaux
       \let\@setckpt\@gobbletwo
       \let\@newl@bel\@testdef
       \@tempswafalse
       \makeatletter \input\jobname.aux
     \fi
     \@dofilelist
     \ifdim \font@submax >\fontsubfuzz\relax
       \@font@warning{Size substitutions with differences\MessageBreak
                  up to \font@submax\space have occured.\@gobbletwo}%
     \fi
     \@defaultsubs
     \@refundefined
     \if@filesw
       \ifx \@multiplelabels \relax
         \if@tempswa
           \@latex@warning@no@line{Label(s) may have changed.
               Rerun to get cross-references right}%
         \fi
       \else
         \@multiplelabels
       \fi
     \fi
   \endgroup
   \deadcycles\z@\@@end}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Trimmarks  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\def\trimmarks{%
  \vbox to 0pt{\offinterlineskip%
    \vskip-25pt\parindent0pt
    %\draftnote
    \offinterlineskip}%
    \vbox to 0pt{\hsize\trimwidth\offinterlineskip
    \parindent0pt\leftskip0pt\rightskip0pt
    \vbox to \trimheight{\offinterlineskip\parindent0pt
    \hbox to \trimwidth{\vbox to 2pc{\vskip-3.5pc\hbox{\vrule height2pc width\trimrule}}\raisebox{2pc}{\hbox{\hskip-3.5pc\vrule width2pc height\trimrule}}\hfill
      \raisebox{2pc}{\vrule width2pc height\trimrule\hskip-3.75pc}
      \vbox to 2pc{\vskip-3.5pc\hbox{\vrule height2pc width\trimrule}}%
    }\vfill
    \hbox to \trimwidth{\hbox{\hskip-3.5pc\vrule height\trimrule width2pc}\vbox to 3pc{\vspace*{4.5pc}\hbox{\hskip1.5pc\vrule width\trimrule height2pc}}\hfill
    \vbox to 3.5pc{\vskip5pc\hbox{\vrule height2pc width\trimrule}}\rlap{\hskip1.5pc\vrule width2pc height\trimrule}}}}
\insidedraftrules}
%
\def\insidedraftrules{\setlength\overfullrule{0pt}\vbox to 0pt{%
  \offinterlineskip\parindent0pt
  \vskip \topmargin
  \tempdimen\normaltextheight
  \advance\tempdimen\headheight
  \advance\tempdimen\headsep
  \moveright\@themargin
  \vbox{\vbox to 0pt{\vskip\headheight\vskip\headsep
   \vrule height\draftrule width\textwidth}
   \hbox{\fboxsep0pt\fboxrule\draftrule
        \fbox{\vbox to \tempdimen
                    {\hsize\textwidth\hskip\textwidth}}}}}}%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Output Routine  %%%%%%%%%%%%%%%%%%%%%%%%%%
%
\def\@outputpage{%
\begingroup%
  \let \protect \noexpand
  \@resetactivechars
  \@parboxrestore
  \shipout \vbox{%
    \set@typeset@protect
    \aftergroup \endgroup
    \aftergroup \set@typeset@protect
  \if@specialpage
    \global\@specialpagefalse\@nameuse{ps@\@specialstyle}%
  \fi
  \if@twoside
    \ifodd\count\z@ \let\@thehead\@oddhead \let\@thefoot\@oddfoot
         \let\@themargin\oddsidemargin
    \else \let\@thehead\@evenhead
       \let\@thefoot\@evenfoot \let\@themargin\evensidemargin
    \fi
  \fi
  \reset@font
  \normalsize
  \baselineskip\z@skip \lineskip\z@skip \lineskiplimit\z@
    \@begindvi\trimmarks
    \vskip \topmargin
    \moveright\@themargin \vbox {%
      \setbox\@tempboxa \vbox to\headheight{%
        \vfil
        \color@hbox
          \normalcolor
          \hb@xt@\textwidth {%
            \let \label \@gobble
            \let \index \@gobble
            \let \glossary \@gobble
            \@thehead
            }%
        \color@endbox
        }%
      \dp\@tempboxa \z@
      \box\@tempboxa
      \vskip \headsep
      \box\@outputbox
      \baselineskip \footskip
      \color@hbox
        \normalcolor
        \hb@xt@\textwidth{%
          \let \label \@gobble
          \let \index \@gobble
          \let \glossary \@gobble
          \@thefoot
          }%
      \color@endbox
      }%
    }%
\global \@colht \textheight
\stepcounter{page}%
\let\firstmark\botmark
  \ifodd\c@page
     \ifspreadlong\global\spreadlongfalse
     \enlargethispage{\@spreadlong}\fi
  \fi
}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Miscelleneous %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\newcommand\callout[1]{\ifdraftrules\marginpar{\bf#1}\fi}
%
\def\comment{\@ifnextchar[\@comment{\@comment[\relax]}}
\def\@comment[#1]#2{\marginpar{\ifx#1\relax\else\vspace*{#1}\fi\bf\raggedright#2}}
%
\def\pos@of@dbl@text{0pt}
\def\movetext{\vrule height\z@ depth\pos@of@dbl@text width\z@}
%
\def\acknowledgments{\par\gdef\withintwocol{true}%\starttwocolumn
   %\subsection
   \xhead*{Acknowledgments}%\vspace*{2pt}
   \ackfont}
\def\endacknowledgments{\par}
%
\newenvironment{displaytext}{\par\addvspace{14pt plus2pt}\bgroup\hangindent18pt\parindent\z@\let\sc\scshape\let\it\itshape}{\par\egroup\addvspace{12pt plus2pt}\@endparenv}
%
\newenvironment{algorithm}{\par\list{}{\leftmargin\z@\labelwidth\z@\labelsep\z@\itemsep6pt\topsep12pt plus2pt
                        \let\makelabel\algorithmlabel}}{\endlist}
\def\algorithmlabel#1{{\bfseries #1: }}
%
\newenvironment{dialogue}{\par\addvspace{12pt plus2pt}\normalsize\hangindent18pt\parindent\z@}{\par\addvspace{12pt plus2pt}\@endparenv}
%
\newenvironment{deflist}{\par\list{}{\leftmargin18pt\rightmargin18pt\itemindent-\leftmargin\labelwidth\z@\labelsep\z@\itemsep6pt\topsep12pt plus2pt
                        \let\makelabel\definitionlabel}\raggedright}{\endlist}
\def\definitionlabel#1{{\bfseries #1:} }
%
\newcounter{rules}
\newenvironment{rules}{\par\addvspace{12pt plus2pt}
   \global\addtocounter{rules}{1}\noindent{\bfseries Rule \therules: }\noindent\ignorespaces%
   }{\par\@endparenv}
%
\@namedef{rules*}{\par\addvspace{12pt plus2pt}\noindent{\bfseries Rule: }\noindent\ignorespaces}
\@namedef{endrules*}{\par\@endparenv}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\def\str@right{right}
\def\str@left{left}
%
\newwrite\@mainqry
%
\newcounter{qcount}
\newdimen\qcountdim\qcountdim0pt
\def\qtoafont{\reset@font\normalsize\bfseries\raggedright}
%\def\queryfont{\fontsize{9}{10.5}\selectfont}
\def\qlist@headfont{\fontsize{15}{15}\selectfont\centering}
\def\qlist@subheadfont{\fontsize{12}{14}\selectfont\bfseries}
\def\qlist@font{\fontsize{10}{12}\selectfont}
%
\def\qtoa{\@ifnextchar[{\@qtoa}{\@qtoa[\@empty]}}
\def\@qtoa[#1]#2{\@ifnextchar[{\@@qtoa[#1]#2}{\@@qtoa[#1]#2[0pt]}}
\def\@@qtoa[#1]#2[#3]{\global\addtocounter{qcount}{1}%
   \protected@write{\@mainqry}{}{\string\item{} #2\par}%
   \@question{#1}{Q\theqcount}{#3}\ignorespaces}
%
\newenvironment{qlist}{\par\list{}{\usecounter{enumi}\topsep30pt\labelsep5pt\settowidth{\labelwidth}{Q\theqcount:}\leftmargin\labelwidth\labelsep5pt\advance\leftmargin\labelsep\itemsep\baselineskip\rightmargin\z@\def\makelabel##1{\hbox
      to\labelwidth{\hss Q\theenumi.}}}}{\endlist}
%
%
\def\qtom{\@ifnextchar[{\@qtom}{\@qtom[\@empty]}}
\def\@qtom[#1]#2{\@ifnextchar[{\@@qtom[#1]#2}{\@@qtom[#1]#2[0pt]}}
\def\@@qtom[#1]#2[#3]{\@question{#1}{#2}{#3}\ignorespaces}
%
\def\@question#1#2#3{%
   \ifvmode%
      \@@question{#1}{#2}{#3}%
   \else%
      \vadjust{\vbox to 0pt{%
      \vskip-7.5pt\@@question{#1}{\qtoafont#2}{#3}\vskip7.5pt}}%
   \fi}%
%
\def\@@question#1#2#3{\edef\@argone{#1}\hbox to \hsize{%
   \if@twocolumn%
      \if@firstcolumn
         \ifx\@argone\str@right
            \hfill\rlap{\hskip\marginparsep%
               \vbox to 0pt{\hsize\marginparwidth\vspace*{#3}{#2}\endgraf\vss}}%
         \else%
            \tempdimen\columnwidth\advance\tempdimen-\hsize%
            \ifdim\columnwidth>\hsize\hskip-\tempdimen\fi%
            \hskip-\marginparsep\llap{\hskip\columnwidth%
               \vbox to 0pt{\hsize\marginparwidth\vspace*{#3}{#2}\endgraf\vss}}%
         \fi%
      \else
         \ifx\@argone\str@left
            \tempdimen\columnwidth\advance\tempdimen-\hsize%
            \ifdim\columnwidth>\hsize\hskip-\tempdimen\fi%
            \hskip-\marginparsep\llap{\hskip\columnwidth%
               \vbox to 0pt{\hsize\marginparwidth\vspace*{#3}{#2}\endgraf\vss}}%
         \else
            \hfill\rlap{\hskip\marginparsep%
               \vbox to 0pt{\hsize\marginparwidth\vspace*{#3}{#2}\endgraf\vss}}%
         \fi%
      \fi%
   \else%
      \ifx\@argone\str@left%
         \tempdimen\columnwidth\advance\tempdimen-\hsize%
         \ifdim\columnwidth>\hsize\hskip-\tempdimen\fi%
         \hskip-\marginparsep\llap{\hskip\columnwidth%
            \vbox to 0pt{\hsize\marginparwidth\vspace*{#3}{#2}\endgraf\vss}}%
      \else%
         \hfill\rlap{\hskip\marginparsep%
         \vbox to 0pt{\hsize\marginparwidth\vspace*{#3}{#2}\endgraf\vss}}%
      \fi%
   \fi}\ignorespaces}%
%
\newif\ifspreadlong
\def\spreadlong#1{\ifodd\c@page\wlog{Ignoring spreadlong}
                  \else
                     \spreadlongtrue\gdef\@spreadlong{#1}%
                     \enlargethispage{#1}%
                  \fi}
%
\def\leaflong#1{\enlargethispage{#1}}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\let\dochead\sptitle
\let\quote\extract
\let\endquote\endextract
\let\tcaption\tbl
\let\unenumerate\unnumlist
\let\endunenumerate\endunnumlist
\let\definition\numdef
\let\enddefinition\endnumdef
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%\let\starttwocolumn\relax
\newdimen\@twocolsep\@twocolsep=16pt
\def\twocolsep#1{\global\advance\@twocolsep by #1\relax}
\newbox\partialpage
\def\starttwocolumn{%
  {\output={\global\setbox\partialpage=\vbox{\unvbox255}}\newpage}%
  \twocolumn[\unvbox\partialpage\vspace{\@twocolsep}]%
}
%
\def\cleardoublepage{\clearpage\if@twoside \ifodd\c@page\else
    \hbox{}\newpage\thispagestyle{empty}\if@twocolumn\hbox{}\newpage\thispagestyle{empty}\fi\fi\fi}
%
\def\onecolumnnew{%
  %\clearpage
  \global\columnwidth\textwidth
  \global\hsize\columnwidth
  \global\linewidth\columnwidth
  \global\@twocolumnfalse
  \col@number \@ne
  \@floatplacement}
%
\def \twocolumnnew {%
  %\clearpage
  \global\columnwidth\textwidth
  \global\advance\columnwidth-\columnsep
  \global\divide\columnwidth\tw@
  \global\hsize\columnwidth
  \global\linewidth\columnwidth
  \global\@twocolumntrue
  \global\@firstcolumntrue
  \col@number \tw@
  \@ifnextchar [\@topnewpage\@floatplacement
}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\newcount\tblcolcount
\newskip\tcsepbefore
%
\def\@addamp{\global\advance\tblcolcount\@ne\relax%
  \if@firstamp
    \@firstampfalse
  \else
    \edef\@preamble{\@preamble &}%
  \fi}
%
\def\CLINE#1{\expandafter\@CLINE#1\@nil}
\def\@CLINE#1-#2\@nil{%
  \omit%
  \@multicnt#1%
  \advance\@multispan\m@ne%
  \ifnum\@multicnt=\@ne\@firstofone{&\omit}\fi%
  \@multicnt#2%
  \advance\@multicnt-#1%
  \advance\@multispan\@ne%
  \ifthenelse{#1=1}{\tcsepbefore\z@}{\tcsepbefore\tabcolsep}%
  \ifthenelse{\the\tblcolcount=#2}{%
     {\kern\tcsepbefore\leaders\hrule\@height.5pt\hfill\kern\tabcolsep}%
   }{%
     \kern\tcsepbefore\leaders\hrule\@height.5pt\hfill\kern\tabcolsep}%
  \cr
  \noalign{\vskip-\arrayrulewidth}}%
%
\def\fulltabular{\global\tblcolcount\z@\def\@halignto{to \textwidth}\@tabular}
\def\endfulltabular{\endtabular\global\tblcolcount\z@}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\usepackage{amsfonts,amssymb}
\usepackage{multicol}
\multicolsep = 14pt plus 4pt% minus 3pt
%
%
\usepackage{dcolumn}
\newcolumntype{D}[3]{>{\DC@{#1}{#2}{#3}}l<{\DC@end}}
%
\AtBeginDocument{%
\@ifpackageloaded{lingmacros}{%
\long\def\@enumsentence[#1]#2{\begin{list}{}{\topsep12pt%
\labelsep6pt\leftmargin30pt\labelwidth30pt\advance\leftmargin by\labelsep\advance\leftmargin by\widelabel \advance\labelwidth by \widelabel}
\item[#1] #2
\end{list}}
}{}
}
%
\AtBeginDocument{

\DeclareFontFamily{OML}{pns}{}
\DeclareFontShape{OML}{pns}{m}{n}{<->  zplmr7m }{}
\DeclareSymbolFont{itgreek}{OML}{zplmr7m}{m}{n}
\SetSymbolFont{itgreek}{normal}{OML}{pns}{m}{n}

%%%%%%%%%%%%%%%%%%% Uppercase Greek Italic  %%%%%%%%%%%%%%%%%%%%%%%%%%
  \DeclareMathSymbol{\slGamma}  {\mathalpha}{itgreek}{"00}
  \DeclareMathSymbol{\slDelta}  {\mathalpha}{itgreek}{"01}
  \DeclareMathSymbol{\slTheta}  {\mathalpha}{itgreek}{"02}
  \DeclareMathSymbol{\slLambda} {\mathalpha}{itgreek}{"03}
  \DeclareMathSymbol{\slXi}     {\mathalpha}{itgreek}{"04}
  \DeclareMathSymbol{\slPi}     {\mathalpha}{itgreek}{"05}
  \DeclareMathSymbol{\slSigma}  {\mathalpha}{itgreek}{"06}
  \DeclareMathSymbol{\slUpsilon}{\mathalpha}{itgreek}{"07}
  \DeclareMathSymbol{\slPhi}    {\mathalpha}{itgreek}{"08}
  \DeclareMathSymbol{\slPsi}    {\mathalpha}{itgreek}{"09}
  \DeclareMathSymbol{\slOmega}  {\mathalpha}{itgreek}{"0A}
  \DeclareMathSymbol{\slupDelta}{\mathalpha}{itgreek}{"01}
  \DeclareMathSymbol{\slupOmega}{\mathalpha}{itgreek}{"0A}

%%%%%%%%%%%%%%%%%%% Lowercase Greek Italic  %%%%%%%%%%%%%%%%%%%%%%%%%%
\DeclareMathSymbol{\slalpha}{\mathalpha}{itgreek}{"0B}
\DeclareMathSymbol{\slbeta}{\mathalpha}{itgreek}{"0C}
\DeclareMathSymbol{\slgamma}{\mathalpha}{itgreek}{"0D}
\DeclareMathSymbol{\sldelta}{\mathalpha}{itgreek}{"0E}
\DeclareMathSymbol{\slepsilon}{\mathalpha}{itgreek}{"0F}
\DeclareMathSymbol{\slzeta}{\mathalpha}{itgreek}{"10}
\DeclareMathSymbol{\sleta}{\mathalpha}{itgreek}{"11}
\DeclareMathSymbol{\sltheta}{\mathalpha}{itgreek}{"12}
\DeclareMathSymbol{\sliota}{\mathalpha}{itgreek}{"13}
\DeclareMathSymbol{\slkappa}{\mathalpha}{itgreek}{"14}
\DeclareMathSymbol{\sllambda}{\mathalpha}{itgreek}{"15}
\DeclareMathSymbol{\slmu}{\mathalpha}{itgreek}{"16}
\DeclareMathSymbol{\slnu}{\mathalpha}{itgreek}{"17}
\DeclareMathSymbol{\slxi}{\mathalpha}{itgreek}{"18}
\DeclareMathSymbol{\slpi}{\mathalpha}{itgreek}{"19}
\DeclareMathSymbol{\slrho}{\mathalpha}{itgreek}{"1A}
\DeclareMathSymbol{\slsigma}{\mathalpha}{itgreek}{"1B}
\DeclareMathSymbol{\sltau}{\mathalpha}{itgreek}{"1C}
\DeclareMathSymbol{\slupsilon}{\mathalpha}{itgreek}{"1D}
\DeclareMathSymbol{\slphi}{\mathalpha}{itgreek}{"1E}
\DeclareMathSymbol{\slchi}{\mathalpha}{itgreek}{"1F}
\DeclareMathSymbol{\slpsi}{\mathalpha}{itgreek}{"20}
\DeclareMathSymbol{\slomega}{\mathalpha}{itgreek}{"21}
\DeclareMathSymbol{\slvarepsilon}{\mathalpha}{itgreek}{"22}
\DeclareMathSymbol{\slvartheta}{\mathalpha}{itgreek}{"23}
\DeclareMathSymbol{\slvarpi}{\mathalpha}{itgreek}{"24}
\DeclareMathSymbol{\slvarrho}{\mathalpha}{itgreek}{"25}
\DeclareMathSymbol{\slvarsigma}{\mathalpha}{itgreek}{"26}
\DeclareMathSymbol{\slvarphi}{\mathalpha}{itgreek}{"27}
}

%
\medmuskip=4mu 
\thickmuskip=5mu 
%
\pagestyle{headings}
\pagenumbering{arabic}
%
%\makeindex
\frenchspacing
\sloppy
%
%\ifprinter
%   \voffset-6.03pc
%   \hoffset-6.03pc
%\else
   \voffset-1pc
   \hoffset-1.5pc
%\fi
%
\endinput

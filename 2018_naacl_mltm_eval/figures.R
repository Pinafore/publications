library(ggplot2)
library(reshape)
library(grid)
library(gridExtra)
library(xtable)
library(Rmisc)
require(ggplot2)
require(scales)


datadir <- function(filename){
    val <- paste(directory, 'data/', filename, sep='')
    #print(val)
    return(val)
}

gfxdir <- function(filename) {
    val <- paste(directory, 'auto_fig/', filename, sep='')
    return(val)
}

directory = "2018_naacl_mltm_eval/"

lang_order <- c("EN-ZH", "EN-TR", "EN-SV", "EN-RO", "EN-TL", "EN-AM")


##################
# Cardinality Plot


card_height <- 1.7
card_width <- 1.35
legend <- .7
card_scale <- 1.3

add_card 		= 	read.table(datadir("/cnpmi_addcard_wiki.dat"), header = TRUE)


add_card$lang_id <- factor(add_card$lang_id, levels = lang_order)


add_card$ref_corpus_f = factor(add_card$ref_corpus, levels=c('Wikipedia'))
add_card_plot 	= 	ggplot(	add_card, aes(add_card$card_id, add_card$npmi_score, colour = add_card$lang_id)) +
					geom_errorbar(aes(ymin=add_card$npmi_score-add_card$error, ymax=add_card$npmi_score+add_card$error),width=0.5) +
					geom_point() + geom_smooth() +
					scale_y_continuous(breaks = scales::pretty_breaks(n = 5)) +
					facet_wrap("add_card$ref_corpus_f", scale="free", as.table=TRUE) +
					xlab("Cardinality") + ylab("CNPMI") +
					theme(legend.position =	"none")
add_card_plot
ggsave(add_card_plot, filename = gfxdir("add_card_npmi_wiki.pdf"), height=card_height, width=card_width, scale=card_scale)


add_card 		= 	read.table(datadir("/cnpmi_addcard_bible.dat"), header = TRUE)

add_card$lang_id <- factor(add_card$lang_id, levels = lang_order)

add_card$ref_corpus_f = factor(add_card$ref_corpus, levels=c('Bible'))
add_card_plot 	= 	ggplot(	add_card, aes(add_card$card_id, add_card$npmi_score, colour = add_card$lang_id)) +
					geom_errorbar(aes(ymin=add_card$npmi_score-add_card$error, ymax=add_card$npmi_score+add_card$error),width=0.5) +
					geom_point() + geom_smooth() +
					scale_y_continuous(breaks = scales::pretty_breaks(n = 5), limits=c(min(add_card$npmi_score)-0.003,max(add_card$npmi_score)+0.0013)) +
					facet_wrap("add_card$ref_corpus_f", scale="free", as.table=TRUE) +
					xlab("Cardinality") + ylab("CNPMI") +
					theme(legend.position = "none")
add_card_plot
ggsave(add_card_plot, filename = gfxdir("add_card_npmi_bible.pdf"), height=card_height, width=card_width, scale=card_scale)

add_card 		= 	read.table(datadir("/cnpmi_addcard_mta.dat"), header = TRUE)
add_card$lang_id <- factor(add_card$lang_id, levels = lang_order)
add_card$ref_corpus_f = factor(add_card$ref_corpus, levels=c('Wiktionary'))
add_card_plot 	= 	ggplot(	add_card, aes(add_card$card_id, add_card$npmi_score, colour = add_card$lang_id)) +
					geom_errorbar(aes(ymin=add_card$npmi_score-add_card$error, ymax=add_card$npmi_score+add_card$error),width=0.5) +
					geom_point() + geom_smooth() +
					scale_y_continuous(breaks = scales::pretty_breaks(n = 4)) +
					facet_wrap("add_card$ref_corpus_f", scale="free", as.table=TRUE) +
					xlab("Cardinality") + ylab("MTA") +
					theme(legend.position = "right") +
					guides(	col = guide_legend(ncol = 1)) +
					labs(colour="Languages")
add_card_plot
ggsave(add_card_plot, filename = gfxdir("add_card_npmi_mta.pdf"), height=card_height, width=card_width+legend, scale=card_scale)


####################################
# Document links plot

dl_width <- 3
dl_height <- 1.25
dl_legend <- .75
dl_scale <- 1.2



add_dl_wiki 	= 	read.table(datadir("npmi-adding_document_link-Wikipedia.dat"), header = TRUE)
add_dl_bible 	= 	read.table(datadir("npmi-adding_document_link-Bible.dat"), header = TRUE)

add_dl <- rbind(add_dl_wiki, add_dl_bible)

add_dl$lang_id <- factor(add_dl$lang_id, levels = lang_order)

add_dl_plot = ggplot(	add_dl, aes(add_dl$link_id, add_dl$npmi_score, colour = add_dl$lang_id)) +
					geom_errorbar(aes(ymin=add_dl$npmi_score-add_dl$error, ymax=add_dl$npmi_score+add_dl$error),width=0.05) +
					facet_grid(add_dl$ref_corpus~.,scale="free") +
					geom_point() +
					xlab("Proportion of Document Links") +
					ylab("CNPMI") +
					geom_smooth() +
					labs(colour='',fill="") +
					scale_x_continuous(breaks=c(0.0,0.2,0.4,0.6,0.8,1.0)) +
  theme(legend.position="top")

ggsave(add_dl_plot, filename = gfxdir("add_dl.pdf"), height=2*dl_height+dl_legend, width=dl_width, scale=dl_scale)



# Adding reference


add_ref_wiki 	= 	read.table(datadir("npmi-adding_reference-Wikipedia.dat"), header = TRUE)
add_ref_bible = 	read.table(datadir("npmi-adding_reference-Bible.dat"), header = TRUE)
add_ref <- rbind(add_ref_wiki, add_ref_bible)
add_ref$Language <- factor(add_ref$Language, levels = lang_order)

add_ref_plot = 	ggplot(	add_ref, aes(add_ref$ref_size, add_ref$npmi_score, colour = Language)) +
					geom_errorbar(aes(ymin=add_ref$npmi_score-add_ref$error, ymax=add_ref$npmi_score+add_ref$error),width=0.05) +
					facet_grid(add_ref$ref_corpus~.,scale="free") +
					geom_point() +
					xlab("Proportion of Reference Corpus") +
					ylab("CNPMI") +
					theme(legend.position = "top") +
    geom_smooth() +
    scale_x_continuous(breaks=c(0.0,0.2,0.4,0.6,0.8,1.0)) +
					labs(colour='',fill="")

ggsave(add_ref_plot, filename = gfxdir("add_ref.pdf"), height=4, width=3, scale=1.2)



### Pearson's correlation
mlc = read.table(datadir("mlc.dat"), header = TRUE)
mlc_plot = 	ggplot(mlc, aes(x=mlc$train, y=mlc$npmi, fill=mlc$corpus)) + 
			geom_bar(position=position_dodge(), stat="identity",
			             size=.3)+
			geom_errorbar(aes(ymin=mlc$npmi-mlc$var, ymax=mlc$npmi+mlc$var),
			                  size=.3,
			                  width=.2,
			                  position=position_dodge(.9)) +
			coord_cartesian(ylim = c(0.85, 1)) +
			facet_grid(mlc$group ~ ., scales = "free") +
			labs(x = "Classification Training Languages", y = "Correlations") +
    guides(fill=guide_legend(title="Reference")) +
    theme(legend.position = "top")  + coord_flip()

ggsave(mlc_plot, filename = gfxdir("mlc.pdf"), height=2, width=3, scale=1.2)


## Model example
example = read.table(datadir("estimator_example.dat"), header = TRUE, sep="\t")
example_plot = 	ggplot(example, aes(x=example$featuregroup, y=example$Coherence.score, color=example$topic, linetype=example$estimation)) + 
				geom_smooth() +
				labs(x = "Feature sets", y = "Coherence scores") + 
				theme(legend.title=element_blank()) +
				scale_x_continuous(labels=c("BASE",
				                          "BASE+GAP",
				                          "BASE+GAP+ERA",
				                          "BASE+GAP+ERA+DRIFT")) +
    scale_y_continuous(position = "right") + 
    theme(legend.position = "none") + geom_smooth() +
    scale_color_manual(values=c("#56BCC2", "#E87D72"))

ggsave(example_plot, filename = gfxdir("estimator_example.pdf"), height=2.25, width=7)

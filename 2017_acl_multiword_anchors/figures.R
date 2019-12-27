library(ggplot2)
library(reshape)
library(scales)

directory <- "2017_acl_multiword_anchors/"

datadir <- function(filename) {
    val <- paste(directory, 'data/', filename, sep='')
    return(val)
}

gfxdir <- function(filename) {
    val <- paste(directory, 'auto_fig/', filename, sep='')
    return(val)
}

make_plot <- function(data) {
    plot <- ggplot(data, aes(variable, value, fill=variable))
    plot = plot + geom_boxplot()
    plot = plot + facet_grid(measure ~ ., scales="free")
    plot = plot + theme(axis.title.x=element_blank(), axis.title.y=element_blank(), legend.position="none", axis.text.x=element_text(angle=270, hjust=0))
    plot = plot + scale_y_reverse()
    return(plot)
}

# Oracle results
oracle_acc <- read.csv(datadir('oracle_accuracy.csv'), sep=',', quote="\"", check.names=FALSE)
oracle_acc["measure"] <- "Accuracy"
oracle_ari <- read.csv(datadir('oracle_ari.csv'), sep=',', quote="\"", check.names=FALSE)
oracle_ari["measure"] <- "ARI"
oracle_f <- read.csv(datadir('oracle_fmeasure.csv'), sep=',', quote="\"", check.names=FALSE)
oracle_f["measure"] <- "F-Measure"
oracle_vi <- read.csv(datadir('oracle_vi.csv'), sep=',', quote="\"", check.names=FALSE)
oracle_vi["measure"] <- "VI"
oracle_coherence <- read.csv(datadir('oracle_coherence.csv'), sep=',', quote="\"", check.names=FALSE)
oracle_coherence["measure"] <- "Coherence"

oracle <- rbind(oracle_acc, oracle_ari, oracle_f, oracle_vi, oracle_coherence)
oracle_melt <- melt(oracle, id=c("measure"))
oracle_melt <- within(oracle_melt, measure <- factor(measure, levels=c('Accuracy', 'ARI', 'F-Measure', 'VI', 'Coherence')))
oracle_plot = make_plot(oracle_melt)
ggsave(oracle_plot, filename=gfxdir("oracle_acc.pdf"), height=7, width=2)

# User results
user_acc <- read.csv(datadir('user_accuracy.csv'), sep=',', quote="\"")
user_acc["measure"] <- "Accuracy"
user_ari <- read.csv(datadir('user_ari.csv'), sep=',', quote="\"")
user_ari["measure"] <- "ARI"
user_f <- read.csv(datadir('user_fmeasure.csv'), sep=',', quote="\"")
user_f["measure"] <- "F-Measure"
user_vi <- read.csv(datadir('user_vi.csv'), sep=',', quote="\"")
user_vi["measure"] <- "VI"
user_coherence <- read.csv(datadir('user_coherence.csv'), sep=',', quote="\"")
user_coherence["measure"] <- "Coherence"

user <- rbind(user_acc, user_ari, user_f, user_vi, user_coherence)
user_melt <- melt(user, id=c("measure"))
user_melt = rbind(user_melt, subset(oracle_melt, variable=='Gram-Schmidt'))
user_melt <- within(user_melt, measure <- factor(measure, levels=c('Accuracy', 'ARI', 'F-Measure', 'VI', 'Coherence')))
user_plot = make_plot(user_melt)
ggsave(user_plot, filename=gfxdir("user_acc.pdf"), height=7, width=1.5)

# Topic Significance Results
uniform <- read.csv(datadir('w_uniform.csv'), sep=',', quote="\"", check.names=FALSE)
uniform["measure"] <- "uniform"
vacuous <- read.csv(datadir('w_vacuous.csv'), sep=',', quote="\"", check.names=FALSE)
vacuous["measure"] <- "vacuous"
bground <- read.csv(datadir('d_bground.csv'), sep=',', quote="\"", check.names=FALSE)
bground["measure"] <- "background"

sig <- rbind(uniform, vacuous, bground)
sig_melt <- melt(sig, id=c("measure"))
sig_melt <- within(sig_melt, measure <- factor(measure, levels=c('uniform', 'vacuous', 'background')))
sig_plot = make_plot(sig_melt)
ggsave(sig_plot, filename=gfxdir("significance.pdf"), height=7, width=1.5)

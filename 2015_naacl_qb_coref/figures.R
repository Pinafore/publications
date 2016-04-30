library(ggplot2)

directory <- "2015_naacl_qb_coref/"

print(getwd())

datadir <- function(filename){
    val <- paste(directory, 'data/', filename, sep='')
    return(val)
}

gfxdir <- function(filename) {
    val <- paste(directory, 'auto_fig/', filename, sep='')
    return(val)
}

palette <- c("#000000", "#CFB87C")

# Load in the data
active_data <- read.csv(datadir('active.csv'))
density_data <- read.csv(datadir('density.csv'))
compare_data <- read.csv(datadir('compare.csv'))

# Active learning comparison
active <- ggplot(active_data, aes(color=Method, y=Precision, x=Iteration)) + geom_smooth() + theme(legend.position="top") + scale_fill_manual(values=palette) + scale_colour_manual(values=palette)

# Density plot
density <- ggplot(density_data, aes(color=Data, size=Data, x=Tokens, y=Count, linetype=Coref)) + geom_line() + theme(legend.position="top") + scale_size_discrete(range = c(0.75, 1.5)) + scale_colour_manual(values=palette)

# Comparing performance
compare <- ggplot(compare_data, aes(x=Formula, y=Score, linetype=Coreference, fill=Coreference)) + facet_grid(Metric ~ Mentions) + geom_bar(stat="identity", position="dodge") + xlab("") + theme(legend.position="top") + scale_fill_manual(values=palette)

ggsave(active, filename = gfxdir("active.pdf"), scale=0.6, height=6, width=8)

ggsave(density, filename = gfxdir("density.pdf"), scale=0.6, height=6, width=8)

ggsave(compare, filename = gfxdir("compare.pdf"), scale=0.6, height=6, width=16)


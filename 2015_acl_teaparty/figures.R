library(ggplot2)
library(reshape)
library(grid)
library(gridExtra)
library(xtable)
library(Rmisc)

directory <- "2015_acl_teaparty/"

print(getwd())

datadir <- function(filename){
    val <- paste(directory, 'data/', filename, sep='')
    return(val)
}

gfxdir <- function(filename) {
    val <- paste(directory, 'auto_fig/', filename, sep='')
    return(val)
}

####################### Boxplot of one-dimensional ideal points #######################
one_dim_112 <- read.csv(datadir('onedim_112.scores'), sep='\t', quote="\"")
one_dim_112_plot <- ggplot(one_dim_112) +
  geom_boxplot(aes(x=TPCaucus, y=Score, fill=TPCaucus, color=TPCaucus)) +
  coord_flip() +
  theme(text = element_text(size=50)) +
  xlab("") +
  ylab("Ideal Point") +
  theme(legend.position="bottom", axis.ticks = element_blank(), axis.text.y = element_blank()) +
  scale_fill_manual("Tea Party Caucus",
                    labels=c("Member", "Non-member"),
                    values=c("chocolate4", "green4")) +
  scale_color_manual("Tea Party Caucus",
                     labels=c("Member", "Non-member"),
                     values=c("black", "black"))
ggsave(one_dim_112_plot, filename = gfxdir("onedim_ip_112.pdf"), height=4, width=16)



############################## Top and bottom legislators ##############################
one_dim_112$Name <- reorder(one_dim_112$Name, one_dim_112$Score)

### Bottom legislators
sorted_one_dim_112 <- one_dim_112[order(one_dim_112$Score),]
bottom <- sorted_one_dim_112[c(1:15),]
bottom$Name <- reorder(bottom$Name, bottom$Score)
bottom_legs <- ggplot(bottom) +
  geom_text(aes(x=Name,y=Score,color=TPCaucus,label=Name), show_guide=FALSE, hjust=-.1, vjust=0.5, size=10) +
  geom_point(aes(x=Name,y=Score,color=TPCaucus,shape=TPCaucus), size=6) +
  coord_flip() +
  xlab("") +
  ylab("Ideal Point") +
  theme(text = element_text(size=30)) +
  theme(legend.position="bottom", axis.ticks = element_blank(), axis.text.y = element_blank()) +
  scale_color_manual("Tea Party Caucus",
                     labels=c("Member", "Non-member"),
                     values=c("orange3", "green4")) +
  scale_shape_manual("Tea Party Caucus",
                     labels=c("Member", "Non-member"),
                     values=c(15, 17)) +
  scale_y_continuous(limits = c(-1.61, -1.2)) +
  theme( # remove the vertical grid lines
    panel.grid.major.y = element_blank() ,
    # explicitly set the horizontal lines (or they will disappear too)
    panel.grid.major.x = element_line( size=.75, color="white" ),
    panel.grid.minor.x = element_line( size=.5, color="white" )
  )
ggsave(bottom_legs, filename = gfxdir("bottom_onedim_ip.pdf"), height=16, width=8)


### Top legislators
sorted_one_dim_112 <- one_dim_112[order(one_dim_112$Score),]
### Remove no names
sorted_one_dim_112$Name <- as.character(sorted_one_dim_112$Name)
sorted_one_dim_112 <- sorted_one_dim_112[complete.cases(sorted_one_dim_112),]

top <- sorted_one_dim_112[c(226:240),]
top$Name <- reorder(top$Name, top$Score)

top_legs <- ggplot(top) +
  geom_text(aes(x=Name,y=Score,color=TPCaucus,label=Name), show_guide=FALSE, hjust=-.1, vjust=0.5, size=10) +
  geom_point(aes(x=Name,y=Score,color=TPCaucus,shape=TPCaucus), size=6) +
  coord_flip() +
  xlab("") +
  ylab("Ideal Point") +
  theme(text = element_text(size=30)) +
  theme(legend.position="bottom", axis.ticks = element_blank(), axis.text.y = element_blank()) +
  scale_color_manual("Tea Party Caucus",
                     labels=c("Member", "Non-member"),
                     values=c("orange3", "green4")) +
  scale_shape_manual("Tea Party Caucus",
                     labels=c("Member", "Non-member"),
                     values=c(15, 17)) +
  scale_y_continuous(limits = c(1.3, 1.95)) +
  theme( # remove the vertical grid lines
    panel.grid.major.y = element_blank() ,
    # explicitly set the horizontal lines (or they will disappear too)
    panel.grid.major.x = element_line( size=.75, color="white" ),
    panel.grid.minor.x = element_line( size=.5, color="white" )
  )
ggsave(top_legs, filename = gfxdir("top_onedim_ip.pdf"), height=16, width=8)


####################### Boxplot of multi-dimensional ideal points #######################
mult_dim_112 <- read.csv(datadir('multdim_112.scores'), sep='\t', quote="\"")
issue_score_112 <- melt(mult_dim_112[,c(1,7, 9:27,29)], id=c('Index', 'TPCaucus', 'Party'))
md_err_112 <- summarySE(issue_score_112, measurevar="value", groupvars=c("TPCaucus", "variable"))
md_err_112_cast <- cast(md_err_112[,c(1,2,4)], variable ~ TPCaucus, mean)
md_err_112_cast$diff <- md_err_112_cast[,2] - md_err_112_cast[,3]
md_err_112_cast$variable <- factor(md_err_112_cast$variable, levels=md_err_112_cast$variable[order(md_err_112_cast$diff)])
issue_score_112$variable <- factor(issue_score_112$variable, levels=levels(md_err_112_cast$variable))

mult_dim_112_plot <- ggplot(issue_score_112, aes(x=variable, y=value, fill=TPCaucus)) +
  geom_boxplot() +
  coord_flip() +
  theme(text = element_text(size=60), axis.text = element_text(colour = "black")) +
  xlab("") +
  ylab("Ideal Points") +
  theme(legend.position="bottom") +
  scale_fill_manual("Tea Party Caucus",
                    labels=c("Member", "Non-member"),
                    values=c("chocolate4", "green4"))
ggsave(mult_dim_112_plot, filename = gfxdir("multdim_ip_112.pdf"), height=16, width=16)


#################################### Summarize errors ####################################
summarySE <- function(data=NULL, measurevar, groupvars=NULL, na.rm=FALSE,
                      conf.interval=.95, .drop=TRUE) {
  require(plyr)

  # New version of length which can handle NA's: if na.rm==T, don't count them
  length2 <- function (x, na.rm=FALSE) {
    if (na.rm) sum(!is.na(x))
    else       length(x)
  }

  # This does the summary. For each group's data frame, return a vector with
  # N, mean, and sd
  datac <- ddply(data, groupvars, .drop=.drop,
                 .fun = function(xx, col) {
                   c(N    = length2(xx[[col]], na.rm=na.rm),
                     mean = mean   (xx[[col]], na.rm=na.rm),
                     sd   = sd     (xx[[col]], na.rm=na.rm),
                     median = median(xx[[col]], na.rm=na.rm)
                   )
                 },
                 measurevar
  )

  # Rename the "mean" column
  datac <- rename(datac, c("mean" = measurevar))

  datac$se <- datac$sd / sqrt(datac$N)  # Calculate standard error of the mean

  # Confidence interval multiplier for standard error
  # Calculate t-statistic for confidence interval:
  # e.g., if conf.interval is .95, use .975 (above/below), and use df=N-1
  ciMult <- qt(conf.interval/2 + .5, datac$N-1)
  datac$ci <- datac$se * ciMult

  return(datac)
}

pd <- position_dodge(1)
fmt2 <- function(x){format(x, nsmall=2, scientific=FALSE)}
fmt3 <- function(x){format(x, nsmall=3, scientific=FALSE)}



#################### Membership prediction using votes and text ####################
tpcaucus <- read.csv(datadir('prediction_results.txt'), sep='\t', quote="\"")
tpcaucus_votetext <- subset(tpcaucus,
                          ((Model=="Hier-Mult-SHDP_all_svm_j-2")
                           | (Model=="vote_Hier-Mult-SHDP_all_svm_j-2")
                           | (Model=="vote_tf_normalized_tfidf_normalized_Hier-Mult-SHDP_all_svm_j-2")
                           | (Model=="vote")
                           | (Model=="tf_normalized")
                           | (Model=="vote_tf_normalized_svm_j-2")
                           | (Model=="tfidf")
                           | (Model=="vote_tfidf_normalized")))

ordermodel <- c("tf_normalized", "tfidf", "vote", "Hier-Mult-SHDP_all_svm_j-2", "vote_tf_normalized_svm_j-2", "vote_tfidf_normalized",
                "vote_Hier-Mult-SHDP_all_svm_j-2", "vote_tf_normalized_tfidf_normalized_Hier-Mult-SHDP_all_svm_j-2")
tpcaucus_votetext$Model <- factor(tpcaucus_votetext$Model, levels=ordermodel)
tpcaucus_votetext_err <- summarySE(tpcaucus_votetext, measurevar="Value", groupvars=c("Model", "Metric"))

votetext <- ggplot(tpcaucus_votetext_err, aes(x=Model, y=as.numeric(Value))) +
  geom_errorbar(aes(ymin=Value-se/2, ymax=Value+se/2), width=0.5) +
  geom_line(aes(shape=Model),size=1.5) +
  geom_point(aes(shape=Model,color=Model), size=8) +
  xlab("") +
  ylab("AUC-ROC") +
  theme(text = element_text(size=50)) +
  theme(legend.position="none") +
  scale_y_continuous(labels=fmt2) +
  ggtitle("") +
  scale_shape_manual("",
                     labels=c("TF", "TF-IDF", "Vote", "HIPTM", "Vote-TF", "Vote-TF-IDF", "Vote-HIPTM", "All"),
                     values=c(15, 15, 15, 15, 15, 15, 15, 17)) +
  scale_color_manual("",
                     labels=c("TF", "TF-IDF", "Vote", "HIPTM", "Vote-TF", "Vote-TF-IDF", "Vote-HIPTM", "All"),
                     values=c("#00FF00", "#00FF00", "black", "#FF0000", "#007F00", "#007F00", "#7F0000", "black")) +
  scale_x_discrete(labels=c("TF", "TF-IDF", "Vote", "HIPTM", "Vote-TF", "Vote-TF-IDF", "Vote-HIPTM", "All"))

votetext <- votetext + coord_flip()

ggsave(votetext, filename = gfxdir("votetext_112.pdf"), scale=.75, height=8, width=18)



#################### Membership prediction using text only ####################
tpcaucus_textonly <- subset(tpcaucus,
                          ((Model=="Hier-Mult-SHDP_svm_j-2")
                           | (Model=="tf_normalized")
                           | (Model=="tfidf")))
ordermodel <- c("tf_normalized", "tfidf", "Hier-Mult-SHDP_svm_j-2")
tpcaucus_textonly$Model <- factor(tpcaucus_textonly$Model, levels=ordermodel)
tpcaucus_textonly_err <- summarySE(tpcaucus_textonly, measurevar="Value", groupvars=c("Model", "Metric"))

textonly <- ggplot(tpcaucus_textonly_err, aes(x=Model, y=as.numeric(Value))) +
  geom_errorbar(aes(ymin=Value-se/2, ymax=Value+se/2), width=0.25) +
  geom_line(aes(shape=Model),size=1.5) +
  geom_point(aes(shape=Model,color=Model), size=8) +
  xlab("") +
  ylab("AUC-ROC") +
  coord_flip() +
  theme(text = element_text(size=50)) +
  theme(legend.position="none") +
  scale_y_continuous(labels=fmt2) +
  ggtitle("") +
  scale_shape_manual("",
                     labels=c("TF", "TF-IDF", "HIPTM"),
                     values=c(15, 15, 15)) +
  scale_x_discrete(labels=c("TF", "TF-IDF", "HIPTM")) +
  scale_color_manual("",
                     labels=c("TF", "TF-IDF", "HIPTM"),
                     values=c("#00FF00", "#00FF00", "#FF0000"))
ggsave(textonly, filename = gfxdir("textonly_112.pdf"), scale=0.75, height=8, width=18)

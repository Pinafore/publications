library(ggplot2)
library(reshape)
library(grid)
library(gridExtra)
library(xtable)
library(Rmisc)
require(ggplot2)

palette2 <- c("#000000", "#CFB87C")
palette3 <- c("#000000", "#FACD00", "#DA1D2B")
palette4 <- c("#FACD00", "#CFB87C", "#b2df8a", "#33a02c")

directory <- "2016_acl_doclabel/"

print(getwd())

datadir <- function(filename){
    val <- paste(directory, 'data/', filename, sep='')
    #print(val)
    return(val)
}

gfxdir <- function(filename) {
    val <- paste(directory, 'auto_fig/', filename, sep='')
    return(val)
}

####################### Plot for user experiments #######################
all_data <- read.csv(datadir('user_exp/plot_data.csv'), sep=',', quote="\"")
condition_time_data <- melt(all_data, id.vars=c("participant","condition","time"), variable_name = "metric")

c1 <- c("time", "metric", "condition")
v1 <- c("value")
median_data <- aggregate(condition_time_data[v1],by=condition_time_data[c1],FUN=median)
pd <- position_dodge(0.1)
#find sd, std, and CI
congress_user <- summarySE(condition_time_data, measurevar="value", groupvars=c("condition","metric","time"))
#add the median data
congress_user["median_value"] <- median_data$value
#data_stats
user_exp_plot <- ggplot(data=congress_user, aes(x=time, y=median_value, group=condition, colour=condition)) +
    geom_errorbar(aes(ymin=median_value-se, ymax=median_value+se), width=1, position=pd) +
    geom_line(size=1, position=pd) +
    geom_point(size=2, aes(shape = condition), position=pd)+
     facet_grid(metric ~ ., scale="free")+
     xlab("Elapsed Time (min)") +
    ylab("Median (over participants)") +
     theme(legend.position="top")
ggsave(user_exp_plot, filename = gfxdir("user_exp_plot.pdf"), height=4, width=4)


###################### Plots for synthetic experiments #######################
#newsgroups
all_data <- read.csv(datadir('synthetic_exp/newsgroups_syn_data.csv'), sep=',', quote="\"")
condition_num_data <- melt(all_data, id.vars=c("iteration","condition","num_docs"), variable_name = "metric")

c1 <- c("num_docs","metric","condition")
v1 <- c("value")
median_data <- aggregate(condition_num_data[v1],by=condition_num_data[c1],FUN=median)
pd <- position_dodge(0.1)
#find sd, std, and CI
ng_synth <- summarySE(condition_num_data, measurevar="value", groupvars=c("condition","metric","num_docs"))
ng_synth["median_value"] <- median_data$value

#congress
all_data <- read.csv(datadir('synthetic_exp/congress_syn_data.csv'), sep=',', quote="\"")
condition_num_data <- melt(all_data, id.vars=c("iteration","condition","num_docs"), variable_name = "metric")

c1 <- c("num_docs","metric","condition")
v1 <- c("value")
median_data <- aggregate(condition_num_data[v1],by=condition_num_data[c1],FUN=median)

pd <- position_dodge(0.1)
#find sd, std, and CI
congress_synth <- summarySE(condition_num_data, measurevar="value", groupvars=c("condition","metric","num_docs"))
#data_stats
congress_synth["median_value"] <- median_data$value

# Combine labeling experiments into one graph
ng_synth["exper"] <- "Newsgroups (Synth)"
congress_synth["exper"] <- "Congress (Synth)"

combined_results <- rbind(ng_synth, congress_synth)
combined_results <- combined_results[combined_results$num_docs >= 10, ]
#combined_results
combined <- ggplot(subset(combined_results,num_docs %in% c("2","10","20","30","40","50","60","70","80","90","100")), aes(x=num_docs, y=median_value, group=condition, colour=condition)) +
  geom_line(size=1, position=pd)+

 geom_errorbar(aes(ymin=median_value-se, ymax=median_value+se), width=.1, position=pd) +

  geom_point(size=2, aes(shape = condition), position=pd)+

  facet_grid(metric ~ exper, scales="free_y")+
  xlab("Documents Labeled") +
  ylab("Median (over 15 runs)") +
  theme(legend.position="top")

ggsave(combined, filename = gfxdir("synthetic.pdf"), height=4, width=4)

# ####################### Plots for bootstrapped label evaluation data #######################
vote_data <- read.csv(datadir('label_eval/sampled_votes.csv'), sep=',', quote="\"")
condition_vote_data <- melt(vote_data, id.vars=c("iteration","condition"), variable_name = "best_worst")
mean_vote_data <- summarySE(condition_vote_data, measurevar="value", groupvars=c("condition","best_worst"))
#mean_vote_data
eval_votes_plot <- ggplot(data=mean_vote_data, aes(condition, y=value, fill=best_worst)) +
             geom_bar(position=position_dodge(), stat="identity", colour='black')+
             scale_fill_manual(values=c("springgreen3", "orangered2"))+
            geom_errorbar(aes(ymin=value-se, ymax=value+se), width=.2,position=position_dodge(.9))+
            theme(legend.position="top", legend.title=element_blank())+
            ylab("Number of Votes (mean)") +
        xlab("Condition") + scale_fill_manual(values=palette2) + scale_colour_manual(values=palette2)

ggsave(eval_votes_plot, filename = gfxdir("eval_votes.pdf"), height=2.5, width=4)
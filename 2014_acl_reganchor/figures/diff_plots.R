
library(ggplot2)
library(GGally)

parallel_plot <- function(top, bottom, old_col, new_col, word_label, topic_group) {
  whole <- rbind(top, bottom)
  
  p <- ggparcoord(data=whole, columns=c(old_col,new_col), scale="globalminmax", groupColumn=topic_group)
    
  anchors = levels(whole[,topic_group])
    
  for(i in 1:nrow(whole)) {
    row <- whole[i,]
    color = which(anchors == row$anchor)
    yval_old <- as.numeric(row[old_col])
    yval_new <- as.numeric(row[new_col])
    p <- p + geom_text(data= NULL, x = 0.9, y = yval_old, label=row$word, colour="black")
    p <- p + geom_text(data= NULL, x = 2.1, y = yval_new, label=row$word, colour="black")
  }
  
  return(p)
}

orig <- read.table("orig.txt")
beta <- read.table("beta.txt")

beta <- data.frame(score = beta$V3,
                   type = "beta",
                   anchor = beta$V1,
                   word = beta$V2,
                   key = sprintf("%s_%s", beta$V1, beta$V2))

beta$rank <- ave(beta$score, beta$anchor, FUN=rank)
beta$rank <- max(beta$rank) - beta$rank

orig <- data.frame(score = orig$V3,
                   type = "orig",
                   anchor = orig$V1,
                   word = orig$V2,
                   key = sprintf("%s_%s", orig$V1, orig$V2))

orig$rank <- ave(orig$score, orig$anchor, FUN=rank)
orig$rank <- max(orig$rank) - orig$rank

words <- rbind(orig, beta)
diffs <- merge(orig, beta, by="key")

diffs$word <- diffs$word.x
diffs$anchor <- diffs$anchor.x
diffs$rank <- diffs$rank.x - diffs$rank.y
diffs$orig_rank <- diffs$rank.x
diffs$beta_rank <- diffs$rank.y
diffs$orig_score <- diffs$score.x
diffs$beta_score <- diffs$score.y
diffs$score <- diffs$score.x - diffs$score.y

density_plot <- ggplot(words, aes(rank, log(score)), scales="free") + geom_line() + facet_grid(type ~ anchor) + ylim(c(-25, 0)) + ylab("p(word|topic)") + xlab("Rank of word in topic") + scale_x_continuous(labels = c())

diff_rank <- diffs[order(diffs$rank),]
diff_score <- diffs[order(diffs$score),]

num_words <- 15
top_diff_rank <- diff_rank[1:num_words,]
bottom_diff_rank <- diff_rank[(dim(diff_rank)[1]-num_words):dim(diff_rank)[1],]

top_diff_score <- diff_score[1:num_words,]
bottom_diff_score <- diff_score[(dim(diff_score)[1]-num_words):dim(diff_score)[1],]


rank_diff <- parallel_plot(top_diff_rank, bottom_diff_rank,  which(colnames(top_diff_rank)=="orig_rank"), which(colnames(top_diff_rank)=="beta_rank"),  which(colnames(top_diff_rank)=="word"), which(colnames(top_diff_rank)=="anchor"))
score_diff <- parallel_plot(top_diff_score, bottom_diff_score,  which(colnames(top_diff_score)=="orig_score"), which(colnames(top_diff_score)=="beta_score"),  which(colnames(top_diff_score)=="word"), which(colnames(top_diff_score)=="anchor"))



require(ggplot2)
library(ggplot2)
d <- data.frame(layers = c(0, 1, 2, 3, 4, 5, 6),
                acc_root = c(82.5, 84.7, 85.7, 85.5, 85.5, 85.6, 85.4),
                acc_all = c(83.6, 85.7, 86.4, 86.8, 85.5, 85.6, 85.8))
p1 <- ggplot(d, aes(x=layers, y=value, color=a)) + 
	geom_point(aes(y=acc_root,color="DAN-ROOT"), size=4) + 
	geom_line(aes(y=acc_root,color="DAN-ROOT")) + 
	geom_point(aes(y=acc_all,color="DAN"), size=4) +
	geom_line(aes(y=acc_all,color="DAN")) + theme_minimal() +
	labs( x="Number of Layers", y="Binary Classification Accuracy") +
	theme(legend.title = element_blank(),
		legend.position = c(0.8, 0.2)) + 
	ggtitle('Effect of Depth on Sentiment Accuracy')
ggsave(p1, file="/home/mohit/pinafore-papers/2015_acl_dan/figures/layers.pdf", width=5, height=3)

p1
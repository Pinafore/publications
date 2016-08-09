require(ggplot2)
library(ggplot2)
d <- data.frame(layers = c(0, 1, 2, 3, 4, 5),
                acc_worst = c(13.5, 7.2, 9.3, 14.4, 26.0, 52.6),
                acc_under = c(11.1, 6.8, 8.8, 13.6, 24.4, 49.7),
                acc_okay = c(13.5, 3.8, 3.6, 5.8, 10.6, 19.8),
                acc_cool = c(12.3, 3.3, 1.9, 1.9, 3.0, 5.3))
p1 <- ggplot(d, aes(x=layers, y=value, color=a)) + 
	geom_line(aes(y=acc_worst,color="the worst")) + 
	geom_line(aes(y=acc_under,color="underwhelming ")) + 
	geom_line(aes(y=acc_okay,color="okay")) + 
	geom_line(aes(y=acc_cool,color="cool")) + theme_minimal() + 
	labs( x="Layer", y="Perturbation Response") +
	theme(legend.title = element_blank(), 
		legend.position = c(0.25, 0.7)) + 
	ggtitle('Perturbation Response vs. Layer') 
ggsave(p1, file="/home/mohit/pinafore-papers/2015_acl_dan/figures/perturb_2.pdf", width=5, height=4)

p1
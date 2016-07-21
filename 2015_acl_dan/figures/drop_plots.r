require(ggplot2)
library(ggplot2)
d <- data.frame(drop = c(0, 0.1, 0.2, 0.3, 0.4, 0.5),
                acc = c(68.7, 69.5, 70.9, 71.6, 70.2, 71.2))
p1 <- ggplot(d, aes(x=drop, y=acc)) + 
  geom_line() + geom_point() + scale_colour_hue() + 
  labs( x="Dropout Probability", y="History QB Accuracy") +
  ggtitle('Effect of Word Dropout') + theme_minimal()
ggsave(p1, file="/home/mohit/pinafore-papers/2015_acl_dan/figures/dropout_effect.pdf", width=5, height=2.5)
p1
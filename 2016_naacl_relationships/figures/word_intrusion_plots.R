require("ggplot2")
require("scales")

theme = theme_set(theme_grey())
box = read.table("/home/mohit/Research/deep_reader/models/cr_intrusion_precision_box.csv", 
                   header=TRUE, sep=",", na.strings="NA", dec=".", strip.white=TRUE)

box$model = factor(box$model, levels=c("LDA", "Nubbi", "HTMM", "GRMN", "RMN"))

mycol = c("dodgerblue2", "darkolivegreen4","darkorchid3", "lightpink2", "darkgoldenrod")
col = scale_fill_manual(values=mycol)

fbox = ggplot(data = box, aes(x = model, y = precision, fill=model) ) + geom_boxplot() + col
fbox = fbox + labs(y="Model Precision") #title="Comparing Model Precision from Word Intrusion"
#fbox = fbox + scale_x_discrete(labels=c("lda" = "LDA", "nubbi" = "Nubbi", "htmm" = "HTMM", "rmn"="RMN"))
#fbox = fbox + theme(axis.title.x=element_blank(),legend.position="none")
fbox = fbox + theme(axis.title.x=element_blank()) + theme(legend.text=element_text(size=14))
fbox = fbox + theme(legend.title=element_blank(),legend.position="bottom",legend.direction="horizontal")
fbox = fbox + theme(axis.title = element_text(color="black", size=18)) 
fbox = fbox + theme(title = element_text(color="black", size=18)) 
#fbox = fbox + theme(axis.text.x = element_text(size=18,color=mycol))
fbox = fbox + theme(axis.text.x = element_blank()) + theme(axis.ticks.x=element_blank())
fbox = fbox + theme(axis.text.y = element_text(size=12))
fbox = fbox + facet_wrap(~K) + theme(strip.text.x = element_text(size = 12))
print(fbox)
ggsave(fbox, file="/home/mohit/pinafore-papers/2016_naacl_relationships/figures/topic_intrusion.pdf", scale=1,width=6, height=3.5)


# precs = read.table("/home/mohit/Fall_2015/books/models/intrusion_precision.csv", 
#                    header=TRUE, sep=",", na.strings="NA", dec=".", strip.white=TRUE)
# precs$model = factor(precs$model, levels=c("lda", "nubbi", "htmm", "rmn"))
# f1 = ggplot(data = precs, aes(x = model, y = precision) ) + 
#   geom_errorbar(aes(ymin = precision - std, ymax = precision + std), width=0.3) + 
#   geom_point(aes(color=model,fill=model), size=5) +
#   labs(title="Model Precision from Word Intrusion Experiments")
# print(f1)
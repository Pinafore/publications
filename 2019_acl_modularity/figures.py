from plotnine import *
import pandas as pd

kROOT_DIR = "2019_acl_modularity"

def datadir(filename):
    return "%s/data/%s" % (kROOT_DIR, filename)

def gfxdir(filename):
    return "%s/auto_fig/%s" % (kROOT_DIR, filename)


def plot_ablation():
    actual = "Actual Classification Accuracy"
    predicted = "Predicted Accuracy"
    lang = "lang"
    dim = "factor(dim)"
    
    df = pd.read_csv(datadir("ablation_study.csv"))
    g = ggplot(df, aes(x=actual, y=predicted, shape=lang, color=dim)) \
        + geom_point(size=4) + geom_abline(intercept=0, slope=1) \
        + xlim(0.0, 1.0) + ylim(0.0, 1.0) \
        + theme(text=element_text(size=14)) \
        + guides(color=guide_legend(title="dim")) \
        + facet_wrap("~label", ncol=2)
    
    g = g + geom_text(aes(x=0.25, y = 0.9, label="r_sq"), color="black", size=14, stat="unique")
    
    g.save(filename=gfxdir("ablation_study.pdf"), format="pdf", height = 5, width = 7)

def plot_hyperparam_k():
    df = pd.read_csv(datadir("k_nn_hyperparam.csv"))
    g = ggplot(df, aes(x="k", y="Absolute Correlation", group="Correlation Type")) \
        + geom_line(aes(linetype="Correlation Type", color="Correlation Type")) \
        + geom_point(aes(shape="Correlation Type", color="Correlation Type"), size=4) \
        + labs(title="") \
        + theme(legend_position="top") \
        + theme(legend_title=element_text(text="")) \
        + theme(legend_entry_spacing=10) \
        + theme(text=element_text(size=16))
#        + guides(color=guide_legend(title="")) \
#        + theme(legend_position=(0.7, 0.7)) \
# \
#        + theme(legend.position=(200, 0.95))
    g.save(filename=gfxdir("k_nn_diff_k_corr.pdf"), format="pdf", height = 5, width = 7)

def plot_bli_corr():
    columns = ["Precision@1", "Modularity", "Dim", "Lang"]
    df = pd.read_csv(datadir("corr_bli.csv"))
    df["Dim"] = df["Dim"].astype(str)
    
    g = ggplot(df, aes(x=columns[0], y=columns[1])) \
        + geom_point(aes(shape=columns[3], color=columns[2]), size=3) \
        + ylim(0.35, 0.7) \
        + geom_smooth(method = 'lm', se=False) \
        + theme(text=element_text(size=18))
    g.save(filename=gfxdir("corr_bli.pdf"), format="pdf")

def plot_cldc_corr():
    columns = ["Classification Accuracy", "Modularity", "Dim", "Lang"]
    df = pd.read_csv(datadir("corr_cldc.csv"))
    df["Dim"] = df["Dim"].astype(str)
    
    g = ggplot(df, aes(x=columns[0], y=columns[1])) \
        + geom_point(aes(shape=columns[3], color=columns[2]), size=3) \
        + ylim(0.35, 0.7) \
        + geom_smooth(method = 'lm', se=False) \
        + theme(text=element_text(size=18))
    g.save(filename=gfxdir("corr_cldc.pdf"), format="pdf")

def plot_tsne():
    actual = "dim0"
    predicted = "dim1"
    
    df = pd.read_csv(datadir("en_jp_w2v_snippet.csv"))
    g = ggplot(df, aes(x=actual, y=predicted, fill="lang", label="word")) \
        + geom_point(size=5, show_legend=False) \
        + geom_text(size=14, position = position_nudge(y = 0.085, x = 0.03), show_legend=False, color="black") \
        + theme(text=element_text(size=14, family="Arial Unicode MS"), \
            axis_title_x=element_blank(), axis_title_y=element_blank()) \
        + xlim(-1.01, 1.0) \
        + scale_fill_manual(values=("#FFFFFF", "#FFA07A"))
    
    g.save(filename=gfxdir("en_jp_w2v_snippet.pdf"), format="pdf", height = 5, width = 7)


plot_ablation()
plot_hyperparam_k()
plot_bli_corr()
plot_cldc_corr()
plot_tsne()

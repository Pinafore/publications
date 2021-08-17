import datetime
import enum
import functools
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Type, TypeVar, Union

import altair as alt
import altair_saver
import krippendorff
import numpy as np
import pandas as pd
import pydantic
import toml
import typer
import unidecode
from altair.expr import datum
from pdf_annotate import Appearance, Location, PdfAnnotator
from pedroai.io import (
    read_json,
    read_jsonlines,
    requires_file,
    requires_files,
    safe_file,
)
from pedroai.math import to_precision
from pydantic import BaseModel
from rich.console import Console
from scipy import stats
from sklearn import metrics

alt.data_transformers.disable_max_rows()

console = Console()

with open("2021_acl_leaderboard/config.toml") as f:
    conf = toml.load(f)

# DO NOT change this code, to make changes, change it
# in isicle/data.py, then copy to here
# BEGIN: isicle/data.py
Json = Dict[str, Any]


def extract_sentences(question: Json) -> List[Json]:
    sentences = []
    qanta_id = question["qanta_id"]
    sentence_tokenizations = question["tokenizations"]
    for idx, (start, end) in enumerate(sentence_tokenizations):
        text = question["text"][start:end]
        sentences.append(
            {
                "text": text,
                "start": start,
                "end": end,
                "qanta_id": qanta_id,
                "sentence_idx": idx,
            }
        )
    return sentences


class Submission(BaseModel):
    name: str
    bundle_id: str
    submit_id: str
    public: bool
    state: str
    submitter: str
    scores: Dict[str, float]
    created: datetime.datetime


class LeaderboardSubmissions(BaseModel):
    submissions: List[Submission]


PredictionScores = Dict[str, float]


class LeaderboardPredictions(BaseModel):
    scored_predictions: Dict[str, Dict[str, PredictionScores]]
    model_scores: Dict[str, Dict[str, float]]


class SquadV2Answer(BaseModel):
    text: str
    answer_start: int


class SquadV2Question(BaseModel):
    question: str
    id: str
    answers: List[SquadV2Answer]
    is_impossible: bool


class SquadV2Paragraph(BaseModel):
    context: str
    qas: List[SquadV2Question]


class SquadV2Page(BaseModel):
    title: str
    paragraphs: List[SquadV2Paragraph]


class SquadV2(BaseModel):
    version: str
    data: List[SquadV2Page]


def load_squad_v2(file: str) -> SquadV2:
    return SquadV2.parse_obj(read_json(file))


class IrtModelType(enum.Enum):
    pyro_1pl = "pyro_1pl"
    stan_1pl = "stan_1pl"
    pyro_2pl = "pyro_2pl"
    stan_2pl = "stan_2pl"
    pyro_3pl = "pyro_3pl"
    multidim_2pl = "multidim_2pl"


class IrtResults(BaseModel):
    irt_model: str
    ability: Optional[List[float]]
    disc: Optional[List[float]]
    diff: Optional[List[float]]
    lambdas: Optional[List[float]]
    example_ids: Optional[Dict[str, str]]
    model_ids: Optional[Dict[str, str]]


T = TypeVar("T", bound="IrtParsed")


class ExampleStats(BaseModel):
    irt_model: str
    example_id: str
    diff: float
    disc: Optional[float]
    lambda_: Optional[float]


class ModelStats(BaseModel):
    irt_model: str
    model_id: str
    skill: float


def compute_item_accuracy(predictions: LeaderboardPredictions) -> Dict[str, float]:
    accuracies = defaultdict(int)
    n_models = 0
    for model_scores in predictions.scored_predictions.values():
        for item_id, score in model_scores["exact_match"].items():
            accuracies[item_id] += score
        n_models += 1

    for item_id in accuracies:
        accuracies[item_id] = accuracies[item_id] / n_models
    return dict(accuracies)


def load_squad_submissions(predictions: LeaderboardPredictions):
    dev_scores = predictions.model_scores
    id_to_sub = {}
    out = read_json(conf["squad"]["out_v2"])
    for row in out["leaderboard"]:
        if row["submission"]["public"] and row["bundle"]["state"] == "ready":
            submit_info = json.loads(row["bundle"]["metadata"]["description"])
            submit_id = submit_info["submit_id"]
            test_id = submit_info["predict_id"]
            name = row["submission"]["description"]
            id_to_sub[submit_id] = {
                "dev_id": submit_id,
                "test_id": test_id,
                "name": name,
                "test_em": row["scores"]["exact_match"],
                "test_f1": row["scores"]["f1"],
                "dev_em": dev_scores[submit_id]["exact_match"],
                "dev_f1": dev_scores[submit_id]["f1"],
                "created": row["submission"]["created"],
            }
    return id_to_sub


def str_idx_to_int(str_idx: str, irt_model_type: IrtModelType) -> int:
    """STAN indexing is one based, so convert to zero based, or keep the same for pyro

    Args:
        str_idx (str): string numerical index
        irt_model_type (IrtModelType): pyro vs stan

    Raises:
        ValueError: Only allow certain models

    Returns:
        int: fixed index
    """
    if irt_model_type == IrtModelType.stan_2pl:
        idx = int(str_idx) - 1
    elif (
        irt_model_type == IrtModelType.pyro_2pl
        or irt_model_type == IrtModelType.pyro_3pl
        or irt_model_type == IrtModelType.pyro_1pl
    ):
        idx = int(str_idx)
    else:
        raise ValueError(f"Invalid model type: {irt_model_type}")
    return idx


def squad_pred_scores_to_jsonlines(fold: str, metric: str = "exact_match"):
    predictions = LeaderboardPredictions.parse_file(
        conf["squad"]["submission_predictions"][fold]
    )
    output = []
    for subject_id, scores in predictions.scored_predictions.items():
        subject_predictions = {}
        for item_id, value in scores[metric].items():
            subject_predictions[item_id] = {
                "scores": {"exact_match": value},
                "example_id": item_id,
                "submission_id": subject_id,
            }
        # Recover the name after the fact when linking back to test data
        output.append(
            {
                "submission_id": subject_id,
                "predictions": subject_predictions,
                "name": None,
            }
        )
    return output


class IrtParsed(BaseModel):
    model_stats: Dict[str, ModelStats]
    example_stats: Dict[str, ExampleStats]
    example_ids: List[str]
    model_ids: List[str]
    irt_model: IrtModelType

    @classmethod
    def from_irt_file(cls: Type[T], file: str) -> T:
        irt_results = IrtResults.parse_file(file)
        return cls.from_irt_results(irt_results)

    @classmethod
    def from_multidim_1d_file(cls: Type[T], subject_file: str, item_file: str):
        items = read_jsonlines(item_file)
        item_stats = {}
        all_item_ids = []
        irt_model = "multidim_2pl"
        for it in items:
            item_id = it["submission_id"]
            dim = len(it["item_feat_mu"])
            if dim != 2:
                raise ValueError(f"Invalid dimensions: {dim}")
            disc = it["item_feat_mu"][0]
            diff = it["item_feat_mu"][1]
            item_stats[item_id] = ExampleStats(
                example_id=item_id, diff=diff, irt_model=irt_model, disc=disc
            )
            all_item_ids.append(item_id)

        subjects = read_jsonlines(subject_file)
        subject_stats = {}
        all_subject_ids = []
        for subj in subjects:
            subject_id = subj["submission_id"]
            dim = len(subj["ability_mu"])
            if dim != 1:
                raise ValueError(f"Invalid dimensions: {dim}")
            ability = subj["ability_mu"][0]
            subject_stats[subject_id] = ModelStats(
                model_id=subject_id, skill=ability, irt_model=irt_model
            )
            all_subject_ids.append(subject_id)
        return cls(
            irt_model=IrtModelType(irt_model),
            example_stats=item_stats,
            example_ids=all_item_ids,
            model_stats=subject_stats,
            model_ids=all_subject_ids,
        )

    @classmethod
    def from_irt_results(cls: Type[T], irt_results: IrtResults) -> T:
        example_ids = set()
        irt_2pl_example_stats = {}
        for str_idx, ex_id in irt_results.example_ids.items():
            idx = str_idx_to_int(str_idx, IrtModelType(irt_results.irt_model))
            n_examples = len(irt_results.example_ids)
            if idx < 0 or idx > n_examples - 1:
                raise ValueError(f"Invalid index: {idx}, n_examples={n_examples}")

            example_ids.add(ex_id)
            irt_2pl_example_stats[ex_id] = ExampleStats(
                irt_model=irt_results.irt_model,
                example_id=ex_id,
                diff=irt_results.diff[idx],
                disc=irt_results.disc[idx] if irt_results.disc is not None else None,
                lambda_=irt_results.lambdas[idx]
                if irt_results.lambdas is not None
                else None,
            )

        model_ids = set()
        irt_2pl_model_stats = {}
        n_models = len(irt_results.model_ids)
        for str_idx, m_id in irt_results.model_ids.items():
            idx = str_idx_to_int(str_idx, IrtModelType(irt_results.irt_model))

            if idx < 0 or idx > n_models - 1:
                all_ids = [int(str_idx) for str_idx in irt_results.model_ids.keys()]
                max_id = max(all_ids)
                min_id = min(all_ids)
                raise ValueError(
                    f"Invalid index: {idx} model_type={irt_results.irt_model} n_models={n_models} min_id={min_id} max_id={max_id}"
                )
            model_ids.add(m_id)
            irt_2pl_model_stats[m_id] = ModelStats(
                irt_model=irt_results.irt_model,
                model_id=m_id,
                skill=irt_results.ability[idx],
            )

        return cls(
            irt_model=IrtModelType(irt_results.irt_model),
            example_stats=irt_2pl_example_stats,
            example_ids=list(example_ids),
            model_stats=irt_2pl_model_stats,
            model_ids=list(model_ids),
        )


# END: isicle/data.py

PAPER_PATH = Path("2021_acl_leaderboard")
FIGURE_PATH = PAPER_PATH / "auto_fig/"
COMMIT_PATH = PAPER_PATH / "commit_auto_figs/"
DATA_PATH = PAPER_PATH / "auto_data"
BASE_SIZE = 150


def save_chart(chart: alt.Chart, base_path: Union[Path, str], filetypes: List[str]):
    base_path = str(base_path)
    for t in filetypes:
        path = base_path + "." + t
        if t in ("svg", "pdf"):
            method = "node"
        else:
            method = None
        altair_saver.save(chart, safe_file(path), method=method)


PLOTS = {}


def register_plot(name: str):
    def decorator(func):
        PLOTS[name] = func
        return func

    return decorator


def prob(*, theta: float, beta: float, gamma: float, c: float, lambda_: float):
    return c + (lambda_ - c) / (1 + np.exp(-gamma * (theta - beta)))


def d_prob(*, theta: float, beta: float, gamma: float, c: float, lambda_: float):
    return (
        gamma
        * (lambda_ - c)
        * np.exp(-gamma * (theta - beta))
        / (np.exp(-gamma * (theta - beta)) + 1) ** 2
    )


@register_plot("3pl")
def plot_3pl(filetypes: List[str], commit: bool = False):
    theta = np.linspace(-4, 4, num=100)
    beta = 0
    gamma = 1
    lambda_ = 0.95
    c = 0.0
    p = prob(theta=theta, beta=beta, gamma=gamma, c=c, lambda_=lambda_)
    df = pd.DataFrame({"theta": theta, "p": p})
    df["disc"] = f"γ = {gamma}"

    gamma_2_df = pd.DataFrame(
        {
            "theta": theta,
            "p": prob(theta=theta, beta=beta, gamma=2, c=c, lambda_=lambda_),
        }
    )
    gamma_2_df["disc"] = "γ = 2"

    gamma_05_df = pd.DataFrame(
        {
            "theta": theta,
            "p": prob(theta=theta, beta=beta, gamma=0.5, c=c, lambda_=lambda_),
        }
    )
    gamma_05_df["disc"] = "γ = 0.5"
    df = pd.concat([df, gamma_2_df, gamma_05_df])

    # alt.renderers.enable("mimetype")
    # alt.renderers.enable('altair_viewer')
    slope = d_prob(theta=0, beta=beta, gamma=gamma, c=c, lambda_=lambda_)
    intercept = prob(theta=0, beta=beta, gamma=gamma, c=c, lambda_=lambda_)
    x = -1.5
    x2 = 1.5
    y = slope * x + intercept
    y2 = slope * x2 + intercept
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x="theta", y="p", color=alt.Color("disc:N", title="Discriminability (γ)")
        )
    )
    segments = []
    segments.append({"x": x, "x2": x2, "y": y, "y2": y2, "linetype": "solid"})
    segments.append({"x": 0, "x2": 0, "y": 0, "y2": intercept, "linetype": "dotted"})
    segments.append(
        {"x": -4, "x2": 0, "y": intercept, "y2": intercept, "linetype": "dotted"}
    )
    # segments.append({"x": -4, "x2": -2.5, "y": c, "y2": c, "linetype": "dotted"})
    segments.append(
        {"x": -4, "x2": 4, "y": lambda_, "y2": lambda_, "linetype": "dotted"}
    )
    seg_df = pd.DataFrame(segments)
    chart += (
        alt.Chart(seg_df)
        .mark_rule()
        .encode(
            x=alt.X("x", title="Skill (θ)"),
            x2="x2",
            y=alt.Y("y", title="P(response = correct | θ)"),
            y2="y2",
            strokeDash=alt.StrokeDash(
                "linetype", legend=None, scale=alt.Scale(domain=["solid", "dotted"]),
            ),
        )
    )
    text_df = pd.DataFrame(
        [
            {"x": 1.0, "y": 0.1, "text": "Difficulty β=0.0"},
            # {"x": -2.5, "y": 0.2, "text": "Random Correct c=0.25"},
            {"x": -3, "y": 0.91, "text": "Feasibility λ=.95"},
        ]
    )
    chart += (
        alt.Chart(text_df)
        .mark_text()
        .encode(x="x", y="y", text="text")
        .properties(title="Item Characteristic Curve")
    )
    chart = chart.configure_legend(orient="top")
    if commit:
        save_chart(chart, COMMIT_PATH / "3pl", filetypes)
    else:
        save_chart(chart, FIGURE_PATH / "3pl", filetypes)


@register_plot("thought")
def plot_thought(filetypes: List[str], commit: bool = False):
    dist_1 = stats.cauchy(loc=0, scale=2)
    dist_2 = stats.norm(loc=10, scale=1.5)
    x = np.linspace(-4, 20, num=100)
    y = dist_1.pdf(x) + 0.2 * dist_2.pdf(x)
    df = pd.DataFrame({"x": x, "y": y})
    chart = (
        (
            alt.Chart(df)
            .mark_line()
            .encode(
                x=alt.X("x", title="Difficulty (β)"),
                y=alt.Y("y", title="Density", scale=alt.Scale(domain=[0, 0.2])),
            )
        )
        .configure_axis(labelFontSize=11, titleFontSize=11)
        .properties(width=150, height=50)
    )
    if commit:
        save_chart(chart, COMMIT_PATH / "thought", filetypes)
    else:
        save_chart(chart, FIGURE_PATH / "thought", filetypes)


TESTS = ["sem", "mcnemar", "wilcoxon", "student_t", "see"]
TEST_FILES = [
    PAPER_PATH
    / "auto_data"
    / "data"
    / "stats"
    / "sampling=random"
    / "percent=100"
    / f"{test}.json"
    for test in TESTS
]
TEST_NAMES = {
    "see": "IRT Standard Error of Estimation",
    "sem": "Standard Error of Mean",
    "mcnemar": "McNemar",
    "student_t": "Student T",
    "wilcoxon": "Wilcoxon",
}


def pretty_name(test):
    return TEST_NAMES[test]


@register_plot("compare")
@requires_files(TEST_FILES)
def plot_stat_tests(filetypes: List[str], commit: bool = False):
    rows = []
    for path in TEST_FILES:
        tests = read_json(path)["results"]
        rows.extend(tests)
    df = pd.DataFrame(rows)
    lookup = {}
    for r in df[df.test == "see"].itertuples():
        lookup[(r.model_a, r.model_b)] = r.pvalue

    df["test_name"] = df["test"].map(pretty_name)
    df["see_pvalue"] = df.apply(lambda x: lookup[(x.model_a, x.model_b)], axis=1)
    df["diff_pvalue"] = df["pvalue"] - df["see_pvalue"]
    df["model_a_skill"] = df["metadata"].map(
        lambda r: None if pd.isna(r) else r["model_a_skill"]
    )
    df["model_b_skill"] = df["metadata"].map(
        lambda r: None if pd.isna(r) else r["model_b_skill"]
    )
    df["sig_alpha_.05"] = df["pvalue"] < 0.05
    df["sig_alpha_.01"] = df["pvalue"] < 0.01
    max_diff = 0.03
    min_diff = 0.001
    sample = df[(df["diff"] < max_diff) & (df["diff"] > min_diff)].sample(5000)
    base = (
        alt.Chart(sample)
        .transform_joinaggregate(total="count(*)")
        .transform_calculate(pct="1 / datum.total")
    )
    cols = alt.hconcat()
    base_hist_count = (
        base.mark_area(interpolate="step")
        .encode(
            x=alt.X("pvalue", title="P Value", bin=alt.Bin(maxbins=50)),
            y=alt.Y(
                "count()",
                title="Density",
                scale=alt.Scale(type="log"),
                axis=alt.Axis(orient="left"),
            ),
        )
        .properties(height=100, width=200)
    )
    base_hist_pct = (
        base.mark_area(interpolate="step")
        .encode(
            x=alt.X("pvalue", title="P Value", bin=alt.Bin(maxbins=50)),
            y=alt.Y(
                "sum(pct):Q",
                title="",
                scale=alt.Scale(type="log"),
                axis=alt.Axis(orient="right", format="%"),
            ),
        )
        .properties(height=100, width=200)
    )
    base_hist = alt.layer(base_hist_count, base_hist_pct).resolve_scale(y="independent")

    base_scatter = base.mark_point().encode(
        x=alt.X("pvalue", title="P Value", axis=alt.Axis(orient="bottom")),
        y=alt.Y(
            "diff",
            title="Score Difference",
            scale=alt.Scale(type="log", domain=(min_diff, max_diff)),
        ),
        color=alt.Color(
            "diff_pvalue",
            title="Test P Value - IRT SEE P Value",
            scale=alt.Scale(scheme="cividis", domain=(-0.5, 0.5)),
            legend=alt.Legend(
                orient="none",
                titleLimit=250,
                gradientLength=200,
                legendX=1100,
                legendY=-80,
                direction="horizontal",
            ),
        ),
        size=alt.value(20),
        tooltip=[
            "model_a",
            "model_b",
            "model_a_skill",
            "model_b_skill",
            "pvalue",
            "see_pvalue",
            "diff",
        ],
    )
    for t in TEST_NAMES.values():
        scatter_density = (
            base.transform_filter(datum.test_name == t)
            .transform_density("diff", as_=["diff", "density"])
            .transform_calculate(pct="datum.density / 100")
            .mark_area(orient="horizontal", opacity=0.3)
            .encode(
                x=alt.X(
                    "pct:Q", title="Density", axis=alt.Axis(orient="top", format="%")
                ),
                y=alt.Y(
                    "diff:Q", scale=alt.Scale(type="log", domain=(min_diff, max_diff))
                ),
            )
        )
        col_hist = base_hist.transform_filter(datum.test_name == t)
        col_scatter = (
            alt.layer(
                scatter_density, base_scatter.transform_filter(datum.test_name == t),
            )
            .resolve_scale(x="independent")
            .properties(width=200, height=200)
        )
        cols |= (col_scatter & col_hist).properties(
            title=alt.TitleParams(text=t, fontWeight="normal", anchor="middle", dx=23)
        )
    chart = cols.configure_title(anchor="middle").properties(
        title=alt.TitleParams(
            text=f"Comparison of Statistical Test Significance on SQuAD, Difference < {max_diff}",
            dy=30,
        )
    )

    if commit:
        save_chart(chart, COMMIT_PATH / "compare_tests", filetypes)
    else:
        save_chart(chart, FIGURE_PATH / "compare_tests", filetypes)


@register_plot("agreement")
@requires_files(TEST_FILES)
def plot_test_agreements(filetypes: List[str], commit: bool = False):
    tests = {}
    comparisons = set()
    for t in TESTS:
        path = (
            PAPER_PATH
            / "auto_data"
            / "data"
            / "stats"
            / "sampling=random"
            / "percent=100"
            / f"{t}.json"
        )
        results = read_json(path)["results"]
        pvalue_lookup = {}
        for row in results:
            pvalue_lookup[row["key"]] = row["pvalue"]
            comparisons.add(row["key"])

        tests[t] = pvalue_lookup

    alpha = 0.05
    rows = []
    for base_test in TESTS:
        for compare_test in TESTS:
            if base_test != compare_test:
                for key in comparisons:
                    base_pvalue = tests[base_test][key]
                    compare_pvalue = tests[compare_test][key]
                    if base_pvalue is None or compare_pvalue is None:
                        continue
                    base_sig = base_pvalue <= alpha
                    compare_sig = compare_pvalue <= alpha
                    rows.append(
                        {
                            "base_test": base_test,
                            "compare_test": compare_test,
                            "key": key,
                            "agree": "Yes" if base_sig == compare_sig else "No",
                            "base_pvalue": base_pvalue,
                        }
                    )
    df = pd.DataFrame(rows)
    group_df = df.groupby(["base_test", "compare_test", "agree"]).count().reset_index()
    group_df["n"] = group_df["key"]
    overall_chart = (
        alt.Chart(group_df)
        .mark_bar()
        .encode(
            x=alt.X("compare_test", title="", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("n", title="Number of (Dis)Agreements"),
            color=alt.Color("agree", title="Tests Agree?"),
            column=alt.Column("base_test", title=""),
        )
        .resolve_scale(x="independent")
    )
    if commit:
        save_chart(overall_chart, COMMIT_PATH / "test_agreement", filetypes)
    else:
        save_chart(overall_chart, FIGURE_PATH / "test_agreement", filetypes)

    disagree_df = df[df.agree == "No"]
    disagree_chart = (
        alt.Chart(disagree_df)
        .mark_bar()
        .encode(
            x=alt.X("base_pvalue", bin=alt.Bin(maxbins=50), title="P-Value of Test"),
            y=alt.Y("count()", title="Count"),
            color=alt.Color("compare_test", title="Test Compared"),
            facet=alt.Facet("base_test", columns=1, title=""),
        )
        .properties(
            height=100,
            title=alt.TitleParams(
                text="Distribution of P-Values on Disagreeing Tests", anchor="middle"
            ),
        )
        .resolve_scale(y="independent")
    )
    if commit:
        save_chart(disagree_chart, COMMIT_PATH / "disagree_pvalues", filetypes)
    else:
        save_chart(disagree_chart, FIGURE_PATH / "disagree_pvalues", filetypes)


@register_plot("mcnemar")
@requires_file(PAPER_PATH / "auto_data" / "data" / "power" / "mcnemar_trials.json")
def plot_mcnemar_simulation(filetypes: List[str], commit: bool = False):
    trials = read_json(
        PAPER_PATH / "auto_data" / "data" / "power" / "mcnemar_trials.json"
    )
    df = pd.DataFrame(trials["df"])
    df["macro"] = (df["power"] + df["antipower"]) / 2

    frames = []
    for var in ["power", "antipower", "macro"]:
        if var == "power":
            name = "P(detect | true effect)"
        elif var == "antipower":
            name = "P(no detect | no effect)"
        else:
            name = "Average"
        var_df = df.copy()
        var_df["variable"] = name
        var_df["value"] = var_df[var]
        frames.append(var_df)
    df = pd.concat(frames).drop(columns=["power", "antipower", "macro"])
    intervals = [0.05, 0.20, 0.40, 0.50, 0.60, 0.80, 0.95]
    sample = df[
        df.p_correct.map(lambda x: any(np.isclose(x, num) for num in intervals))
    ]
    base = alt.Chart(sample)
    scatter = base.mark_point().encode(
        x=alt.X("delta", title="Score Difference"),
        y=alt.Y("value", title="Measure Value"),
        shape=alt.Shape("variable", title="Measure"),
        color=alt.Color(
            "agreement:Q",
            title="Probability of Agreement",
            scale=alt.Scale(scheme="viridis"),
        ),
    )
    line = base.mark_line(color="black").encode(
        x="delta", y="value", strokeDash=alt.StrokeDash("variable", title="Measure"),
    )
    chart = (
        (line + scatter)
        .facet(alt.Facet("p_correct:N", title="Probability of Correct"), columns=4)
        .configure_header(format=".2f")
        .configure_legend(orient="top")
    )

    if commit:
        save_chart(chart, COMMIT_PATH / "mcnemar_simulation", filetypes)
    else:
        save_chart(chart, FIGURE_PATH / "mcnemar_simulation", filetypes)


def generate_irt_files():
    with open(PAPER_PATH / "config.toml") as f:
        conf = toml.load(f)
    irt_files = {}
    for model_type, evaluations in conf["irt"]["squad"]["dev"]["pyro"].items():
        for eval_type in ("full", "heldout"):
            irt_files[(model_type, eval_type)] = (
                PAPER_PATH / "auto_data" / evaluations[eval_type] / "report.json"
            )
    return irt_files


IRT_FILES = generate_irt_files()


@register_plot("irt_compare")
@requires_files(list(IRT_FILES.values()))
def plot_irt_comparison(filetypes: List[str], commit: bool = False):
    irt_reports = []
    for (model_type, eval_type), path in IRT_FILES.items():
        report = read_json(path)
        irt_reports.append(
            {
                "model": model_type,
                "evaluation": eval_type,
                "ROC AUC": report["roc_auc"],
                "Macro F1": report["classification_report"]["macro avg"]["f1-score"],
                # "Macro Precision": report["classification_report"]["macro avg"][
                #    "precision"
                # ],
                # "Macro Recall": report["classification_report"]["macro avg"]["recall"],
                #'weighted_f1': report['classification_report']['weighted avg']['f1-score'],
                #'weighted_precision': report['classification_report']['weighted avg']['precision'],
                #'weighted_recall': report['classification_report']['weighted avg']['recall'],
                "Accuracy": report["classification_report"]["accuracy"],
            }
        )
    report_df = pd.DataFrame(irt_reports)

    def to_precision_numbers(num, places):
        if isinstance(num, str):
            return r"\text{" + num + r"}"
        else:
            return to_precision(num, places)

    latex_out = (
        report_df[report_df.evaluation == "heldout"]
        .applymap(lambda n: f"${to_precision_numbers(n, 3)}$")
        .pivot(index="model", columns="evaluation")
        .reset_index()
        .to_latex(index=False, escape=False)
    )
    print(latex_out)

    df = report_df.melt(id_vars=["model", "evaluation"], var_name="metric")
    METRIC_SORT_ORDER = [
        "ROC AUC",
        "Macro F1",
        "Macro Precision",
        "Macro Recall",
        "Accuracy",
    ]
    heldout_df = df[df.evaluation == "heldout"]
    bars = (
        alt.Chart()
        .mark_bar()
        .encode(
            color=alt.Color(
                "model",
                title="IRT Model",
                scale=alt.Scale(scheme="category10"),
                legend=alt.Legend(orient="top"),
            ),
            x=alt.X(
                "model", title="", axis=alt.Axis(labels=False), sort=METRIC_SORT_ORDER,
            ),
            y=alt.Y(
                "value",
                title="Heldout Metric",
                scale=alt.Scale(zero=False, domain=[0.8, 1]),
            ),
            tooltip="value",
        )
        .properties(width=100, height=150)
    )
    font_size = 18
    text = bars.mark_text(align="center", baseline="middle", dy=-7, fontSize=14).encode(
        text=alt.Text("value:Q", format=".2r"), color=alt.value("black")
    )

    chart = (
        alt.layer(bars, text, data=heldout_df)
        .facet(column=alt.Column("metric", title=""))
        .configure_axis(labelFontSize=font_size, titleFontSize=font_size)
        .configure_legend(labelFontSize=font_size, titleFontSize=font_size)
        .configure_header(labelFontSize=font_size)
    )

    if commit:
        save_chart(chart, COMMIT_PATH / "irt_model_comparison", filetypes)
    else:
        save_chart(chart, FIGURE_PATH / "irt_model_comparison", filetypes)


@register_plot("sign_test")
def plot_sign_test(filetypes: List[str], commit: bool = False):
    def f(d, p):
        return d ** 2 + d + p - p ** 2 - 1 / 2

    x = np.linspace(0, 1, 100)
    y = f(0.01, x)
    df = pd.DataFrame({"x": x, "y": y})
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(x=alt.X("x", title="P"), y=alt.Y("y", title="Test Statistic Z"))
    )
    if commit:
        save_chart(chart, COMMIT_PATH / "sign_test", filetypes)
    else:
        save_chart(chart, FIGURE_PATH / "sign_test", filetypes)


def multi_caps(text):
    return " ".join(w.capitalize() for w in text.split())


@register_plot("example_analysis")
def table_annotation(filetypes: List[str], commit: bool = False):
    with open(PAPER_PATH / "examples.toml") as f:
        example_annotations = toml.load(f)

    rows = []
    for param, categories in example_annotations["item"].items():
        for category_name, annotations in categories.items():
            for labels in annotations.values():
                if len(labels) == 1:
                    reasons = ["none"]
                else:
                    reasons = labels[1:]
                outcome = labels[0]
                for r in reasons:
                    rows.append(
                        {
                            "param": param,
                            "category": category_name,
                            "validity": multi_caps(outcome),
                            "reason": multi_caps(r.replace("_", " ")),
                            "n": 1,
                            "param_category": param + " " + category_name,
                        }
                    )
    df = (
        pd.DataFrame(rows).groupby(["param_category", "validity", "reason"]).sum("n")
    ).reset_index()

    names = {
        "diff high": "Diff: High",
        "diff low": "Diff: Low",
        "disc high": "Disc: High",
        "disc near_zero": "Disc: ≈0",
        "disc negative": "Disc: Neg",
        "irt validation": "IRT Val",
    }
    df["param_category"] = df["param_category"].map(lambda x: names[x])
    font_size = 40
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("validity", title="", axis=alt.Axis(labelAngle=-25)),
            y=alt.Y("n", title="Count"),
            color=alt.Color(
                "reason",
                title="Explanation",
                scale=alt.Scale(scheme="category20"),
                legend=alt.Legend(orient="bottom"),
                sort=["None"],
            ),
            column=alt.Column("param_category", title=""),
        )
        .properties(height=200, width=300)
        .configure_axis(labelFontSize=font_size, titleFontSize=font_size, tickCount=10)
        .configure_legend(
            labelFontSize=font_size,
            titleFontSize=font_size,
            titleLimit=0,
            labelLimit=0,
            symbolLimit=0,
            symbolSize=400,
            columns=3,
        )
        .configure_header(labelFontSize=font_size, titleFontSize=font_size)
    )

    if commit:
        save_chart(chart, COMMIT_PATH / "example_analysis", filetypes)
    else:
        save_chart(chart, FIGURE_PATH / "example_analysis", filetypes)


def example_template(
    *,
    question_id,
    question_text,
    context,
    wiki_title,
    answer,
    validity,
    reason,
    diff,
    disc,
    feas,
    acc,
):
    lines = []
    lines.append(r"\begin{figure*}[ht]")
    lines.append(r"\center")
    lines.append(
        r"\tikz\node[draw=black!40!lightblue,inner sep=1pt,line width=0.3mm,rounded corners=0.1cm]{"
    )
    lines.append(r"\begin{tabular}{p{.95\textwidth}}")
    lines.append(
        r"\textbf{\discability{}}: %s \textbf{\diff{}}: %s \textbf{Feasibility}: %s \textbf{Mean Accuracy}: %s\\"
        % (disc, diff, feas, acc)
    )
    lines.append(r"\textbf{Validity}: %s \textbf{Reason}: %s\\" % (validity, reason))
    lines.append(
        r"\textbf{Wikipedia Page}: \underline{%s} \textbf{Question ID}: %s \\"
        % (wiki_title, question_id)
    )
    lines.append(r"\textbf{Question}: %s \\" % question_text)
    lines.append(r"\textbf{Official Answer}: %s \\" % answer)
    lines.append(r"\textbf{Context}: %s\\" % context)
    lines.append(r"\end{tabular}")
    lines.append(r"};")
    lines.append(r"\label{fig:ex-%s}" % question_id)
    lines.append(r"\end{figure*}")
    return "\n".join(lines)


def rater_example_template(
    *,
    question_id,
    question_text,
    context,
    wiki_title,
    answer,
    rater_0,
    rater_1,
    rater_2,
    validity_0,
    validity_1,
    validity_2,
    reason_0,
    reason_1,
    reason_2,
):
    lines = []
    lines.append(r"\begin{figure*}[ht]")
    lines.append(r"\center")
    lines.append(
        r"\tikz\node[draw=black!40!lightblue,inner sep=1pt,line width=0.3mm,rounded corners=0.1cm]{"
    )
    lines.append(r"\begin{tabular}{p{.95\textwidth}}")
    lines.append(
        r"\textbf{Wikipedia Page}: \underline{%s} \textbf{Question ID}: %s \\"
        % (wiki_title, question_id)
    )
    lines.append(r"\textbf{Question}: %s \\" % question_text)
    lines.append(r"\textbf{Official Answer}: %s \\" % answer)
    lines.append(r"\textbf{Context}: %s\\" % context)
    lines.append(
        r"\textbf{Validity}: %s \textbf{Reason}: %s \textbf{Rater}: %s\\"
        % (validity_0, reason_0, rater_0)
    )
    lines.append(
        r"\textbf{Validity}: %s \textbf{Reason}: %s \textbf{Rater}: %s\\"
        % (validity_1, reason_1, rater_1)
    )
    lines.append(
        r"\textbf{Validity}: %s \textbf{Reason}: %s \textbf{Rater}: %s\\"
        % (validity_2, reason_2, rater_2)
    )
    lines.append(r"\end{tabular}")
    lines.append(r"};")
    lines.append(r"\label{fig:ex-%s}" % question_id)
    lines.append(r"\end{figure*}")
    return "\n".join(lines)


@functools.lru_cache
def load_squad():
    squad = SquadV2.parse_file(DATA_PATH / conf["squad"]["dev_v2"])
    id_to_question = {}
    for page in squad.data:
        title = page.title
        for par in page.paragraphs:
            context = par.context
            for qas in par.qas:
                id_to_question[qas.id] = {
                    "text": qas.question,
                    "answers": " \\textbf{|} ".join(a.text for a in qas.answers),
                    "is_impossible": qas.is_impossible,
                    "context": context,
                    "title": title,
                }
    return id_to_question


def tex_escape(text):
    return unidecode.unidecode(
        text.replace("$", r"\$")
        .replace("%", r"\%")
        .replace("&", r"\&")
        .replace("_", r"\_")
    )


class Annotation(BaseModel):
    annotator: str
    qid: str
    correctness: str
    reasons: Set[str]


def parse_choices(choices: List[str]) -> Tuple[str, Set[str]]:
    correctness = choices[0]
    if len(choices) < 2:
        reasons = set()
    else:
        str_reason = choices[1]
        if "+" in str_reason:
            reasons = set(str_reason.split(" + "))
        else:
            reasons = {str_reason}

        # These aren't annotations, they are just used for visualization
        reasons.discard("low_probability")
        reasons.discard("high_probability")
    return correctness, reasons


OriginalAnnotations = Dict[str, Annotation]
PEDRO_EMAIL = "me@pedro.ai"


def load_original_annotations() -> OriginalAnnotations:
    with open(PAPER_PATH / "examples.toml") as f:
        annotations = {}
        original_annotations = toml.load(f)
        for item_id, choices in original_annotations["item"]["disc"][
            "negative"
        ].items():
            correctness, reasons = parse_choices(choices)
            annotations[item_id] = Annotation(
                qid=item_id,
                annotator=PEDRO_EMAIL,
                correctness=correctness,
                reasons=reasons,
            )

        for item_id, choices in original_annotations["item"]["disc"][
            "near_zero"
        ].items():
            correctness, reasons = parse_choices(choices)
            annotations[item_id] = Annotation(
                qid=item_id,
                annotator=PEDRO_EMAIL,
                correctness=correctness,
                reasons=reasons,
            )

        for item_id, choices in original_annotations["item"]["disc"]["high"].items():
            correctness, reasons = parse_choices(choices)
            annotations[item_id] = Annotation(
                qid=item_id,
                annotator=PEDRO_EMAIL,
                correctness=correctness,
                reasons=reasons,
            )

        for item_id, choices in original_annotations["item"]["diff"]["low"].items():
            correctness, reasons = parse_choices(choices)
            annotations[item_id] = Annotation(
                qid=item_id,
                annotator=PEDRO_EMAIL,
                correctness=correctness,
                reasons=reasons,
            )

        for item_id, choices in original_annotations["item"]["diff"]["high"].items():
            correctness, reasons = parse_choices(choices)
            annotations[item_id] = Annotation(
                qid=item_id,
                annotator=PEDRO_EMAIL,
                correctness=correctness,
                reasons=reasons,
            )

        for item_id, choices in original_annotations["item"]["irt"][
            "validation"
        ].items():
            correctness, reasons = parse_choices(choices)
            annotations[item_id] = Annotation(
                qid=item_id,
                annotator=PEDRO_EMAIL,
                correctness=correctness,
                reasons=reasons,
            )
        return annotations


AdditionalAnnotations = Dict[str, List[Annotation]]


def load_additional_annotations() -> AdditionalAnnotations:
    annotations = defaultdict(list)
    for item in read_json(PAPER_PATH / "data" / "label-studio.json"):
        qid = item["data"]["qid"]
        for annot in item["annotations"]:
            annotator = annot["completed_by"]["email"]
            result = annot["result"]
            correctness = set()
            reasons = set()
            for row in result:
                if row["from_name"] == "correctness_classes":
                    for choice in row["value"]["choices"]:
                        correctness.add(choice)
                elif row["from_name"] == "reason_classes":
                    for choice in row["value"]["choices"]:
                        reasons.add(choice)
                else:
                    raise ValueError(f"Unexpected row: {row}")
            if len(correctness) != 1:
                raise ValueError()
            else:
                correctness = list(correctness)[0]
            annotations[qid].append(
                Annotation(
                    qid=qid,
                    annotator=annotator,
                    correctness=correctness,
                    reasons=reasons,
                )
            )

    return dict(annotations)


JBARROW_EMAIL = "joseph.d.barrow@gmail.com"
PR_EMAIL = "me@pedro.ai"
HOYLE_EMAIL = "hoyle@umd.edu"
CORRECT = "correct"
FLAWED = "flawed"
WRONG = "wrong"


def binary(row):
    if row[JBARROW_EMAIL] == CORRECT:
        first_correct = CORRECT
    else:
        first_correct = WRONG

    if row[PR_EMAIL] == CORRECT:
        second_correct = CORRECT
    else:
        second_correct = WRONG

    if row[HOYLE_EMAIL] == CORRECT:
        second_correct = CORRECT
    else:
        second_correct = WRONG

    if first_correct == second_correct:
        return 1
    else:
        return 0


def correctness_to_int(label: str) -> int:
    if label == CORRECT:
        return 2
    elif label == FLAWED:
        return 1
    elif label == WRONG:
        return 0
    else:
        raise ValueError(f"Invalid label: {label}")


def correctness_to_binary(label: str) -> int:
    if label == CORRECT:
        return 1
    elif label == FLAWED:
        return 0
    elif label == WRONG:
        return 0
    else:
        raise ValueError(f"Invalid label: {label}")


class AnnotationAgreement:
    def __init__(self) -> None:
        self.original_annotations = load_original_annotations()
        self.additional_annotations = load_additional_annotations()
        self.merged_annotations: Dict[str, List[Annotation]] = {}
        self.item_ids = set(self.original_annotations) | set(
            self.additional_annotations
        )

        for item_id in self.item_ids:
            original = self.original_annotations[item_id]
            additional = self.additional_annotations[item_id]
            self.merged_annotations[item_id] = [original] + list(additional)

    def correctness_cohen_kappa(self):
        _, df = self.prepare_correctness_df()
        jb_pr_percent_agreement = df["jb_pr_agree"].mean()
        jb_ah_percent_agreement = df["jb_ah_agree"].mean()
        ah_pr_percent_agreement = df["ah_pr_agree"].mean()
        console.log(f"Correctness Percent Agreement JB PR: {jb_pr_percent_agreement}")
        console.log(f"Correctness Percent Agreement JB AH: {jb_ah_percent_agreement}")
        console.log(f"Correctness Percent Agreement AH PR: {ah_pr_percent_agreement}")
        return {
            "joe-pedro": metrics.cohen_kappa_score(df[JBARROW_EMAIL], df[PR_EMAIL]),
            "joe-alexander": metrics.cohen_kappa_score(
                df[JBARROW_EMAIL], df[HOYLE_EMAIL]
            ),
            "alexander-pedro": metrics.cohen_kappa_score(df[HOYLE_EMAIL], df[PR_EMAIL]),
        }

    def correctness_krippendorff(self):
        _, df = self.prepare_correctness_df()

        jb_ordinal = df[JBARROW_EMAIL].map(correctness_to_int)
        pr_ordinal = df[PR_EMAIL].map(correctness_to_int)
        ah_ordinal = df[HOYLE_EMAIL].map(correctness_to_int)
        all_coders_ordinal = np.array(
            [jb_ordinal.to_numpy(), pr_ordinal.to_numpy(), ah_ordinal.to_numpy(),]
        )
        coders_without_pr_ordinal = np.array(
            [jb_ordinal.to_numpy(), ah_ordinal.to_numpy(),]
        )

        jb_binary = df[JBARROW_EMAIL].map(correctness_to_int)
        pr_binary = df[PR_EMAIL].map(correctness_to_int)
        ah_binary = df[HOYLE_EMAIL].map(correctness_to_int)
        all_coders_binary = np.array(
            [jb_binary.to_numpy(), pr_binary.to_numpy(), ah_binary.to_numpy(),]
        )
        coders_without_pr_binary = np.array(
            [jb_binary.to_numpy(), ah_binary.to_numpy(),]
        )

        return {
            "ordinal_all": krippendorff.alpha(
                reliability_data=all_coders_ordinal, level_of_measurement="ordinal"
            ),
            "ordinal_without_pr": krippendorff.alpha(
                reliability_data=coders_without_pr_ordinal,
                level_of_measurement="ordinal",
            ),
            "binary_all": krippendorff.alpha(
                reliability_data=all_coders_binary, level_of_measurement="nominal"
            ),
            "binary_without_pr": krippendorff.alpha(
                reliability_data=coders_without_pr_binary,
                level_of_measurement="nominal",
            ),
        }

    def prepare_correctness_df(self,):
        rows = []
        for item_id, annotations in self.merged_annotations.items():
            for a in annotations:
                rows.append(
                    {
                        "item_id": item_id,
                        "annotator": a.annotator,
                        "correct": a.correctness,
                    }
                )

        tidy_df = pd.DataFrame(rows)
        df = tidy_df.pivot(
            index="item_id", columns="annotator", values="correct"
        ).reset_index()
        df["jb_pr_agree"] = df[JBARROW_EMAIL] == df[PR_EMAIL]
        df["jb_ah_agree"] = df[JBARROW_EMAIL] == df[HOYLE_EMAIL]
        df["ah_pr_agree"] = df[HOYLE_EMAIL] == df[PR_EMAIL]
        return tidy_df, df

    def prepare_reason_df(self):
        rows = []
        for item_id, annotations in self.merged_annotations.items():
            non_correct_agree = True
            item_rows = []
            for a in annotations:
                if a.correctness == CORRECT:
                    non_correct_agree = False
                item_rows.append(
                    {
                        "item_id": item_id,
                        "annotator": a.annotator,
                        "reason": a.reasons,
                        "correct": a.correctness,
                    }
                )
            if non_correct_agree:
                common_reasons = set()
                for r in item_rows:
                    if len(common_reasons) == 0:
                        common_reasons = set(r["reason"])
                    else:
                        common_reasons &= r["reason"]
                agreement = len(common_reasons) > 0
                for r in item_rows:
                    if agreement:
                        reason = list(common_reasons)[0]
                    else:
                        reason = list(r["reason"])[0]
                    rows.append(
                        {
                            "item_id": r["item_id"],
                            "annotator": r["annotator"],
                            "reason_agreement": agreement,
                            "original_reason": r["reason"],
                            "correct": r["correct"],
                            "reason": reason,
                        }
                    )

        tidy_df = pd.DataFrame(rows)
        df = tidy_df.pivot(
            index="item_id", columns="annotator", values="reason"
        ).reset_index()
        df["jb_pr_agree"] = df[JBARROW_EMAIL] == df[PR_EMAIL]
        df["jb_ah_agree"] = df[JBARROW_EMAIL] == df[HOYLE_EMAIL]
        df["ah_pr_agree"] = df[HOYLE_EMAIL] == df[PR_EMAIL]
        return tidy_df, df

    def reason_cohen_kappa(self):
        _, df = self.prepare_reason_df()
        jb_pr_percent_agreement = df["jb_pr_agree"].mean()
        jb_ah_percent_agreement = df["jb_ah_agree"].mean()
        ah_pr_percent_agreement = df["ah_pr_agree"].mean()
        console.log(f"Correctness Percent Agreement JB PR: {jb_pr_percent_agreement}")
        console.log(f"Correctness Percent Agreement JB AH: {jb_ah_percent_agreement}")
        console.log(f"Correctness Percent Agreement AH PR: {ah_pr_percent_agreement}")
        return {
            "joe-pedro": metrics.cohen_kappa_score(df[JBARROW_EMAIL], df[PR_EMAIL]),
            "joe-alexander": metrics.cohen_kappa_score(
                df[JBARROW_EMAIL], df[HOYLE_EMAIL]
            ),
            "alexander-pedro": metrics.cohen_kappa_score(df[HOYLE_EMAIL], df[PR_EMAIL]),
        }

    def disagreement_to_latex(self):
        squad = load_squad()
        output = []
        num = 1
        console.log(f"Total: {len(self.item_ids)}")
        for item_id in self.item_ids:
            question = squad[item_id]
            annotations = self.merged_annotations[item_id]
            if len(annotations) != 3:
                raise ValueError()
            rater_0, rater_1, rater_2 = annotations
            if rater_0.correctness != rater_1.correctness:
                output.append(
                    rater_example_template(
                        question_id=item_id,
                        question_text=tex_escape(question["text"]),
                        context=tex_escape(question["context"]),
                        wiki_title=tex_escape(question["title"]),
                        answer="Not Answerable"
                        if question["is_impossible"]
                        else tex_escape(question["answers"]),
                        rater_0=rater_0.annotator,
                        rater_1=rater_1.annotator,
                        rater_2=rater_2.annotator,
                        validity_0=tex_escape(rater_0.correctness),
                        validity_1=tex_escape(rater_1.correctness),
                        validity_2=tex_escape(rater_2.correctness),
                        reason_0=tex_escape(" ".join(rater_0.reasons)),
                        reason_1=tex_escape(" ".join(rater_1.reasons)),
                        reason_2=tex_escape(" ".join(rater_2.reasons)),
                    )
                )
                if num == 2:
                    output.append(r"\clearpage")
                    num = 1
                num += 1

        return "\n\n".join(output)


@register_plot("agreement")
def compute_annotator_agreement(filetypes: List[str], commit: bool = False):
    """This function computes inter-annotator agreement on the SQuAD examples
    that we (authors) manually annotated based on IRT features.

    Args:
        filetypes (List[str]): fieltypes to write
        commit (bool, optional): Whether to commit figs. Defaults to False.
    """
    annotation_agreement = AnnotationAgreement()
    correctness_kappa = annotation_agreement.correctness_cohen_kappa()
    console.log(f"Correctness Cohen Kappa: {correctness_kappa}")

    reason_kappa = annotation_agreement.reason_cohen_kappa()
    console.log(f"Reason Cohen Kappa: {reason_kappa}")

    correctness_kripp = annotation_agreement.correctness_krippendorff()
    console.log(f"Correctness Krippendorff alpha: {correctness_kripp}")

    latex_out = annotation_agreement.disagreement_to_latex()

    if commit:
        path = PAPER_PATH / "commit_auto_figs" / "disagreement_examples.tex"
    else:
        path = PAPER_PATH / "auto_fig" / "disagreement_examples.tex"

    with open(path, "w") as f:
        f.write(latex_out)


@register_plot("appendix_examples")
def appendix_examples(filetypes: List[str], commit: bool = False):
    irt_model = "3PL"
    irt_params = IrtParsed.from_irt_file(
        DATA_PATH
        / conf["irt"]["squad"]["dev"]["pyro"][irt_model]["full"]
        / "parameters.json"
    )
    predictions = LeaderboardPredictions.parse_file(
        DATA_PATH / conf["squad"]["submission_predictions"]["dev"]
    )
    item_accs = compute_item_accuracy(predictions)
    squad = load_squad()
    with open(PAPER_PATH / "examples.toml") as f:
        example_annotations = toml.load(f)

    section_names = {
        ("disc", "negative"): "Negative Discriminability",
        ("disc", "near_zero"): "Discriminability Near Zero",
        ("disc", "high"): "High Discriminability",
        ("diff", "low"): "Low Difficulty",
        ("diff", "high"): "High Difficulty",
        ("irt", "validation"): "IRT Prediction Errors",
    }
    output = []
    for param, categories in example_annotations["item"].items():
        for category_name, annotations in categories.items():
            name = section_names[(param, category_name)]
            output.append(r"\subsection{%s}" % name)
            for qid, labels in annotations.items():
                question = squad[qid]
                item_stats = irt_params.example_stats[qid]
                output.append(
                    example_template(
                        question_id=qid,
                        question_text=tex_escape(question["text"]),
                        context=tex_escape(question["context"]),
                        wiki_title=tex_escape(question["title"]),
                        answer="Not Answerable"
                        if question["is_impossible"]
                        else tex_escape(question["answers"]),
                        validity=tex_escape(labels[0]),
                        reason="NA" if len(labels) < 2 else tex_escape(labels[1]),
                        diff=to_precision(item_stats.diff, 3),
                        disc=to_precision(item_stats.disc, 3),
                        feas=to_precision(item_stats.lambda_, 3),
                        acc=to_precision(item_accs[qid], 3),
                    )
                )
            output.append(r"\clearpage")

    if commit:
        path = COMMIT_PATH / "appendix_examples.tex"
    else:
        path = FIGURE_PATH / "appendix_examples.tex"

    latex_out = "\n\n".join(output)
    with open(path, "w") as f:
        f.write(latex_out)


class Rectangle(pydantic.BaseModel):
    origin_x: int
    origin_y: int
    width: int
    height: int
    text: Optional[str]

    @property
    def x1(self):
        return self.origin_x

    @property
    def x2(self):
        return self.origin_x + self.width

    @property
    def y1(self):
        return self.origin_y

    @property
    def y2(self):
        return self.origin_y + self.height


class Line(pydantic.BaseModel):
    origin_x: float
    origin_y: float
    length: float
    angle: float

    @property
    def x_start(self):
        return self.origin_x

    @property
    def x_end(self):
        return self.origin_x + self.length * math.cos(math.pi * self.angle / 180)

    @property
    def y_start(self):
        return self.origin_y

    @property
    def y_end(self):
        return self.origin_y + self.length * math.sin(math.pi * self.angle / 180)


@register_plot("annotate_dist_pdf")
def annotate_dist_pdf(filetypes: List[str], commit: bool = False):
    pdf = PdfAnnotator(str(COMMIT_PATH / "irt_example_dist.pdf"))
    shapes = [
        Rectangle(origin_x=120, origin_y=200, width=25, height=52),
        Rectangle(origin_x=123, origin_y=50, width=30, height=70),
        Rectangle(origin_x=174, origin_y=93, width=25, height=32),
        Rectangle(origin_x=165, origin_y=136, width=35, height=30),
        Rectangle(origin_x=202, origin_y=79, width=51, height=29),
        Rectangle(origin_x=60, origin_y=133, width=45, height=20),
    ]
    for s in shapes:
        pdf.add_annotation(
            "square",
            Location(x1=s.x1, y1=s.y1, x2=s.x2, y2=s.y2, page=0),
            Appearance(stroke_color=(0, 0, 0), stroke_width=1),
        )
    text_annotations = [
        Rectangle(
            origin_x=170, origin_y=32, width=70, height=50, text="Annotation Error"
        ),
        Rectangle(
            origin_x=154,
            origin_y=152,
            width=60,
            height=50,
            text="Discriminative and Hard",
        ),
        Rectangle(
            origin_x=104, origin_y=231.5, width=60, height=50, text="Discriminative"
        ),
        Rectangle(origin_x=55, origin_y=134, width=60, height=50, text="Easy"),
    ]
    for t in text_annotations:
        pdf.add_annotation(
            "text",
            Location(x1=t.x1, y1=t.y1, x2=t.x2, y2=t.y2, page=0),
            Appearance(
                fill=[0, 0, 0],
                stroke_width=1,
                font_size=9,
                content=t.text,
                text_align="center",
            ),
        )
    lines = [
        Line(origin_x=200, origin_y=65, length=34.5, angle=24),
        Line(origin_x=200, origin_y=65, length=31, angle=115),
        Line(origin_x=200.5, origin_y=65, length=50.5, angle=160),
    ]
    for l in lines:
        pdf.add_annotation(
            "line",
            Location(points=[[l.x_start, l.y_start], [l.x_end, l.y_end]], page=0),
            Appearance(),
        )
    if commit:
        pdf.write(COMMIT_PATH / "annotated_irt_example_dist.pdf")
    else:
        pdf.write(FIGURE_PATH / "annotated_irt_example_dist.pdf")


def main(
    plot: Optional[List[str]] = typer.Option(None),
    seed: int = 42,
    filetype: Optional[List[str]] = typer.Option(None),
    commit: bool = False,
):
    random.seed(seed)
    if filetype is None or len(filetype) == 0:
        filetype = ["svg", "pdf", "json", "png"]

    console.log("Output Filetypes:", filetype)
    console.log("Commit:", commit)

    if plot is None or len(plot) == 0:
        for name, func in PLOTS.items():
            console.log(f"Plotting: {name}")
            func(filetype, commit=commit)
    else:
        for p in plot:
            console.log(f"Plotting: {p}")
            PLOTS[p](filetype, commit=commit)


if __name__ == "__main__":
    typer.run(main)

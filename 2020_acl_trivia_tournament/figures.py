
# Script to create plots for your paper
from math import floor
from collections import defaultdict
import os

import pandas as pd
import numpy as np

from plotnine import *

palette = {2: ["#4285F4", "#EA4335"],
           3: ["#4285F4", "#EA4335", "#FBBC04"],
           4: ["#4285F4", "#EA4335", "#FBBC04", "#34A853"]}

kROOT_DIR = "2020_acl_trivia_tournament"

def datadir(filename):
    return "%s/data/%s" % (kROOT_DIR, filename)

def gfxdir(filename):
    return "%s/auto_fig/%s" % (kROOT_DIR, filename)

def one_dataset(acc_a, acc_b, effective_prop, size, runs):
  """Given two QA systems on a dataset, will you reach correct result

  Args:
    acc_a: Accuracy of worse system
    acc_b: Accuracy of better system
    effective_prop: How many of the questions are effective
    size: Number of examples in dataset
    runs: How many times to run experiment

  Returns:
    Probability of declaring better system winner.
  """
  assert acc_b >= acc_a, "We assume second system is better"

  effective_size = round(effective_prop * size)

  a_output = np.random.binomial(effective_size, acc_a, runs)
  b_output = np.random.binomial(effective_size, acc_b, runs)

  return sum(1 for x, y in zip(a_output, b_output) if y > x) / runs

def size_needed(acc_a, acc_b, effective_prop, desired_prob,
                runs=5000, min=1, max=100000):
  """How many questions do you need to declare correct winner?

    desired_prob: How confident you want to be that correct system wins
  Returns:
    Total size of dataset needed
  """

  while (max - min) > 1:
    probe = floor((max + min) / 2)
    prob = one_dataset(acc_a, acc_b, effective_prop, probe, runs)
    if prob < desired_prob:
      min = probe
    else:
      max = probe
    print("[%i, %i]: %i -> %f" % (min, max, probe, prob))

  return max

def generate_dataframe(confidences = [.95],
                       effectives = [1.0, .85, .25],
                       acc_pivot = [0.5, 0.8],
                       steps = 500):
  filename = "%s_%s_%s_%i.csv" % (str(confidences), str(effectives),
                                  str(acc_pivot), steps)
  try:
    data = pd.read_csv(datadir(filename))
    print("Read %s from cache" % filename)
  except IOError:
    data = _generate_dataframe(confidences, effectives, acc_pivot, steps)
    data.to_csv(datadir(filename))
  return data

def _generate_dataframe(confidences, effectives, acc_pivot, steps):
  data = defaultdict(list)
  for cc in confidences:
    for rho in effectives:
      for ii in range(steps):
        for aa in acc_pivot:
          delta = min(1.0 - aa, aa) / steps

          acc_a = aa - ii * delta
          acc_b = aa + ii * delta

          if acc_b - acc_a < 0.02 or acc_b - acc_a > 0.35:
            continue

          print("===========================\n".join(["C: %f U: %f A: %f B: %f" %
                                                      (cc, rho, acc_a, acc_b)]))
          data["Confidence"].append(cc)
          data["Effective Proportion"].append(r"$\rho=%0.2f$" % rho)
          data["Average Accuracy"].append(str(aa * 100))
          data[r"$\Delta$ Accuracy"].append(ii * delta * 100)
          data["Test Needed"].append(size_needed(acc_a, acc_b, rho, cc))
  return pd.DataFrame.from_dict(data)

def test_dataset_needed_plot(filename, size, limit_rho=None):
  if limit_rho is not None:
    data = generate_dataframe(effectives=[limit_rho])
  else:
    data = generate_dataframe()

  p = (ggplot(aes(x=r"$\Delta$ Accuracy", y="Test Needed", color="Average Accuracy"), data=data) +
       geom_line(stat='identity', size=1) +
       scale_y_continuous(trans='sqrt', breaks=[100, 1000, 2500, 5000, 10000, 25000, 50000]) +
       scale_x_continuous(breaks=[1, 2, 5, 10, 15, 20]) +
       scale_fill_discrete(palette=palette[4]) +
       # facet_grid("Confidence ~ Effective Proportion", scales="free") +
       facet_grid("~ Effective Proportion") +
       theme(figure_size=size,
             legend_position='right')
       )
  p.save(gfxdir(filename), dpi=400)
  return data, p

if __name__ == "__main__":
  # Create data dir if doesn't already exist
  if not os.path.exists("%s/data" % kROOT_DIR):
    os.makedirs("%s/data" % kROOT_DIR)

  for filename, size, rho in [("test_set.pdf", (6, 1), None),
                        ("test_set-1.0.png", (3, 2), 1.0),
                        ("test_set-0.75.png", (3, 2), 0.75),
                        ("test_set-0.5.png", (3, 2), 0.5),
                        ("test_set-0.1.png", (3, 2), 0.1)]:
    data, plot = test_dataset_needed_plot(filename, size, rho)
    print(data.head())

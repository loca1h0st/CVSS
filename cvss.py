#!/usr/bin/env python3
#
# Author: Fredrik Hedman <fredrik.hedman@noruna.se>
# Version: 0.2
# LICENSE: MIT LICENSE
#
"""
Calculate CVSS metrics based on a list of Metrics.
"""
from metric import Metric
from cvss_base import CVSS
from cvss_210 import CommonVulnerabilityScore

def base_metrics():
    BASE_METRICS = [
        ["Access Vector", "AV",
         [("Local", "L", 0.395, "Local access"),
          ("Adjecent Network", "A", 0.646, "Adjacent network access"),
          ("Network", "N", 1.0, "Network access") ]],
        ["Access Complexity", "AC",
         [("High", "H", 0.35, "Specialized access conditions exist"),
          ("Medium", "M", 0.61, "The access conditions are somewhat specialized"),
          ("Low", "L", 0.71, "No specialized access exist") ]],
        ["Authentication", "Au",
         [("Multiple", "M", 0.45, "Authenticate two or more times"),
          ("Single", "S", 0.56, "Logged into the system"),
          ("None", "N", 0.704, "Authentication not required") ]],
        ["Confidentiality Impact", "C",
         [("None", "N", 0.0, "No impact"),
          ("Partial", "P", 0.275, "Considerable disclosure"),
          ("Complete", "C", 0.660, "Total inforamtion disclosure") ]],
        ["Integrity Impact", "I",
         [("None", "N", 0.0, "No impact"),
          ("Partial", "P", 0.275, "Possible to modify some system files or information"),
          ("Complete", "C", 0.660, "Total compromise of system integrity") ]],
        ["Availability Impact", "A",
         [("None", "N", 0.0, "No impact"),
          ("Partial", "P", 0.275, "Reduced performance or interruptions in resource availability"),
          ("Complete", "C", 0.660, "Total shutdown of the affected resource") ]],
    ]
    return BASE_METRICS


def temporal_metrics():
    TEMPORAL_METRICS = [
    ["Exploitability", "E",
     [("Unproven", "U", 0.85, "No exploit code is available"),
      ("Proof-of-Concept", "POC", 0.9, "Proof-of-concept exploit code exists"),
      ("Functional", "F", 0.95, "Functional exploit code is available"),
      ("High", "H", 1.0, "Exploitable by functional mobile autonomous code"),
      ("Not Defined", "ND", 1.0, "Skip this metric") ]],
    ["Remediation Level", "RL",
     [("Official Fix", "OF", 0.87, "Complete vendor solution is available"),
      ("Temporary Fix", "TF", 0.90, "Official but temporary fix available"),
      ("Workaround", "W", 0.95, "Unofficial, non-vendor solution available"),
      ("Unavailable", "U", 1.0, "No solution available or it is impossible to apply"),
      ("Not Defined", "ND", 1.0, "Skip this metric") ]],
    ["Report Confidence", "RC",
     [("Unconfirmed", "UC", 0.90, "Single unconfirmed source"),
      ("Uncorroborated", "UR", 0.95, "Multiple non-official sources"),
      ("Confirmed", "C", 1.0, "Acknowledged by the vendor or author"),
      ("Not Defined", "ND", 1.0, "Skip this metric") ]],
    ]
    return TEMPORAL_METRICS

def environmental_metrics():
    ENVIRONMENTAL_METRICS = [
    ["Collateral Damage Potential", "CDP",
     [("None", "N", 0.0, "No potential for loss of life"),
      ("Low", "L", 0.1, "Potential for slight physical or property damage"),
      ("Low-Medium", "LM", 0.3, "Moderate physical or property damage"),
      ("Medium-High", "MH", 0.4, "Significant physical or property damage or loss"),
      ("High", "H", 0.5, "Catastrophic physical or property damage and loss"),
      ("Not Defined", "ND", 0.9, "Skip this metric") ]],
    ["Target Distribution", "TD",
     [("None", "N", 0.0, "No target systems exist"),
      ("Low", "L", 0.25, "Targets exist on a small scale inside the environment"),
      ("Medium", "M", 0.75, "Targets exist on a medium scale"),
      ("High", "H", 1.0, "Targets exist on a considerable scale"),
      ("Not Defined", "ND", 1.0, "Skip this metric") ]],
    ["Confidentiality Requirement", "CR",
     [("Low", "L", 0.5, "Limited adverse effect"),
      ("Medium", "M", 1.0, "Serious adverse effect"),
      ("High", "H", 1.51, "Catastrophic adverse effect"),
      ("Not Defined", "ND", 1.0, "Skip this metric") ]],
    ["Integrity Requirement", "IR",
     [("Low", "L", 0.5, "Limited adverse effect"),
      ("Medium", "M", 1.0, "Serious adverse effect"),
      ("High", "H", 1.51, "Catastrophic adverse effect"),
      ("Not Defined", "ND", 1.0, "Skip this metric") ]],
    ["Availability Requirement", "AR",
     [("Low", "L", 0.5, "Limited adverse effect"),
      ("Medium", "M", 1.0, "Serious adverse effect"),
      ("High", "H", 1.51, "Catastrophic adverse effect"),
      ("Not Defined", "ND", 1.0, "Skip this metric") ]],
    ]
    return ENVIRONMENTAL_METRICS

def add_padding(to_length, selected):
    if selected == None:
        selected =  []
    padding = to_length - len(selected)
    if padding:
        selected.extend(padding * [None])
    return selected

def prepare_metrics(L, selected):
    lmetrics = []
    for ii, mm in enumerate(L):
        lmetrics.append(Metric(*mm, index = selected[ii]))
    return lmetrics

def cvs_factory(cls, selected = None):
    L = base_metrics()
    L.extend(temporal_metrics())
    L.extend(environmental_metrics())
    selected = add_padding(len(L), selected)
    lmetrics = prepare_metrics(L, selected)
    return cls(lmetrics)

def select_metric_value(m):
    m = Metric(*m)
    default_metric_value = m.index
    print(10*'+', m.name, m.short_name, 10*'+')
    while True:
        for v in m.values:
            print(v, v.description)
        idx = input('Select one [{0}]: '.format(default_metric_value)).upper()

        if not idx:
           idx = default_metric_value

        print('Selected metric value ###|', idx, '|###')

        try:
            m.index = idx
        except AssertionError:
            print('Not valid')
        else:
            return m.index

def display_score(H, F, ML, FD, VEC):
    def display_header(H):
        print('{0:<{3}}{1:<{3}}{2}'.format(H[0], H[1], H[2], W0))
    def display_metrics(ML):
        for m in ML:
            print('{0:<{3}}{1:<{3}}{2:>{4}.2f}'.format(m.name,
                                                       m.selected.metric,
                                                       m.selected.number,
                                                       W0, W1))
    def display_footer(F):
        W2 = len(S1) - len(F[1])
        print('{0:<{2}}{1}'.format(F[0], F[1], W2))
    def display_footer_data(FD, VEC):
        for d in FD:
            print('{0:<{2}}{1:>{3}.2f}'.format(d[0] + ' =', d[1], 2*W0, W1))
        print('{1} Vulnerability Vector: {0}'.format(VEC[1], VEC[0]))
    #
    W0 = 30
    W1 = len(H[2])
    S1 = (W0*2 + W1) * '='
    #
    print(S1)
    display_header(H)
    print(S1)
    display_metrics(ML)
    print(S1)
    display_footer(F)
    print(S1)
    display_footer_data(FD, VEC)
    print(S1)


if __name__ == "__main__":
    selected = []

    L = base_metrics()
    for m in L:
        mm = select_metric_value(m)
        selected.append(mm)

    L = temporal_metrics()
    for m in L:
        mm = select_metric_value(m)
        selected.append(mm)

    L = environmental_metrics()
    for m in L:
        mm = select_metric_value(m)
        selected.append(mm)

    cvs = cvs_factory(CommonVulnerabilityScore, selected)

    display_score(["BASE METRIC", "EVALUATION", "SCORE"],
                  ["FORMULA", "BASE SCORE"],
                  cvs.base_metrics(),
                  [ ('Impact', cvs.impact),
                    ('Exploitability', cvs.exploitability),
                    ('Base Score', cvs.base_score) ],
                  ('Base', cvs.base_vulnerability_vector))

    display_score(["TEMPORAL METRIC", "EVALUATION", "SCORE"],
                  ["FORMULA", "TEMPORAL SCORE"],
                  cvs.temporal_metrics(),
                  [ ('Temporal Score', cvs.temporal_score) ],
                  ('Temporal', cvs.temporal_vulnerability_vector))

    display_score(["ENIRONMENTAL METRIC", "EVALUATION", "SCORE"],
                  ["FORMULA", "ENIRONMENTAL SCORE"],
                  cvs.environmental_metrics(),
                  [ ('Adjusted Impact', cvs.adjusted_impact),
                    ('Adjusted Base', cvs.adjusted_base_score),
                    ('Adjusted Temporal', cvs.adjusted_temporal_score),
                    ('Environmental Score', cvs.environmental_score) ],
                  ('Environmental', cvs.environmental_vulnerability_vector))




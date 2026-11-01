"""Chapter 5 examples from Weiss (ed.), Multiagent Systems, 2nd ed., 2013.

ASCII a1 means the book's alpha_1. Utilities use the corrected ownership.
"""
from engine import ArgumentationFramework, GroundedMechanism


def example_5_10():
    af = ArgumentationFramework(['a1','a2','a3','a4','a5'],
                               [('a1','a2'),('a2','a3'),('a3','a4'),('a3','a5')])
    return GroundedMechanism(af, [{'a1','a4','a5'}, {'a2'}, {'a3'}])


def example_5_11():
    af = ArgumentationFramework(['a1','a2','a3','a4','a5','a6'],
                               [('a1','a2'),('a2','a3'),('a3','a4'),('a3','a5'),('a6','a3')])
    return GroundedMechanism(af, [{'a1','a4','a5','a6'}, {'a2'}, {'a3'}])

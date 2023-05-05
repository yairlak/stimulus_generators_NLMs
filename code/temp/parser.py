import spacy
import benepar  # Must be imported even if not used.

"""
To install locally:

In terminal:
$ python -m spacy download en_core_web_lg
$ pip uninstall protobuf
$ pip install protobuf==3.20.1

In Python:
>> import benepar
>> benepar.download("benepar_en3")
"""


def _children(tree):
    return tuple(tree.children)


def _label(tree):
    if not tree:
        return None
    labels = tuple(tree.labels)
    if len(labels):
        return labels[0]
    return None


def _left_child(tree):
    children = _children(tree)
    if children:
        return _children(tree)[0]._
    return None


def _2nd_child(tree):
    children = _children(tree)
    if children:
        return _children(tree)[1]._
    return None


def _right_child(tree):
    children = _children(tree)
    if children:
        return _children(tree)[-1]._
    return None


def is_long_range_agreement(sentence):
    nlp = spacy.load("en_core_web_lg")
    nlp.add_pipe("benepar", config={"model": "benepar_en3"})
    doc = nlp(sentence)
    parse = list(doc.sents)[0]

    tree = parse._
    head = _left_child(tree)
    right_child_of_head = _right_child(head)
    right_child = _right_child(tree)

    return (
        _label(head) == "NP"
        and _label(right_child_of_head) in {"SBAR", "PP"}
        and _label(right_child) == "VP"
    )


def test():
    positive_sentences = (
        "The boy near the cars smiles",
        "a sons that interrupt the sisters ignore a girls",
        "The idea that the daughters that the fathers interrupt ignore is ridiculous",
        "the woman that defends the actress blocks the friend",
        "a friend that blocks the farmers observes an actor",
        "the sister that blocks the girls avoids the students",
        "girl that watches the sisters interrupts actress",
        "a daughter that meets the mothers avoids an actresses",
        "girls that interrupt the farmer greet man",
        "the sisters that interrupt the father avoid the friends",
        "the daughters that stop the brother meet the student",
    )

    negative_sentences = (
        "The boy smiles",
        "a son ignore a girls",
        "The idea is ridiculous",
        "the woman blocks the friend",
        "a friend observes an actor",
        "the sister avoids the students",
        "the girl interrupts the actress",
        "a daughter avoids an actresses",
        "girls greet men",
        "the sisters avoid the friends",
        "the daughters meet the student",
    )

    for s in positive_sentences:
        assert is_long_range_agreement(s), s

    for s in negative_sentences:
        assert not is_long_range_agreement(s), s


if __name__ == "__main__":
    test()

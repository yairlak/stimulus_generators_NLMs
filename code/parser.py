import spacy
import benepar

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
    return tuple(tree.labels)[0]


def _left_child(tree):
    return tuple(tree.children)[0]._


def _2nd_child(tree):
    return tuple(tree.children)[1]._


def _right_child(tree):
    return tuple(tree.children)[-1]._


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
    sentences = (
        "The boy near the cars smiles",
        "a sons that interrupt the sisters ignore a girls",
        "The idea that the daughters that the fathers interrupt ignore is ridiculous",
    )

    for s in sentences:
        print(is_long_range_agreement(s))


if __name__ == "__main__":
    test()

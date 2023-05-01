import csv
import itertools
import random
import re

from lexicon_English import Words

FEATURES = {
    "gender": ["masculine", "feminine"],
    "definiteness": ["definit", "a"],
    "number": ["singular", "plural"]
}

REMAP_POS = {
    "P": "pronouns",
    "N": "nouns",
    "V": "verbs",
    "N_SC": "nouns_SC",
    "det": "determinants",
    "V_copula": "copula",
    "V_MATRIX": "matrix_verbs"
}


def find_features(pos: str):
    pos_features = []
    try:
        W = Words[pos]
        for _ in range(len(FEATURES.keys())):
            for feature in FEATURES:
                try:
                    W = W[FEATURES[feature][0]]
                    pos_features.append(feature)
                except:
                    pass
    except:
        pass
    return pos_features


def extract_features():
    Words_features = {}
    for pos in Words.keys():
        Words_features[pos] = find_features(pos)
    return Words_features


Words_features = extract_features()


def csv_to_param(csvfilename):
    with open(csvfilename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        templates_param = []
        for row in reader:
            row['n_repetitions'] = float(row['n_repetitions'])
            other_cols = {key: value for key, value in row.items() if key not in ['name', 'n_repetitions', 'template']}
            row_dict = {
                'name': row['name'],
                'n_repetitions': row['n_repetitions'],
                'template_str': row['template'],
                'labels': other_cols.values()}
            templates_param.append(row_dict)
    return templates_param


class Word:
    def __init__(self, word_code: str):
        self.word_code = word_code
        match = re.search(r"([^\d]*)(\d*)$", word_code)
        self.pos = match.group(1)
        try:
            self.pos = REMAP_POS[self.pos]
        except:
            pass
        f_index = match.group(2)
        self.f_index = int(f_index) if f_index else 0
    def sample(self, features=None):
        w = Word(self.word_code)
        try:
            w_features = Words_features[self.pos]
            w_pool = Words[self.pos]
            if features is None:
                features = {}
            for f in w_features:
                try:
                    f_value = features[f]
                except:
                    f_value = random.choice(FEATURES[f])
                    features[f] = f_value
                w_pool = w_pool[f_value]
            w.lemma_ix, w.word_form = random.choice(list(enumerate(w_pool)))
        except:
            w.lemma_ix = None
            w.word_form = w.word_code
        return w, features


class Label:
    def __init__(self, label_code: str=""):
        self.label_code = label_code

        if (self.label_code) and (self.label_code[0] == "w"):
            self.type = "w"
            label_split = self.label_code[1:].split("__")
            if len(label_split) == 2:
                self.index, self.feature = label_split
            else:
                self.type = "code"
        else:
            self.type = "code"

    def extract(self, sentence):
        if self.type == "code":
            return self.label_code
        else:
            try:
                return sentence.features[int(self.index)][self.feature]
            except:
                return "FAILED"  # or underspecified?


class Template:
    def __init__(self, template_str: str, name: str = "", labels: list = None, n_repetitions: int = 1):
        self.name = name
        self.template_str = template_str
        self.n_repetitions = n_repetitions
        if labels is not None:
            self.labels = [Label(label) for label in labels]
        else:
            self.labels = None
        self.calc_words()
        self.calc_indices()
        self.calc_all_possible_features()

    def calc_words(self):
        word_codes = self.template_str.split(" ")
        self.words = [Word(w) for w in word_codes]

    def calc_indices(self):
        self.indices = set(w.f_index for w in self.words if w.f_index > 0)
        self.feature_indices = {
            ind: self.index_features(ind)
            for ind in self.indices
        }

    def index_features(self, f_index):
        index_poss = set(
            w.pos for w in self.words
            if w.f_index == f_index)
        index_features = set(
            feature
            for pos in index_poss
            for feature in Words_features.get(pos, []))
        return index_features

    def calc_all_possible_features(self):
        self.all_possible_features = []
        ind_feat = [
            (index, feature, FEATURES[feature])
            for index, feature_list in self.feature_indices.items()
            for feature in feature_list]
        combinations = (itertools.product(*[pair[2] for pair in ind_feat]))
        for combination in combinations:
            d = {ind: {} for ind in self.indices}
            for ((ind, f), fv) in zip(
                    [(x[0], x[1]) for x in ind_feat],
                    combination):
                d[ind][f] = fv
            self.all_possible_features.append(d)

    def generate_sentence(self, features=None):
        if features is None:
            features = {}
        sentence = Sentence(template=self)
        for w in self.words:
            try:
                w_form, final_features = w.sample(features[w.f_index])
            except:
                w_form, final_features = w.sample()
            features[w.f_index] = final_features
            sentence.add_word(w_form)
            sentence.add_features(features)
        return sentence

    def generate_corpus_feature(self, feature=None, n_repetitions=None):
        if n_repetitions is None:
            n_repetitions = self.n_repetitions
        if n_repetitions is None:
            n_repetitions = 1
        sentences = []
        n_rep = 0
        n_attempt = 0
        while (n_rep < n_repetitions) and (n_attempt < 2 + 0 * n_repetitions):
            n_attempt += 1
            sentence = self.generate_sentence(feature)
            if not (sentence in sentences):
                if (sentence.is_unique_words()):
                    sentences.append(sentence)
                    n_rep += 1
        return sentences

    def generate_corpus(self, feature=None, n_repetitions=None):
        if n_repetitions is None:
            n_repetitions = self.n_repetitions
        if n_repetitions is None:
            n_repetitions = 1
        sentences = []
        for feature in self.all_possible_features:
            new_sentences = self.generate_corpus_feature(feature=feature, n_repetitions=n_repetitions)
            sentences.extend(new_sentences)
        return sentences


class Sentence:
    def __init__(self, words=None, template=None, features=None):
        self.template = template
        self.features = features
        self.words = words if words else []

    def add_word(self, word):
        self.words.append(word)

    def add_features(self, features):
        self.features = features

    def is_unique_words(self):
        seen_pairs = set()
        for w in self.words:
            if w.lemma_ix:
                pos_lemma_ix_pair = (w.pos, w.lemma_ix)
                if pos_lemma_ix_pair in seen_pairs:
                    return False
                seen_pairs.add(pos_lemma_ix_pair)
        return True

    def __repr__(self):
        for i, w in enumerate(self.words[:-1]):
            if w.word_form in ["a", "an"]:
                w_next = self.words[i+1]
                if w_next.word_form[0] in ["a", "e", "i", "o", "u"]:  # forget about 'h'
                    w.word_form = "an"
                else:
                    w.word_form = "a"

        res = " ".join([w.word_form for w in self.words])
        res = res.replace("  ", " ").strip().lower()
        return res

    def show_labels(self):
        labels = []
        if self.template.labels is not None:
            labels = [
                label.extract(self)
                for label in self.template.labels]
        return "\t".join(labels)

    def __eq__(self, other):
        if isinstance(other, Sentence):
            return repr(self) == repr(other)
        return False


if __name__ == "__main__":
    print()
    template = Template("determinants1 nouns1 verbs1 .", labels=["w1__number"])
    c = template.generate_corpus(n_repetitions=1)
    for s in c:
        print(f"- {s}\t{s.show_labels()}")
    print()

    templates_param = csv_to_param('code/templates.csv')
    for template_param in templates_param:
        template = Template(**template_param)
        c = template.generate_corpus()
        for s in c:
            print(f"- {s}\t{s.show_labels()}")
        print()

import sys, argparse
import numpy as np
from lexicon_English import Words

# Output is a tab-delimited list of stimuli with info: sentence \t tense \t subject gender \t subject number

# Parse arguments
parser = argparse.ArgumentParser(description='Stimulus generator for Italian')
parser.add_argument('-t', '--natask', default='embedding_mental', type=str, help = 'Number-agreement (NA) task to generate (nounpp/subjrel_that/objrel_that)')
parser.add_argument('-n', default=250 , type=int, help = 'number of samples from each condition')
parser.add_argument('-seed', default=1 , type=int, help = 'Random seed for replicability')
args = parser.parse_args()

stimuli = []
np.random.seed(args.seed)

def construct_DP(subject, subject_gender, subject_number):
    ''' This function returns the index to the pertinent article given the gender and grammatical number of the noun.
    For example, singular nouns that begins with a vowel go with the article "l'" before them, whereas singular masculine
    starting with, e.g., 'sp' will go with 'lo'.
    !!! The function expects a FIXED structure for each type of article (see lexicon). For example,
    definit['masc']['sing'] = ['il', 'lo', "l'"]
    definit['masc']['plur'] = ['i', 'gli']
    definit['femi']['sing'] = ['la', "l'"]
    definit['femi']['plur'] = ['le']
    So for a singular noun starting with a vowel the function will return the index IX=-1 (last element in the list).
    For a singular masculin noun starting with 'sp' the function witll return the index IX=1, thus referring to 'lo'.
    :param subject: string of the noun (e.g., 'tavolo')
    :param subject_gender: string ('masc' or 'femi')
    :param subject_number: string ('plur' or 'sing')
    :return: IX [0, 1, or -1]. Index to the token in the list (assuming a fixed structure - see lexicon_*.py)
    '''
    #vowels = ['a', 'e', 'i', 'o', 'u']

    # Tests for initial letters
    #subject = subject.lower()
    #starts_with_vowel = subject[0] in vowels

    IX = 0
    #if subject_number == 'singular':
    #    if starts_with_vowel:
    #        IX = -1 # choose det l'

    return IX


def get_random_article(determiners):
    # Generates a random (definite) article
    rand_gender = ['masculine', 'feminine'][np.random.randint(2)]
    rand_number = ['singular', 'plural'][np.random.randint(2)]
    num_possible_articles = len(determiners['definit'][rand_gender][rand_number])
    rand_IX = np.random.randint(num_possible_articles)
    return determiners['definit'][rand_gender][rand_number][rand_IX]


def init_counter(features):
    # Create counter
    import itertools
    counter = {}
    feature_combinations = list(itertools.product(*features.values()))
    for comb in feature_combinations:
        counter['_'.join(comb)] = 0
    return counter


def counter_fullfilled(counter, n):
    return False if any(v < n for v in list(counter.values())) else True


# det N1 that the N2 V2 V1 det N3
if args.natask == 'subjrel':

    genders = ['masculine', 'feminine']
    numbers = ['singular', 'plural']

    features = {}
    features['N1_gender'] = genders
    features['N1_number'] = numbers
    features['N2_gender'] = genders
    features['N2_number'] = numbers
    counter = init_counter(features)

    while not counter_fullfilled(counter, args.n):
        # N1
        N1_gender = genders[np.random.randint(2)]
        N1_number = numbers[np.random.randint(2)]
        N1s = Words['nouns'][N1_gender][N1_number]#[0:num_nouns]
        IX_N1 = np.random.randint(len(N1s))
        N1 = N1s[IX_N1]
        # N2
        N2_gender = genders[np.random.randint(2)]
        N2_number = numbers[np.random.randint(2)]
        N2s = Words['nouns'][N2_gender][N2_number]#[0:num_nouns]
        IX_N2 = np.random.randint(len(N2s))
        N2 = N2s[IX_N2]
        # N3
        N3_gender = genders[np.random.randint(2)]
        N3_number = numbers[np.random.randint(2)]
        N3s = Words['nouns'][N3_gender][N3_number]#[0:num_nouns]
        IX_N3 = np.random.randint(len(N3s))
        N3 = N3s[IX_N3]
        # V1
        V1s = Words['verbs'][N1_number]#[0:num_nouns]
        IX_V1 = np.random.randint(len(V1s))
        V1 = V1s[IX_V1]
        # V2
        V2s = Words['verbs'][N1_number]
        IX_V2 = np.random.randint(len(V2s))
        V2 = V2s[IX_V2]
        # sentence
        opposite_number_V2 = 'singular' if N2_number == 'plural' else 'plural'
        opposite_number_V1 = 'singular' if N1_number == 'plural' else 'plural'
        sentence = ' '.join(['The', N1, 'that', V2, 'the', N2, V1, 'the', N3])

        noun_IXs = [IX_N1, IX_N2, IX_N3]
        if len(set(noun_IXs)) == len(noun_IXs): # check noun repetition at the lemma level (i.e., all indexes are different)
            if IX_V1 != IX_V2:                  # check verb repetition at the lemma level
                if counter['_'.join([N1_gender, N1_number, N2_gender, N2_number])] < args.n:
                    stimuli.append([args.natask, sentence,
                           N1_gender, N1_number,
                           N2_gender, N2_number,
                           N3_gender, N3_number,
                           Words['verbs'][opposite_number_V1][IX_V1], Words['verbs'][opposite_number_V2][IX_V2]])
                    counter['_'.join([N1_gender, N1_number, N2_gender, N2_number])]+=1

    stimuli.sort(key=lambda x: x[1]) # first word
    stimuli.sort(key=lambda x: x[7], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[5], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[3], reverse=True) # feature 2
    [print('\t'.join(l)) for l in stimuli]

# det N1 that the N2 V2 V1 det N3
if args.natask == 'objrel':

    genders = ['masculine', 'feminine']
    numbers = ['singular', 'plural']

    features = {}
    features['N1_gender'] = genders
    features['N1_number'] = numbers
    features['N2_gender'] = genders
    features['N2_number'] = numbers
    counter = init_counter(features)

    while not counter_fullfilled(counter, args.n):
        # N1
        N1_gender = genders[np.random.randint(2)]
        N1_number = numbers[np.random.randint(2)]
        N1s = Words['nouns'][N1_gender][N1_number]#[0:num_nouns]
        IX_N1 = np.random.randint(len(N1s))
        N1 = N1s[IX_N1]
        # N2
        N2_gender = genders[np.random.randint(2)]
        N2_number = numbers[np.random.randint(2)]
        N2s = Words['nouns'][N2_gender][N2_number]#[0:num_nouns]
        IX_N2 = np.random.randint(len(N2s))
        N2 = N2s[IX_N2]
        # N3
        N3_gender = genders[np.random.randint(2)]
        N3_number = numbers[np.random.randint(2)]
        N3s = Words['nouns'][N3_gender][N3_number]#[0:num_nouns]
        IX_N3 = np.random.randint(len(N3s))
        N3 = N3s[IX_N3]
        # V1
        V1s = Words['verbs'][N1_number]#[0:num_nouns]
        IX_V1 = np.random.randint(len(V1s))
        V1 = V1s[IX_V1]
        # V2
        V2s = Words['verbs'][N2_number]
        IX_V2 = np.random.randint(len(V2s))
        V2 = V2s[IX_V2]
        # sentence
        opposite_number_V2 = 'singular' if N2_number == 'plural' else 'plural'
        opposite_number_V1 = 'singular' if N1_number == 'plural' else 'plural'
        sentence = ' '.join(['The', N1, 'that', 'the', N2, V2, V1, 'the', N3])

        noun_IXs = [IX_N1, IX_N2, IX_N3]
        if len(set(noun_IXs)) == len(noun_IXs): # check noun repetition at the lemma level (i.e., all indexes are different)
            if IX_V1 != IX_V2:                  # check verb repetition at the lemma level
                if counter['_'.join([N1_gender, N1_number, N2_gender, N2_number])] < args.n:
                    stimuli.append([args.natask, sentence,
                           N1_gender, N1_number,
                           N2_gender, N2_number,
                           N3_gender, N3_number,
                           Words['verbs'][opposite_number_V1][IX_V1], Words['verbs'][opposite_number_V2][IX_V2]])
                    counter['_'.join([N1_gender, N1_number, N2_gender, N2_number])]+=1

    stimuli.sort(key=lambda x: x[1]) # first word
    stimuli.sort(key=lambda x: x[7], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[5], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[3], reverse=True) # feature 2
    [print('\t'.join(l)) for l in stimuli]

# det N1 that the pronuon V2 V1 det N3
if args.natask == 'objrel_pronoun':

    genders = ['masculine', 'feminine']
    numbers = ['singular', 'plural']

    features = {}
    features['N1_gender'] = genders
    features['N1_number'] = numbers
    features['N2_gender'] = genders
    features['N2_number'] = numbers
    counter = init_counter(features)

    while not counter_fullfilled(counter, args.n):
        # N1
        N1_gender = genders[np.random.randint(2)]
        N1_number = numbers[np.random.randint(2)]
        N1s = Words['nouns'][N1_gender][N1_number]#[0:num_nouns]
        IX_N1 = np.random.randint(len(N1s))
        N1 = N1s[IX_N1]
        # N2
        N2_gender = genders[np.random.randint(2)]
        N2_number = numbers[np.random.randint(2)]
        N2s = Words['pronouns'][N2_gender][N2_number]#[0:num_nouns]
        IX_N2 = np.random.randint(len(N2s))
        N2 = N2s[IX_N2]
        # N3
        N3_gender = genders[np.random.randint(2)]
        N3_number = numbers[np.random.randint(2)]
        N3s = Words['nouns'][N3_gender][N3_number]#[0:num_nouns]
        IX_N3 = np.random.randint(len(N3s))
        N3 = N3s[IX_N3]
        # V1
        V1s = Words['verbs'][N1_number]#[0:num_nouns]
        IX_V1 = np.random.randint(len(V1s))
        V1 = V1s[IX_V1]
        # V2
        V2s = Words['verbs'][N2_number]
        IX_V2 = np.random.randint(len(V2s))
        V2 = V2s[IX_V2]
        # sentence
        opposite_number_V2 = 'singular' if N2_number == 'plural' else 'plural'
        opposite_number_V1 = 'singular' if N1_number == 'plural' else 'plural'
        sentence = ' '.join(['The', N1, 'that', N2, V2, V1, 'the', N3])

        noun_IXs = [IX_N1, IX_N2, IX_N3]
        if len(set(noun_IXs)) == len(noun_IXs): # check noun repetition at the lemma level (i.e., all indexes are different)
            if IX_V1 != IX_V2:                  # check verb repetition at the lemma level
                if counter['_'.join([N1_gender, N1_number, N2_gender, N2_number])] < args.n:
                    stimuli.append([args.natask, sentence,
                           N1_gender, N1_number,
                           N2_gender, N2_number,
                           N3_gender, N3_number,
                           Words['verbs'][opposite_number_V1][IX_V1], Words['verbs'][opposite_number_V2][IX_V2]])
                    counter['_'.join([N1_gender, N1_number, N2_gender, N2_number])]+=1

    stimuli.sort(key=lambda x: x[1]) # first word
    stimuli.sort(key=lambda x: x[7], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[5], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[3], reverse=True) # feature 2
    [print('\t'.join(l)) for l in stimuli]

if args.natask == 'objrel_nounpp':

    genders = ['masculine', 'feminine']
    numbers = ['singular', 'plural']

    features = {}
    features['N1_gender'] = genders
    features['N1_number'] = numbers
    features['N2_gender'] = genders
    features['N2_number'] = numbers
    features['N3_gender'] = genders
    features['N3_number'] = numbers
    counter = init_counter(features)

    while not counter_fullfilled(counter, args.n):
        # N1
        N1_gender = genders[np.random.randint(2)]
        N1_number = numbers[np.random.randint(2)]
        N1s = Words['nouns'][N1_gender][N1_number]#[0:num_nouns]
        IX_N1 = np.random.randint(len(N1s))
        N1 = N1s[IX_N1]
        # N2
        N2_gender = genders[np.random.randint(2)]
        N2_number = numbers[np.random.randint(2)]
        N2s = Words['nouns'][N2_gender][N2_number]#[0:num_nouns]
        IX_N2 = np.random.randint(len(N2s))
        N2 = N2s[IX_N2]
        # N3
        N3_gender = genders[np.random.randint(2)]
        N3_number = numbers[np.random.randint(2)]
        N3s = Words['nouns'][N3_gender][N3_number]#[0:num_nouns]
        IX_N3 = np.random.randint(len(N3s))
        N3 = N3s[IX_N3]
        # N4
        N4_gender = genders[np.random.randint(2)]
        N4_number = numbers[np.random.randint(2)]
        N4s = Words['nouns'][N4_gender][N4_number]#[0:num_nouns]
        IX_N4 = np.random.randint(len(N4s))
        N4 = N4s[IX_N4]
        # V1
        V1s = Words['verbs'][N1_number]#[0:num_nouns]
        IX_V1 = np.random.randint(len(V1s))
        V1 = V1s[IX_V1]
        # V2
        V2s = Words['verbs'][N2_number]
        IX_V2 = np.random.randint(len(V2s))
        V2 = V2s[IX_V2]
        # prep
        preps = Words['loc_preps']
        IX_prep = np.random.randint(len(preps))
        prep = preps[IX_prep]
        # sentence
        opposite_number_V2 = 'singular' if N2_number == 'plural' else 'plural'
        opposite_number_V1 = 'singular' if N1_number == 'plural' else 'plural'
        last_article = get_random_article(Words['determinants'])
        sentence = ' '.join(['The', N1, 'that', 'the', N2, prep, 'the', N3, V2, V1, 'the', N4])

        noun_IXs = [IX_N1, IX_N2, IX_N3, IX_N4]
        if len(set(noun_IXs)) == len(noun_IXs): # check noun repetition at the lemma level (i.e., all indexes are different)
            if IX_V1 != IX_V2:                  # check verb repetition at the lemma level
                if counter['_'.join([N1_gender, N1_number, N2_gender, N2_number, N3_gender, N3_number])] < args.n:
                    stimuli.append([args.natask, sentence,
                           N1_gender, N1_number,
                           N2_gender, N2_number,
                           N3_gender, N3_number,
                           Words['verbs'][opposite_number_V1][IX_V1], Words['verbs'][opposite_number_V2][IX_V2]])
                    counter['_'.join([N1_gender, N1_number, N2_gender, N2_number, N3_gender, N3_number])]+=1

    stimuli.sort(key=lambda x: x[1]) # first word
    stimuli.sort(key=lambda x: x[7], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[5], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[3], reverse=True) # feature 2
    [print('\t'.join(l)) for l in stimuli]

# det N1 that the N2 V2 V1 det N3
if args.natask == 'embedding_mental_SR':

    genders = ['masculine', 'feminine']
    numbers = ['singular', 'plural']

    features = {}
    features['N1_gender'] = genders
    features['N1_number'] = numbers
    features['N2_gender'] = genders
    features['N2_number'] = numbers
    counter = init_counter(features)

    while not counter_fullfilled(counter, args.n):
        # N1
        N1_gender = genders[np.random.randint(2)]
        N1_number = numbers[np.random.randint(2)]
        N1s = Words['nouns'][N1_gender][N1_number]#[0:num_nouns]
        IX_N1 = np.random.randint(len(N1s))
        N1 = N1s[IX_N1]
        # N2
        N2_gender = genders[np.random.randint(2)]
        N2_number = numbers[np.random.randint(2)]
        N2s = Words['nouns'][N2_gender][N2_number]#[0:num_nouns]
        IX_N2 = np.random.randint(len(N2s))
        N2 = N2s[IX_N2]
        # N3
        N3_gender = genders[np.random.randint(2)]
        N3_number = numbers[np.random.randint(2)]
        N3s = Words['nouns'][N3_gender][N3_number]#[0:num_nouns]
        IX_N3 = np.random.randint(len(N3s))
        N3 = N3s[IX_N3]
        # V1
        V1s = Words['matrix_verbs'][N1_number]#[0:num_nouns]
        IX_V1 = np.random.randint(len(V1s))
        V1 = V1s[IX_V1]
        # V2
        V2s = Words['verbs'][N2_number]
        IX_V2 = np.random.randint(len(V2s))
        V2 = V2s[IX_V2]
        # sentence
        opposite_number_V2 = 'singular' if N2_number == 'plural' else 'plural'
        opposite_number_V1 = 'singular' if N1_number == 'plural' else 'plural'
        sentence = ' '.join(['The', N1, V1, 'that', 'the', N2, V2, 'the', N3])

        noun_IXs = [IX_N1, IX_N2, IX_N3]
        if len(set(noun_IXs)) == len(noun_IXs): # check noun repetition at the lemma level (i.e., all indexes are different)
            if IX_V1 != IX_V2:                  # check verb repetition at the lemma level
                if counter['_'.join([N1_gender, N1_number, N2_gender, N2_number])] < args.n:
                    stimuli.append([args.natask, sentence,
                           N1_gender, N1_number,
                           N2_gender, N2_number,
                           N3_gender, N3_number,
                           Words['matrix_verbs'][opposite_number_V1][IX_V1], Words['verbs'][opposite_number_V2][IX_V2]])
                    counter['_'.join([N1_gender, N1_number, N2_gender, N2_number])]+=1

    stimuli.sort(key=lambda x: x[1]) # first word
    stimuli.sort(key=lambda x: x[7], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[5], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[3], reverse=True) # feature 2
    [print('\t'.join(l)) for l in stimuli]

# The N1 V1_MATRIX that the N2 prep the N3 V2 the N4
if args.natask == 'embedding_mental':

    genders = ['masculine', 'feminine']
    numbers = ['singular', 'plural']

    features = {}
    features['N1_gender'] = genders
    features['N1_number'] = numbers
    features['N2_gender'] = genders
    features['N2_number'] = numbers
    features['N3_gender'] = genders
    features['N3_number'] = numbers
    counter = init_counter(features)

    while not counter_fullfilled(counter, args.n):
        # N1
        N1_gender = genders[np.random.randint(2)]
        N1_number = numbers[np.random.randint(2)]
        N1s = Words['nouns'][N1_gender][N1_number]#[0:num_nouns]
        IX_N1 = np.random.randint(len(N1s))
        N1 = N1s[IX_N1]
        # N2
        N2_gender = genders[np.random.randint(2)]
        N2_number = numbers[np.random.randint(2)]
        N2s = Words['nouns'][N2_gender][N2_number]#[0:num_nouns]
        IX_N2 = np.random.randint(len(N2s))
        N2 = N2s[IX_N2]
        # N3
        N3_gender = genders[np.random.randint(2)]
        N3_number = numbers[np.random.randint(2)]
        N3s = Words['nouns'][N3_gender][N3_number]#[0:num_nouns]
        IX_N3 = np.random.randint(len(N3s))
        N3 = N3s[IX_N3]
        # N4
        N4_gender = genders[np.random.randint(2)]
        N4_number = numbers[np.random.randint(2)]
        N4s = Words['nouns'][N4_gender][N4_number]#[0:num_nouns]
        IX_N4 = np.random.randint(len(N4s))
        N4 = N4s[IX_N4]
        # V1
        V1s = Words['matrix_verbs'][N1_number]#[0:num_nouns]
        IX_V1 = np.random.randint(len(V1s))
        V1 = V1s[IX_V1]
        # V2
        V2s = Words['verbs'][N2_number]
        IX_V2 = np.random.randint(len(V2s))
        V2 = V2s[IX_V2]
        # prep
        preps = Words['loc_preps']
        IX_prep = np.random.randint(len(preps))
        prep = preps[IX_prep]
        # sentence
        opposite_number_V2 = 'singular' if N2_number == 'plural' else 'plural'
        opposite_number_V1 = 'singular' if N1_number == 'plural' else 'plural'
        sentence = ' '.join(['The', N1, V1, 'that', 'the', N2, prep, 'the', N3, V2, 'the', N4])

        noun_IXs = [IX_N1, IX_N2, IX_N3, IX_N4]
        if len(set(noun_IXs)) == len(noun_IXs): # check noun repetition at the lemma level (i.e., all indexes are different)
            if IX_V1 != IX_V2:                  # check verb repetition at the lemma level
                if counter['_'.join([N1_gender, N1_number, N2_gender, N2_number, N3_gender, N3_number])] < args.n:
                    stimuli.append([args.natask, sentence,
                           N1_gender, N1_number,
                           N2_gender, N2_number,
                           N3_gender, N3_number,
                           Words['matrix_verbs'][opposite_number_V1][IX_V1], Words['verbs'][opposite_number_V2][IX_V2]])
                    counter['_'.join([N1_gender, N1_number, N2_gender, N2_number, N3_gender, N3_number])]+=1

    stimuli.sort(key=lambda x: x[1]) # first word
    stimuli.sort(key=lambda x: x[7], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[5], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[3], reverse=True) # feature 2
    [print('\t'.join(l)) for l in stimuli]

# The N1 prep1 the N3 V1_MATRIX that the N2 prep2 the N4 V2 the N5
# - opposite genders: not used?
if args.natask == 'embedding_mental_2LRs':

    genders = ['masculine', 'feminine']
    numbers = ['singular', 'plural']

    features = {}
    features['N1_gender'] = genders
    features['N1_number'] = numbers
    features['N2_gender'] = genders
    features['N2_number'] = numbers
    features['N3_gender'] = genders
    features['N3_number'] = numbers
    features['N4_gender'] = genders
    features['N4_number'] = numbers
    counter = init_counter(features)

    while not counter_fullfilled(counter, args.n):
        # N1
        N1_gender = genders[np.random.randint(2)]
        N1_number = numbers[np.random.randint(2)]
        N1s = Words['nouns'][N1_gender][N1_number]#[0:num_nouns]
        IX_N1 = np.random.randint(len(N1s))
        N1 = N1s[IX_N1]
        # N2
        N2_gender = genders[np.random.randint(2)]
        N2_number = numbers[np.random.randint(2)]
        N2s = Words['nouns'][N2_gender][N2_number]#[0:num_nouns]
        IX_N2 = np.random.randint(len(N2s))
        N2 = N2s[IX_N2]
        # N3
        N3_gender = genders[np.random.randint(2)]
        N3_number = numbers[np.random.randint(2)]
        N3s = Words['nouns'][N3_gender][N3_number]#[0:num_nouns]
        IX_N3 = np.random.randint(len(N3s))
        N3 = N3s[IX_N3]
        # N4
        N4_gender = genders[np.random.randint(2)]
        N4_number = numbers[np.random.randint(2)]
        N4s = Words['nouns'][N4_gender][N4_number]#[0:num_nouns]
        IX_N4 = np.random.randint(len(N4s))
        N4 = N4s[IX_N4]
        # N5
        N5_gender = genders[np.random.randint(2)]
        N5_number = numbers[np.random.randint(2)]
        N5s = Words['nouns'][N5_gender][N5_number]#[0:num_nouns]
        IX_N5 = np.random.randint(len(N5s))
        N5 = N5s[IX_N5]
        # V1
        V1s = Words['matrix_verbs'][N1_number]#[0:num_nouns]
        IX_V1 = np.random.randint(len(V1s))
        V1 = V1s[IX_V1]
        # V2
        V2s = Words['verbs'][N2_number]
        IX_V2 = np.random.randint(len(V2s))
        V2 = V2s[IX_V2]
        # prep1 and prep2
        preps = Words['loc_preps']
        IX_prep1 = np.random.randint(len(preps))
        prep1 = preps[IX_prep1]
        IX_prep2 = np.random.randint(len(preps))
        prep2 = preps[IX_prep2]
        # sentence
        opposite_number_V2 = 'singular' if N2_number == 'plural' else 'plural'
        opposite_number_V1 = 'singular' if N1_number == 'plural' else 'plural'
        sentence = ' '.join(['The', N1, prep1, 'the', N3, V1, 'that', 'the', N2, prep2, 'the', N4, V2, 'the', N5])

        noun_IXs = [IX_N1, IX_N2, IX_N3, IX_N4, IX_N5]
        if len(set(noun_IXs)) == len(noun_IXs): # check noun repetition at the lemma level (i.e., all indexes are different)
            if IX_V1 != IX_V2:                  # check verb repetition at the lemma level
                if IX_prep1 != IX_prep2:
                    if counter['_'.join([N1_gender, N1_number, N2_gender, N2_number, N3_gender, N3_number, N4_gender, N4_number])] < args.n:
                        stimuli.append([args.natask, sentence,
                               N1_gender, N1_number,
                               N2_gender, N2_number,
                               N3_gender, N3_number,
                               N4_gender, N4_number,
                               Words['matrix_verbs'][opposite_number_V1][IX_V1], Words['verbs'][opposite_number_V2][IX_V2]])
                        counter['_'.join([N1_gender, N1_number, N2_gender, N2_number, N3_gender, N3_number, N4_gender, N4_number])]+=1

    stimuli.sort(key=lambda x: x[1]) # first word
    stimuli.sort(key=lambda x: x[7], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[5], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[3], reverse=True) # feature 2
    [print('\t'.join(l)) for l in stimuli]

# The N1 that the N2 that the N3 V3 V2 V1 the N4
if args.natask == 'OR_OR':

    genders = ['masculine', 'feminine']
    numbers = ['singular', 'plural']

    features = {}
    features['N1_gender'] = genders
    features['N1_number'] = numbers
    features['N2_gender'] = genders
    features['N2_number'] = numbers
    features['N3_gender'] = genders
    features['N3_number'] = numbers
    features['N4_gender'] = genders
    features['N4_number'] = numbers
    counter = init_counter(features)

    while not counter_fullfilled(counter, args.n):
        # N1
        N1_gender = genders[np.random.randint(2)]
        N1_number = numbers[np.random.randint(2)]
        N1s = Words['nouns'][N1_gender][N1_number]#[0:num_nouns]
        IX_N1 = np.random.randint(len(N1s))
        N1 = N1s[IX_N1]
        # N2
        N2_gender = genders[np.random.randint(2)]
        N2_number = numbers[np.random.randint(2)]
        N2s = Words['nouns'][N2_gender][N2_number]#[0:num_nouns]
        IX_N2 = np.random.randint(len(N2s))
        N2 = N2s[IX_N2]
        # N3
        N3_gender = genders[np.random.randint(2)]
        N3_number = numbers[np.random.randint(2)]
        N3s = Words['nouns'][N3_gender][N3_number]#[0:num_nouns]
        IX_N3 = np.random.randint(len(N3s))
        N3 = N3s[IX_N3]
        # N4
        N4_gender = genders[np.random.randint(2)]
        N4_number = numbers[np.random.randint(2)]
        N4s = Words['nouns'][N4_gender][N4_number]#[0:num_nouns]
        IX_N4 = np.random.randint(len(N4s))
        N4 = N4s[IX_N4]
        # V1
        V1s = Words['verbs'][N1_number]#[0:num_nouns]
        IX_V1 = np.random.randint(len(V1s))
        V1 = V1s[IX_V1]
        # V2
        V2s = Words['verbs'][N2_number]
        IX_V2 = np.random.randint(len(V2s))
        V2 = V2s[IX_V2]
        # V3
        V3s = Words['verbs'][N3_number]
        IX_V3 = np.random.randint(len(V3s))
        V3 = V3s[IX_V3]
        # sentence
        opposite_number_V3 = 'singular' if N3_number == 'plural' else 'plural'
        opposite_number_V2 = 'singular' if N2_number == 'plural' else 'plural'
        opposite_number_V1 = 'singular' if N1_number == 'plural' else 'plural'
        last_article = get_random_article(Words['determinants'])
        sentence = ' '.join(['The', N1, 'that', 'the', N2, 'that', 'the', N3, V3, V2, V1, 'the', N4])

        noun_IXs = [IX_N1, IX_N2, IX_N3, IX_N4]
        verb_IXs = [IX_V1, IX_V2, IX_V3]
        if len(set(noun_IXs)) == len(noun_IXs): # check noun repetition at the lemma level (i.e., all indexes are different)
            if len(set(verb_IXs)) == len(verb_IXs): # check verb repetition at the lemma level
                if counter['_'.join([N1_gender, N1_number, N2_gender, N2_number, N3_gender, N3_number, N4_gender, N4_number])] < args.n:
                    stimuli.append([args.natask, sentence,
                           N1_gender, N1_number,
                           N2_gender, N2_number,
                           N3_gender, N3_number,
                           N4_gender, N4_number,
                           Words['verbs'][opposite_number_V1][IX_V1], Words['verbs'][opposite_number_V2][IX_V2], Words['verbs'][opposite_number_V3][IX_V3]])
                    counter['_'.join([N1_gender, N1_number, N2_gender, N2_number, N3_gender, N3_number, N4_gender, N4_number])]+=1

    stimuli.sort(key=lambda x: x[1]) # first word
    stimuli.sort(key=lambda x: x[7], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[5], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[3], reverse=True) # feature 2
    [print('\t'.join(l)) for l in stimuli]

# The N1 that the N2 that the N3 V3 V2 V1 ridiculous
if args.natask == 'SC_OR':

    genders = ['masculine', 'feminine']
    numbers = ['singular', 'plural']

    features = {}
    features['N1_number'] = numbers
    features['N2_gender'] = genders
    features['N2_number'] = numbers
    features['N3_gender'] = genders
    features['N3_number'] = numbers
    counter = init_counter(features)

    while not counter_fullfilled(counter, args.n):
        # N1
        N1_gender = genders[np.random.randint(2)]
        N1_number = numbers[np.random.randint(2)]
        N1s = Words['nouns_SC'][N1_number]#[0:num_nouns]
        IX_N1 = np.random.randint(len(N1s))
        N1 = N1s[IX_N1]
        # N2
        N2_gender = genders[np.random.randint(2)]
        N2_number = numbers[np.random.randint(2)]
        N2s = Words['nouns'][N2_gender][N2_number]#[0:num_nouns]
        IX_N2 = np.random.randint(len(N2s))
        N2 = N2s[IX_N2]
        # N3
        N3_gender = genders[np.random.randint(2)]
        N3_number = numbers[np.random.randint(2)]
        N3s = Words['nouns'][N3_gender][N3_number]#[0:num_nouns]
        IX_N3 = np.random.randint(len(N3s))
        N3 = N3s[IX_N3]
        # V1
        V1s = Words['copula'][N1_number]#[0:num_nouns]
        IX_V1 = np.random.randint(len(V1s))
        V1 = V1s[IX_V1]
        # V2
        V2s = Words['verbs_intran'][N2_number]
        IX_V2 = np.random.randint(len(V2s))
        V2 = V2s[IX_V2]
        # V3
        V3s = Words['verbs'][N3_number]
        IX_V3 = np.random.randint(len(V3s))
        V3 = V3s[IX_V3]
        # sentence
        opposite_number_V3 = 'singular' if N3_number == 'plural' else 'plural'
        opposite_number_V2 = 'singular' if N2_number == 'plural' else 'plural'
        opposite_number_V1 = 'singular' if N1_number == 'plural' else 'plural'
        last_article = get_random_article(Words['determinants'])
        sentence = ' '.join(['The', N1, 'that', 'the', N2, 'that', 'the', N3, V3, V2, V1, 'ridiculous'])

        noun_IXs = [IX_N1, IX_N2, IX_N3]
        if len(set(noun_IXs)) == len(noun_IXs): # check noun repetition at the lemma level (i.e., all indexes are different)
            if IX_V2 != IX_V3:                  # check verb repetition at the lemma level
                if counter['_'.join([N1_number, N2_gender, N2_number, N3_gender, N3_number])] < args.n:
                    stimuli.append([args.natask, sentence,
                           'NA', N1_number,
                           N2_gender, N2_number,
                           N3_gender, N3_number,
                           Words['copula'][opposite_number_V1][IX_V1], Words['verbs_intran'][opposite_number_V2][IX_V2], Words['verbs'][opposite_number_V3][IX_V3]])
                    counter['_'.join([N1_number, N2_gender, N2_number, N3_gender, N3_number])]+=1

    stimuli.sort(key=lambda x: x[1]) # first word
    stimuli.sort(key=lambda x: x[7], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[5], reverse=True) # feature 1
    stimuli.sort(key=lambda x: x[3], reverse=True) # feature 2
    [print('\t'.join(l)) for l in stimuli]
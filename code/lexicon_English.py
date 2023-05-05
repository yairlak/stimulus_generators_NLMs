###################
###### DET ########
###################
# DEFINITE
# --------
# Initialization

determinants = {}
definit = {}
a = {}
for gender in ['masculine', 'feminine']:
    definit[gender] = {}
    a[gender] = {}
# Tokens
definit['masculine']['singular'] = ['The']
definit['masculine']['plural'] = ['The']
definit['feminine']['singular'] = ['The']
definit['feminine']['plural'] = ['The']

a['masculine']['singular'] = ['a', 'an']
a['masculine']['plural'] = ['']
a['feminine']['singular'] = ['a', 'an']
a['feminine']['plural'] = ['']

determinants = {'definit':definit, 'a':a}

###################
###### PRONOUNS ######
###################
# Initialization
pronouns = {}
for gender in ['masculine', 'feminine']:
    pronouns[gender] = {}
# Tokens
pronouns['masculine']['singular'] = ['he']
pronouns['masculine']['plural'] = ['they']
pronouns['feminine']['singular'] = ['she']
pronouns['feminine']['plural'] = ['they']

###################
###### ANAPHORAS ######
###################
# Initialization
anaphoras = {}
for gender in ['masculine', 'feminine']:
    anaphoras[gender] = {}
# Tokens
anaphoras['masculine']['singular'] = ['himself']
anaphoras['masculine']['plural'] = ['themselves']
anaphoras['feminine']['singular'] = ['herself']
anaphoras['feminine']['plural'] = ['themselves']

###################
###### QUANTIFIERS ######
###################
# Initialization
quantifiers = {}
# Tokens
quantifiers['singular'] = ['every', 'no']
quantifiers['plural'] = ['all', 'few']

###################
###### PROPER NAMES ######
###################
# Initialization
proper_names = {}
for number in ['singular']:
    proper_names[number] = {}
# Tokens
proper_names['singular']['masculine']=['John', 'Bob']
proper_names['singular']['feminine']=['Mary', 'Alice']

###################
###### NOUNS ######
###################
# Initialization
nouns = {}
for gender in ['masculine', 'feminine']:
    nouns[gender] = {}
# Tokens
nouns['masculine']['singular'] = ['brother', 'father', 'boy', 'man']
nouns['masculine']['plural'] = ['brothers', 'fathers', 'boys', 'men']
nouns['feminine']['singular'] = ['sister', 'mother', 'girl', 'woman']
nouns['feminine']['plural'] = ['sisters', 'mothers', 'girls', 'women']


nouns_inanimate = {}
nouns_inanimate['singular'] = ['car', 'table', 'pen']
nouns_inanimate['plural'] = ['cars', 'tables', 'pens']
    
###################
####SC NOUNS ######
###################
# Initialization
nouns_SC = {}
# Tokens
nouns_SC['singular'] = ['fact', 'idea', 'thought']
nouns_SC['plural'] = ['facts', 'ideas', 'thoughts']

# LOCATION NOUNS
# --------------
# Initialization
location_nouns = {}
for gender in ['masculine', 'feminine']:
    location_nouns[gender] = {}
# Tokens
location_nouns['masculine']['singular'] = nouns['masculine']['singular']
location_nouns['masculine']['plural'] = nouns['masculine']['plural']
location_nouns['feminine']['singular'] = nouns['feminine']['singular']
location_nouns['feminine']['plural'] = nouns['feminine']['plural']

###################
###### VERBS ######
###################
# Initialization
verbs, verbs_intran_anim, verbs_intran_inanim, matrix_verbs = {}, {}, {}, {}
for tense in ['past', 'present', 'future', 'finite']:
    verbs[tense], verbs_intran_anim[tense], verbs_intran_inanim[tense], matrix_verbs[tense] = {}, {}, {}, {}

verbs['past'] = ['saw', 'stopped']
verbs['present']['singular'] = ['sees', 'stops']
verbs['present']['plural'] =  ['see', 'stop']
verbs['future'] = ['will see', 'will stop']
verbs['finite'] = verbs['present']['plural']

verbs_intran_anim['past'] = ['smiled', 'jumpped']
verbs_intran_anim['present']['singular'] = ['smiles', 'jumps']
verbs_intran_anim['present']['plural'] =  ['smile', 'jump']
verbs_intran_anim['future'] = ['will smile', 'will jump']

verbs_intran_inanim['past'] = ['fell', 'disappeared']
verbs_intran_inanim['present']['singular'] = ['falls', 'disappears']
verbs_intran_inanim['present']['plural'] =  ['fall', 'disappear']
verbs_intran_inanim['future'] = ['will fall', 'will disappear']

matrix_verbs['past'] = ['knew', 'remembered', 'said']
matrix_verbs['present']['singular'] = ['knows', 'remembers', 'says']
matrix_verbs['present']['plural'] =   ['know', 'remember' , 'say']
matrix_verbs['future'] = ['will know', 'will remember', 'will say']

copula = {}
copula['singular'] = ['is']
copula['plural'] = ['are']

##########################
###### PREPOSITIONS ######
##########################

# LOCATION PREPOSITIONS
# -----
# Tokens (second word will be used to choose the right article from determinats{} - 'a'/'definit'/)
loc_preps = ['near', 'behind', 'before', 'beside']


##########################
####### ADJECTIVES #######
##########################
adjectives = {}
#for gender in ['masculine', 'feminine']:
#    adjectives[gender] = {}
#adjectives['masculine']['singular'] = ['bello', 'famoso', 'brutto', 'ricco', 'povero', 'basso', 'alto', 'grasso', 'cattivo', 'buono', 'lento', 'nuovo']
#adjectives['masculine']['plural'] = ['belli', 'famosi', 'brutti', 'ricchi', 'poveri', 'bassi', 'alti', 'grassi', 'cattivi', 'buoni', 'lenti', 'nuovi']
#adjectives['feminine']['singular'] = ['bella', 'famosa', 'brutta', 'ricca', 'povera', 'bassa', 'alta', 'grassa', 'cattiva', 'buona', 'lenta', 'nuova']
#adjectives['feminine']['plural'] = ['belle', 'famose', 'brutte', 'ricche', 'povere', 'basse', 'alte', 'grasse', 'cattive', 'buone', 'lente', 'nuove']


Words = {
    'determinants':determinants.copy(),
    'pronouns':pronouns.copy(),
    'nouns':nouns.copy(),
    'nouns_inanimate':nouns_inanimate.copy(),
    'nouns_SC':nouns_SC.copy(),
    'location_nouns':location_nouns.copy(),
    'verbs':verbs.copy(),
    'verbs_intran_anim':verbs_intran_anim.copy(),
    'verbs_intran_inanim':verbs_intran_inanim.copy(),
    'copula':copula.copy(),
    'matrix_verbs':matrix_verbs.copy(),
    'loc_preps':loc_preps.copy(),
    'adjectives':adjectives.copy(),
    'quantifiers':quantifiers.copy(),
    'proper_names':proper_names.copy(),
    'anaphoras':anaphoras.copy()
    }

from nltk import CFG, ChartParser, FeatureChartParser
from nltk.grammar import FeatureGrammar

def parse_sents(sents_text, parser, verbose = True):
    """
    Method for parsing sentences
    sents_text - String of sentences, one sentence per line
    parser - to be used for parsing
    """
    sents = sents_text.splitlines()
    for sent in sents:
        parses = parser.parse(sent.split())
        parses_list = list(parses)
        if verbose:
            print(sent + '\nNum parses: ' + str(len(parses_list)) + '\n')
            for tree in parses_list:
                print(tree)
                print('\n')

# Steps 1 and 2 - lexicon and context-free rules
cfg = CFG.fromstring("""\
S -> SENT
SENT -> NP VP
S -> Wh-Conjunction SENT SENT
S -> Wh-Adverb Aux SENT
NP -> NP Conjunction NP | ProperNoun | Determiner Nominal | Nominal | NP PP
VP -> VERB | VERB NP | VERB NP NP | VERB SENT | VP PP
VERB -> Verb | Adverb Verb
Nominal -> Adjective Nominal | Nominal Noun | Noun
PP -> Preposition NP
ProperNoun -> 'Bart' | 'Homer' | 'Lisa'
Verb -> 'laughs' | 'laugh' | 'laughed' | 'drinks' | 'drink'| 'wears' | 'wear' | 'serves' | 'thinks'
Noun -> 'milk' | 'shoes' | 'salad' | 'kitchen' | 'midnight' | 'table'
Adjective -> 'blue' | 'healthy' | 'green'
Conjunction -> 'and' | 'or'
Wh-Conjunction -> 'when' | 'while'
Preposition -> 'in' | 'on' | 'before'
Determiner -> 'a' | 'the'
Adverb -> 'always' | 'never'
Wh-Adverb -> 'when' | 'why'
Aux -> 'do' | 'does'
""")

cfparser = ChartParser(cfg)

sents_text = """\
Bart laughs
Homer laughed
Bart and Lisa drink milk
Bart wears blue shoes
Lisa serves Bart a healthy green salad
Homer serves Lisa
Bart always drinks milk
Lisa thinks Homer thinks Bart drinks milk
Homer never drinks milk in the kitchen before midnight
when Homer drinks milk Bart laughs
when does Lisa drink the milk on the table
when do Lisa and Bart wear shoes
"""

# Step 3 Intermediate testing
print('STEP 3 PARSING WITH CONTEXT-FREE GRAMMAR')
parse_sents(sents_text, cfparser)

# Step 4 Unification grammar
ugrammar = FeatureGrammar.fromstring("""\
S -> SENT
SENT -> NP[NUM=sg] VP[SUBCAT=nil, FORM=vbz]
SENT -> NP[NUM=pl] VP[SUBCAT=nil, FORM=base]
SENT -> NP VP[SUBCAT=nil, FORM=pret]
S -> Wh-Conjunction SENT SENT
S -> Wh-Adverb Aux[FORM=vbz] NP[NUM=sg] VP[SUBCAT=nil, FORM=base]
S -> Wh-Adverb Aux[FORM=base] NP[NUM=pl] VP[SUBCAT=nil, FORM=base]
VP[SUBCAT=?rest, FORM=?form] -> VP[SUBCAT=[HEAD=?arg, TAIL=?rest], FORM=?form] ARG[CAT=?arg]
VP[SUBCAT=?args, FORM=?form] -> VP[SUBCAT=?args, FORM=?form] PP
VP[SUBCAT=?args, FORM=?form] -> V[SUBCAT=?args, FORM=?form]
V[SUBCAT=?args, FORM=?form] -> Adverb V[SUBCAT=?args, FORM=?form]
ARG[CAT=np] -> NP
ARG[CAT=pp] -> PP
ARG[CAT=sent] -> SENT
V[SUBCAT=nil, FORM=vbz] -> 'laughs'
V[SUBCAT=nil, FORM=base] -> 'laugh'
V[SUBCAT=nil, FORM=pret] -> 'laughed'
V[SUBCAT=[HEAD=np, TAIL=nil], FORM=vbz] -> 'drinks' | 'wears'
V[SUBCAT=[HEAD=np, TAIL=nil], FORM=base] -> 'drink' | 'wear'
V[SUBCAT=[HEAD=np, TAIL=[HEAD=np, TAIL=nil]], FORM=vbz] -> 'serves'
V[SUBCAT=[HEAD=np, TAIL=nil], FORM=vbz] -> 'serves'
V[SUBCAT=[HEAD=sent, TAIL=nil], FORM=vbz] -> 'thinks'
NP[NUM=pl] -> NP Conjunction NP
NP[NUM=?arg] -> ProperNoun[NUM=?arg] | Determiner Nominal[NUM=?arg] | Nominal[NUM=?arg] | NP[NUM=?arg] PP
Nominal[NUM=?arg] -> Adjective Nominal[NUM=?arg] | Nominal Noun[NUM=?arg] | Noun[NUM=?arg]
PP -> Preposition NP
ProperNoun[NUM=sg] -> 'Bart' | 'Homer' | 'Lisa'
Noun[NUM=sg] -> 'milk' | 'salad' | 'kitchen' | 'midnight' | 'table'
Noun[NUM=pl] -> 'shoes'
Adjective -> 'blue' | 'healthy' | 'green'
Conjunction -> 'and'
Wh-Conjunction -> 'when' | 'while'
Preposition -> 'in' | 'on' | 'before'
Determiner -> 'a' | 'the'
Adverb -> 'always' | 'never'
Wh-Adverb -> 'when' | 'what'
Aux[FORM=vbz] -> 'does'
Aux[FORM=base] -> 'do'
""")
uparser = FeatureChartParser(ugrammar)

# Step 5 final testing
sents_all_text = """\
Bart laughs
Homer laughed
Bart and Lisa drink milk
Bart wears blue shoes
Lisa serves Bart a healthy green salad
Homer serves Lisa
Bart always drinks milk
Lisa thinks Homer thinks Bart drinks milk
Homer never drinks milk in the kitchen before midnight
when Homer drinks milk Bart laughs
when does Lisa drink the milk on the table
when do Lisa and Bart wear shoes
Bart laugh
when do Homer drinks milk
Bart laughs the kitchen
"""

print('STEP 5 PARSING WITH UNIFICATION GRAMMAR')
parse_sents(sents_all_text, uparser)

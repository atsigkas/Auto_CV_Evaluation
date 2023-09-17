import editdistance
import fuzzy
import phonetics
from fuzzywuzzy import fuzz


def name_similarity(name1, name2):
    return editdistance.eval(fuzzy.nysiis(name1), fuzzy.nysiis(name2))


def name_similarity2(name1, name2):
    code1 = phonetics.metaphone(name1)
    code2 = phonetics.metaphone(name2)
    return fuzz.ratio(code1, code2)


print(name_similarity('Theologos Athanaselis', 'Dr THEOLOGOS ATHANASELIS'))
print(name_similarity2('Theologos Athanaselis', 'Dr THEOLOGOS ATHANASELIS'))
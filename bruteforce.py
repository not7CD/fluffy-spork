import Levenshtein as lv
import json

DEPARTAMENTS = json.loads(open('data/departaments.json').read())


def levenshtein(inpath=None, outpath=None, data=None, tags=None):
    best_ratio = None
    best_sentence = None
    best_departament = None
    for dep in DEPARTAMENTS['departaments']:
        dep_len = len(dep['departament-name'])
        for x in range(len(data) - dep_len):
            ratio = lv.ratio(
                data[x:x + dep_len],
                dep['departament-name']
            )
            if best_ratio is None or ratio.real > best_ratio:
                best_ratio = ratio.real
                best_sentence = data[x:x + dep_len]
                best_departament = dep
    try:
        print("SCORE: %s\n%s\n%s" % (best_ratio, best_sentence, best_departament['departament-name']))
    except TypeError as e:
        print("SCORE: %s\n%s\n%s\n%s" % (best_ratio, best_sentence, best_departament, e))
    return ({'data': {'score': best_ratio, 'sentence': best_sentence, 'match': best_departament}, 'path': inpath}, None)

import json
import Levenshtein as lv

DEPARTAMENTS = json.loads(open('data/departaments.json').read())
JOB_TITLES = json.loads(open('data/stanowiska.json').read())


def job_titles(inpath=None, outpath=None, data=None, tags=None):

    best_ratio = None
    best_sentence = None
    best_departament = None
    for elt in JOB_TITLES['job_titles']:
        # print('------\n%s %s' %  (i, dep['departament-name']))
        elt_len = len(elt)
        if elt_len > 4:
            if len(data) - elt_len < elt_len:
                ratio = lv.jaro(data.lower(), elt.lower())
                real_ratio = ratio.real + (elt_len * 0.001)
                if best_ratio is None or real_ratio > best_ratio:
                    best_ratio = real_ratio
                    best_sentence = data
                    best_match = elt
            # print(i, ratio, best_ratio, elt)
            for x in range(len(data) - elt_len):
                ratio = lv.jaro(data[x:x + elt_len].lower(), elt.lower())
                real_ratio = ratio.real + (elt_len * 0.004) - (x * 0.001)
                if best_ratio is None or real_ratio > best_ratio:
                    best_ratio = real_ratio
                    best_sentence = data[x:x + elt_len]
                    best_match = elt
                # print(ratio, best_ratio, elt)

    try:
        print("SCORE: %s\n%s\n%s" %
              (best_ratio, best_sentence, best_match))
    except TypeError as e:
        print("SCORE: %s\n%s\n%s\n%s" %
              (best_ratio, best_sentence, best_departament, e))
    return ({'data': {'score': best_ratio, 'sentence': best_sentence, 'match': best_match}}, None)


def levenshtein(inpath=None, outpath=None, data=None, tags=None):

    best_ratio = None
    best_sentence = None
    best_departament = None
    for i, dep in enumerate(DEPARTAMENTS['departaments']):
        # print('------\n%s %s' %  (i, dep['departament-name']))
        dep_len = len(dep['departament-name'])
        if dep_len > 5:
            if len(data) - dep_len < dep_len:
                ratio = lv.jaro(data.lower(), dep['departament-name'].lower())
                if best_ratio is None or ratio.real > best_ratio:
                    best_ratio = ratio.real
                    best_sentence = data
                    best_departament = dep
            # print(i, ratio, best_ratio, dep['departament-name'])
            for x in range(len(data) - dep_len):
                ratio = lv.jaro(
                    data[x:x + dep_len].lower(),
                    dep['departament-name'].lower()
                )
                if best_ratio is None or ratio.real > best_ratio:
                    best_ratio = ratio.real
                    best_sentence = data[x:x + dep_len]
                    best_departament = dep
                # print(i, ratio, best_ratio, dep['departament-name'])

    try:
        print("SCORE: %s\n%s\n%s" %
              (best_ratio, best_sentence, best_departament['departament-name']))
    except TypeError as e:
        print("SCORE: %s\n%s\n%s\n%s" %
              (best_ratio, best_sentence, best_departament, e))
    return ({'data': {'score': best_ratio, 'sentence': best_sentence, 'match': best_departament}}, None)

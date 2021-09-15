from collections import Counter
from itertools import groupby
import math
import numpy as np
# import pandas as pd 


# df = pd.read_csv('data_combined_get_splits_v1.csv')
# df = df.dropna(subset=['langtags'])


def calc(line, func):
    global NUMTAGS, LANG_TAGS, LANGS
    LANGS = ['en', 'hi']
    LANG_TAGS = [i for i in line]

    if not LANGS:
        LANGS = list(set(LANG_TAGS))
    else:
        LANG_TAGS = [lang for lang in LANG_TAGS if lang in LANGS]
    
    NUMTAGS = len(LANG_TAGS)

    func_map = {
                # 'metrics': metrics,
                'm_metric': m_metric,
                'i_metric': i_metric,
                'burstiness': burstiness,
                'memory': memory,
                'spans': spans,
                'span_summary': span_summary,
                'switchpoints': switchpoints,
                'lang_entropy': lang_entropy,
                'span_entropy': span_entropy,
                'switch_entropy': switch_entropy,
                'switch_surprisal': switch_surprisal,
                }

    return func_map[func]()



def metrics():
        num_switchpoints()
        m_metric()
        i_metric()
        burstiness()
        memory()
        lang_entropy()
        span_entropy()
        switch_entropy()
        switch_surprisal()


def num_switchpoints():
        num_switches = 0

        for index, tag in enumerate(LANG_TAGS[1:]):
                if tag != LANG_TAGS[index - 1]:
                        num_switches += 1

        # print("Number of switchpoints: {}".format(num_switches))
        return num_switches


def m_metric():
        num_langs = len(LANGS)
        counts = Counter(LANG_TAGS)
        m_metric = 0.0

        if num_langs == 1:
                # print("M-metric: {}".format(m_metric))
                return m_metric


        # Compute p_i^2 for all languages in text
        p_lang = {}
        for lang, count in counts.items():
                p_lang[lang] = (count / float(NUMTAGS)) ** 2

        p_sum = sum(p_lang.values())
        m_metric = (1 - p_sum) / ((num_langs - 1) * p_sum)

        # print("M-metric: {}".format(m_metric))
        return m_metric


def i_metric():
        # Count number of language switches for each language
        switches = {lang: {} for lang in LANGS}
        counts = Counter(zip(LANG_TAGS, LANG_TAGS[1:]))

        # Compute transition probabilities
        for (x, y), c in counts.items():
                switches[x][y] = c / float(NUMTAGS - 1)

        i_metric = 0.0

        # Sum all probabilities of switching language
        for lang1, switch in switches.items():
                for lang2, prob in switch.items():
                        if lang1 != lang2:
                                i_metric += prob

        # print("I-metric: {}".format(i_metric))
        return i_metric


def burstiness():
        spans = [len(list(group)) for lang, group in groupby(LANG_TAGS)]
        mean = np.mean(spans)
        sd = np.std(spans)
        burstiness = (sd - mean)/(sd + mean)

        # print("Burstiness: {}".format(burstiness))
        return burstiness


def memory():
        spans = [len(list(group)) for lang, group in groupby(LANG_TAGS)]
        mean1 = np.mean(spans[:-1])
        mean2 = np.mean(spans[1:])
        sd1 = np.std(spans[:-1])
        sd2 = np.std(spans[1:])
        memory = 0.0

        for i, span in enumerate(spans[:-1]):
                memory += (span - mean1) * (spans[i + 1] - mean2)

        memory /= (len(spans) - 1) * (sd1 * sd2)

        # print("Memory: {}".format(memory))
        return memory


def spans():
        spans = [(lang, len(list(group))) for lang, group in groupby(LANG_TAGS)]

        print("Lang\tLength")

        for lang, length in spans:
                print("{}\t{}".format(lang, length))


def span_summary():
        spans = sorted([(lang, len(list(group))) for lang, group in groupby(LANG_TAGS)])
        spans = sorted([(c, len(list(cgen))) for c, cgen in groupby(spans)])

        print("Lang\tSpanLength\tSpanFreq")

        for (lang, length), freq in spans:
                print("{}\t{}\t{}".format(lang, length, freq))


def switchpoints():
        switchpoints = []

        # Compute vector of switch indices
        for index, tag in enumerate(LANG_TAGS[:-1]):
                if tag != LANG_TAGS[index + 1]:
                        switchpoints.append(index + 1)
                else:
                        switchpoints.append(0)

        for switch in switchpoints:
                # print("{}".format(switch))
                return switch


def lang_entropy():
        # Count frequencies of language tokens
        counts = Counter(LANG_TAGS)

        # Compute entropy based on unigram language tokens
        lang_entropy = 0.0
        for lang, count in counts.items():
                lang_prob = count / float(NUMTAGS)
                lang_entropy -= lang_prob * math.log2(lang_prob)

        # print("Language Entropy: {}".format(lang_entropy))
        return lang_entropy


def span_entropy():
        # Get frequencies of language spans
        spans = [len(list(group)) for lang, group in groupby(LANG_TAGS)]
        span_counts = Counter(spans)
        total_count = len(spans)

        # Compute entropy based on spans of language tokens
        span_entropy = 0.0
        for length, count in span_counts.items():
                span_prob = count / float(total_count)
                span_entropy -= span_prob * math.log2(span_prob)

        # print("Span Entropy: {}".format(span_entropy))
        return span_entropy


def switch_entropy():
        switches = 0

        # Compute vector of switch indices
        for index, tag in enumerate(LANG_TAGS[:-1]):
                if tag != LANG_TAGS[index + 1]:
                        switches += 1

        switches = switches / (NUMTAGS - 1)
        switches = - switches * math.log2(switches)

        # print("Switch Entropy: {}".format(switches))
        return switches


def switch_surprisal():
        surprisal = 0

        # Compute vector of switch indices
        for index, tag in enumerate(LANG_TAGS[:-1]):
                if tag != LANG_TAGS[index + 1]:
                        surprisal += 1

        surprisal = surprisal / (NUMTAGS - 1)
        surprisal = math.log2(1 / surprisal)

        # print("Switch Surprisal: {}".format(surprisal))
        return surprisal


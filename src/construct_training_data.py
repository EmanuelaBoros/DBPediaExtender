#!/usr/bin/env python
import sys
from itertools import izip
from collections import defaultdict
from random import shuffle

from config import tests_path
from sparql_access import select_all, select_entities_of_type_in_relation
from sentence_classifier import SentenceClassifier
from article_access import get_article, prepare_articles
from language_tools import LanguageToolsFactory

if __name__ == '__main__':
    lt = LanguageToolsFactory.get_language_tools()
    predicate = 'stolica'
    test_data_limit = 1000
    entities_f = open(tests_path + '%s/entities' % predicate, 'w')
    values_f = open(tests_path + '%s/values' % predicate, 'w')
    names = select_all({'p': predicate})
    shuffle(names)
    names = names[: test_data_limit]
    subjects, objects = zip(*list(names))
    values = defaultdict(list)
    for subject, value in names:
        values[subject].append(value)
    prepare_articles(subjects)
    for subject, value in values.iteritems():
        try:
            article = get_article(subject)
        except:
            continue
        print subject, lt.prepare_value(value[0], predicate)
        for sentence in article:
            sentence = [word.segment for word in sentence]
            print ' '.join(sentence)
        print
        print >>entities_f, subject
        print >>values_f, subject


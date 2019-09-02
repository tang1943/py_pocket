# coding: utf-8

import re

__resentencesp = re.compile('([﹒﹔﹖﹗．；。！？]["’”」』]{0,2}|：(?=["‘“「『]{1,2}|$))')


def split_sentence(sentence):
    """
    cut paragraph to sentence for Chinese
    copy from https://github.com/fxsjy/jieba/issues/575
    :param sentence: text
    :return: list of sentence
    """
    s = sentence
    slist = []
    for i in __resentencesp.split(s):
        if __resentencesp.match(i) and slist:
            slist[-1] += i
        elif i:
            slist.append(i)
    return slist

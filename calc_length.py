# -*- coding: utf-8 -*-

"""
   Created on 27/04/2015
   @author: C&C - HardSoft
"""

from util.HOFs import *
from util.CobolPatterns import *
from util.homogenize import homogenize

def calc_length(copy):
    if isinstance(copy, list):
        book = copy
    else:
        if isinstance(copy, str):
            book = copy.splitlines()
        else:
            book = []

    lines = homogenize(book)

    havecopy = filter(isCopy, lines)
    if havecopy:
        bkm = ''.join(havecopy[0].split('COPY')[1].replace('.', '').split())
        msg = 'COPY {} deve ser expandido.'.format(bkm)
        return {'retorno': False, 'msg': msg, 'lrecl': 0}

    lrecl = 0
    redefines = False
    occurs = False
    locc = 0
    lvlred = 0
    lvlocc = 0

    for line in lines:
        match = CobolPatterns.row_pattern.match(line.strip())
        if not match:
            continue
        match = match.groupdict()

        if not match['level']:
            continue

        level = int(match['level'])

        if redefines:
            if level > lvlred:
                continue
        redefines = False
        lvlred = 0

        if match['redefines']:
            lvlred = level
            redefines = True
            continue

        if occurs:
            if level > lvlocc:
                if match['pic']:
                    locc += lenfield(match['pic'], match['usage'])
                continue
            lrecl += locc * occurs
        occurs = False
        lvlocc = 0

        if match['occurs']:
            lvlocc = level
            occurs = (int(nextWord('OCCURS', line)) if 'TO' not in wrds else
                      int(nextWord('TO', line)))

        if match['pic']:
            if occurs:
                locc += lenfield(match['pic'], match['usage'])
            else:
                lrecl += lenfield(match['pic'], match['usage'])

    return {'retorno': True, 'msg': None, 'lrecl': lrecl}


def lenfield(pic_str, usage):
    if pic_str[0] == 'S':
        pic_str = pic_str[1:]

    while True:
        match = CobolPatterns.pic_pattern_repeats.search(pic_str)

        if  not match:
            break

        expanded_str = match.group(1) * int(match.group(2))
        pic_str = CobolPatterns.pic_pattern_repeats.sub(expanded_str, pic_str, 1)

    lentmp = len(pic_str.replace('V', ''))

    if not usage:
        usage = 'DISPLAY'

    if 'COMP-3' in usage or 'COMPUTATIONAL-3' in usage:
        lrecl = lentmp / 2 + 1
    elif 'COMP' in usage or 'COMPUTATIONAL' in usage or 'BINARY' in usage:
        lrecl = lentmp / 2
    elif 'SIGN' in usage:
        lrecl = lentmp + 1
    else:
        lrecl = lentmp

    return lrecl


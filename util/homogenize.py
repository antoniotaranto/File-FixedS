# -*- coding: utf-8 -*-

'''
   Created on 25/05/2015
   @author: C&C - HardSoft
'''

from HOFs import *
def homogenize(book):
    clearLines = map(l672, filter(all3(isNotRem, isNotBlank, isNotEjectOrSkip), book))
    joinLines = []
    holder = []
    for l in clearLines:
        holder.append(l if not holder else l.strip())
        if l.endswith('.'):
            joinLines.append(" ".join(holder))
            holder = []
    return joinLines

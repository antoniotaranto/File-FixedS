# -*- coding: utf-8 -*-

import json
from collections import namedtuple
from Exceptions import FieldLengthOverflow


__author__ = 'flavio@casacurta.com'


class Fixed_files(object):

    def __init__(self, filejson, obj=False, dic=False, checklength=False):

        self.dic = dic
        self.checklength = checklength

        try:
            if obj:
                self.lattrs = filejson
            else:
                filejson = filejson if filejson.endswith('.json') else '{}.json'.format(filejson)
                attrs = open(filejson).readlines()
                self.lattrs = [json.loads(line.decode('utf-8')) for line in attrs]
        except:
            self.lattrs = []

        self.attr = [att['field'] for att in self.lattrs]

        start = 0
        for att in self.lattrs:
            if att['sign']:
                att['length'] = att['length'] + 1
            exec ("self.{} = slice({}, {})".format(att['field'], start, (start + att['length'])))
            start += att['length']

        self.slices = ''
        for att in self.lattrs:
            if att['type'] == 'str':
                self.slices += 'record[self.{}], '.format(att['field'])
            elif att['type'] == 'int':
                if att['decimals']:
                    self.slices += 'round('
                if att['sign']:
                    self.slices += "int(record[self.{0}][:-1])*int(record[self.{0}][-1]+{1})".format(
                         att['field'], "'1'")
                else:
                    self.slices += 'int(record[self.{}])'.format(att['field'])
                if att['decimals']:
                    self.slices += ' * .{0:>0{1}}, {1})'.format('1', att['decimals'])
                self.slices += ', '

        fmt_out_str = ''
        fmt_out_fmt = ''
        for att in self.lattrs:
            if att['sign']:
                att['length'] = str(int(att['length']) - 1)
            if att['type'] == 'str':
                fmt_out_str += "{}".format('{:<' + str(att['length']) + '}')
                if self.dic:
                    fmt_out_fmt += 'record["{}"][:{}], '.format(att['field'], att['length'])
                else:
                    fmt_out_fmt += 'record.{}[:{}], '.format(att['field'], att['length'])
            elif att['type'] == 'int':
                if att['decimals']:
                    dec = ' * {}'.format(int('{:<0{}}'.format('1', att['decimals']+1)))
                else:
                    dec = ''
                if att['sign']:
                    fmt_out_str += '{}'.format('{:>0' + str(att['length']) + '}{}')
                else:
                    fmt_out_str += '{}'.format('{:>0' + str(att['length']) + '}')
                if self.dic:
                    if att['sign']:
                        fmt_out_fmt += '''str(int(round(record["{0}"]{1}, 0) * -1))[:{2}]
                                          if record["{0}"] < 0
                                          else str(int(round(record["{0}"]{1}, 0)))[:{2}],
                                          '-' if record["{0}"] < 0 else '+'
                                       '''.format(att['field'],
                                                  dec,
                                                  att['length'])
                    else:
                        fmt_out_fmt += 'str(int(round(record["{}"]{}, 0)))[:{}]'.format(att['field'],
                                                                              dec,
                                                                              att['length'])
                else:
                    if att['sign']:
                        fmt_out_fmt += '''str(int(round(record.{0}{1}, 0) * -1))[:{2}]
                                          if record.{0} < 0
                                          else str(int(round(record.{0}{1}, 0)))[:{2}],
                                          '-' if record.{0} < 0 else '+'
                                       '''.format(att['field'],
                                                  dec,
                                                  att['length'])
                    else:
                        fmt_out_fmt += 'str(int(round(record.{}{}, 0)))[:{}]'.format(att['field'],
                                                                           dec,
                                                                           att['length'])
                fmt_out_fmt += ', '

        self.fmt_out = "'" + fmt_out_str + "\\n'.format(" + fmt_out_fmt + ")"

        self.Record = namedtuple('Record', self.attr)


    def parse(self, record):

        nt = eval("self.Record({})".format(self.slices))

        if self.dic:
            return {k:nt[n] for n, k in enumerate(self.attr)}

        return nt


    def unparse(self, record):

        return eval("{}".format(self.fmt_out))

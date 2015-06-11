# -*- coding: utf-8 -*-

dicAttrSql = {'COMP2'    : 'SMALLINT'
             ,'COMP4'    : 'INTEGER'
             ,'COMP8'    : 'DOUBLE'
             ,'COMP-3'   : 'DECIMAL('
             ,'DISPLAYX' : 'CHAR('
             ,'OUTROS'   : 'CHAR('
             ,'DISPLAY9' : 'DECIMAL('}

dicAttrJson = {'COMP2'    : ['int', '4', '0', True]
              ,'COMP4'    : ['int', '9', '0', True]
              ,'COMP8'    : ['int', '18', '0', True]
              ,'COMP-3'   : ['int', '0', '0', None]
              ,'DISPLAYX' : ['str', '0', '0', None]
              ,'OUTROS'   : ['str', '0', '0', None]
              ,'DISPLAY9' : ['int', '0', '0', None]}

class Attribute(object):

    def __init__(self, lenVar=20):
        self.lenVar = lenVar

### Atributos SQL

    def attributeSql(self, pic, usage=None, occurs=None):

        usage = 'DISPLAY' if not usage else usage
        decimals = 0

# Determina a natureza Alpha ou Numerica
        if  pic[0] == 'S':
            pic = pic[1:]
        pic0 = pic[0] if not occurs else 'X'

# Determina se a picture tem parenteses
        pap = pic.find('(')

# determina length dos integers e decimals SEM parenteses
        if  pap == -1:
            if  'V' in pic:
                integers = pic.index('V')
                decimals = len(pic)-(pic.index('V')+1)
            else:
                integers = len(pic)
# determina length dos integers e decimals COM parenteses
        else:
            if  'V' in pic:
                intTmp = pic[:pic.index('V')]
                decTmp = pic[pic.index('V')+1:]
                if  '('  in intTmp:
                    integers = int(intTmp[intTmp.index('(')+1:intTmp.index(')')])
                else:
                    integers = len(intTmp)
                if  '('  in decTmp:
                    decimals = int(decTmp[decTmp.index('(')+1:decTmp.index(')')])
                else:
                    decimals = len(decTmp)
            else:
                integers = int(pic[pap+1:pic.index(')')])

        length = integers + decimals

        if  occurs:
            for o in occurs.split():
                if o.isdigit():
                    occ = int(o)
                    break
            usage = 'DISPLAY'
            length = length * occ
            decimals = 0

        comma        = ','
        if  decimals == 0:
            decimals = ''
            comma    = ''

        var          = ''
        if  length  > self.lenVar and usage == 'DISPLAY' and pic0 == 'X':
            var      = 'VAR'

        if  usage == 'COMP':
            return dicAttrSql[usage + str(length / 2 )]

        length      = str(length)
        decimals     = str(decimals)

        if  usage in dicAttrSql:
            return dicAttrSql[usage] + length + comma + decimals +')'
        if  usage + pic0 in dicAttrSql:
            return var + dicAttrSql[usage + pic0] + length + comma + decimals + ')'
        return dicAttrSql['OUTROS'] + length + comma + decimals + ')'

### Atributos COBOL

    def attributeCob(self, col):

        pic = 'S9' if col.datatypes.picture_cobol == '9' else ' X'

        lenCol = str(col.colunas.lengthColuna - col.colunas.decimals)

        comma = ('' if col.datatypes.picture_cobol == 'X' else
                 'V' if not col.colunas.decimals else
                 'V9({})'.format(col.colunas.decimals))

        usage = ('.' if col.datatypes.usage_cobol == 'DISPLAY'
                     else ' USAGE {}.'.format(col.datatypes.usage_cobol))

        return '{}({}){}{}'.format(pic, lenCol, comma, usage)


### Atributos JSON

    def attribute_json(self, pic, usage=None, occurs=None, signal=True):

        usage = 'DISPLAY' if not usage else usage
        decimals = 0

# Determina a natureza Alpha ou Numerica
        sign = False
        if  pic[0] == 'S':
            sign = signal
            pic = pic[1:]
        pic0 = pic[0] if not occurs else 'X'

# Determina se a picture tem parenteses
        pap = pic.find('(')

# determina length dos integers e decimals SEM parenteses
        if  pap == -1:
            if  'V' in pic:
                integers = pic.index('V')
                decimals = len(pic)-(pic.index('V')+1)
            else:
                integers = len(pic)
# determina length dos integers e decimals COM parenteses
        else:
            if  'V' in pic:
                intTmp = pic[:pic.index('V')]
                decTmp = pic[pic.index('V')+1:]
                if  '('  in intTmp:
                    integers = int(intTmp[intTmp.index('(')+1:intTmp.index(')')])
                else:
                    integers = len(intTmp)
                if  '('  in decTmp:
                    decimals = int(decTmp[decTmp.index('(')+1:decTmp.index(')')])
                else:
                    decimals = len(decTmp)
            else:
                integers = int(pic[pap+1:pic.index(')')])

        length = integers + decimals

        if occurs:
            for o in occurs.split():
                if o.isdigit():
                    occ = int(o)
                    break
            usage = 'DISPLAY'
            length = length * occ
            decimals = 0

        if usage == 'COMP':
            usage = usage + str(length / 2 )

        if usage == 'COMP-3':
            dicAttrJson[usage][1] = str(length)
            dicAttrJson[usage][2] = str(decimals)
            dicAttrJson[usage][3] = sign

        if usage in dicAttrJson:
            return dicAttrJson[usage]

        if usage + pic0 in dicAttrJson:
            return [dicAttrJson[usage + pic0][0], str(length), str(decimals), sign]
        return [dicAttrJson['OUTROS'][0], str(length), str(decimals), sign]


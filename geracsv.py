import os
import sys
import traceback
import re
import json
from columns import Columns
from fixed_files import Fixed_files

def geracsv(book, records, arq, signal):
    try:
        basename = os.path.basename(book).split('.')[0]
        col = Columns()
        js = col.columns(book, signal=signal)
        fj = [json.loads(line.decode('utf-8')) for line in js]
        ff = Fixed_files(fj, obj=True)
        rec_in = []
        for record in records:
            rec_in.append(ff.parse(record))

        flds = [str(att['field']) for att in fj]
        csvs = ';'.join(str(flds)[1:-1].upper().replace(basename + '_','').replace("'","").split(',')) + '\n'
        csvs = re.sub('FILLER_..', 'FILLER', csvs)

        fmt = '''"{}"'''.format(str(['{' + f + '}' for f in flds])[1:-1]).replace("'","").replace(',',';')
        fmt += ".format(**r)"

        for r in rec_in:
            for n, f in enumerate(r):
                csvs += r[n] +';'
            csvs += '\n'

        outcsv = arq.split('.')[0] + '.csv'
        out = open(outcsv, 'w')
        out.write(csvs)
        out.close()
        return (True, outcsv)
    except:
        return (False, traceback.format_exc(sys.exc_info))

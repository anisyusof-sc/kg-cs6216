import os
import pandas as pd
import tempfile
import re

class Log2DatasetConverter():
    
    def __init__(self, filename, retrieve_size=-1) -> None:
        self.filename = filename
        self.filepath = os.path.join(os.getcwd(), filename)
        self.result = []
        self.tempfilepath = None
        self.retrieve_size = retrieve_size

    def convert(self):
        self._resolve_format_issues()

        if self.tempfilepath is None:
            print('Error: Format issue resolving failed')
            return

        print('[{}] Generating triples. This may take long time...'.format(self.filename))

        df = pd.read_table(self.tempfilepath)
        if self.retrieve_size > 0:
            df = df[0:self.retrieve_size]

        for _, row in df.iterrows():
            for k in row.keys():
                if k != 'uid' and row[k] != '-':
                    self.result.append((row['uid'], k, row[k]))
        
        print('OK')

    def _resolve_format_issues(self):
        print('[{}] Resolving format issues...'.format(self.filename))

        tempfilefd, self.tempfilepath = tempfile.mkstemp()
        
        tmpfp = os.fdopen(tempfilefd, 'w+')

        with open(self.filepath, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
            
                # line starts with '#': fields or ignore
                if line.startswith('#'):
                    if line.startswith('#fields'):
                        line = line[8:]
                    else:
                        continue
                
                # line contains 4 spaces rather than tab
                line = re.sub(r'([ ]+)', '\t', line)

                # write to temp file
                tmpfp.write(line + '\n')

        tmpfp.close()
        print('OK')

    def save(self, filename):
        outfilepath = os.path.join(os.getcwd(), filename)
        with open(outfilepath, 'w') as f:
            f.writelines([','.join(map(str, t)) + '\n' for t in self.result])
        print('[{}] Converted file saved to {}'.format(self.filename, outfilepath))

        os.unlink(self.tempfilepath)

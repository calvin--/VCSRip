from http import HTTP

class RipperSVNOLD(object):
    def __init__(self, vulnerability):
        self.vulnerability = vulnerability
        self.host = vulnerability['host']
        self.session = HTTP()
        self.output_folder = "output/{}/".format(self.host.host)

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
                    self.output_folder + directory + "/" + entries[x-1]
                )

    def download_file(self, url, dest):
        if self.session.get_file(url, dest):
            print "Fetched " + str(url)
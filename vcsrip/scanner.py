from http import HTTP
from yurl import URL

class Scanner(object):

    FINGERPRINTS = [
        {
            "type": "git",
            "base": ".git",
            "files": ["index"]
        },
        {
            "type": "svn",
            "base": ".svn",
            "files": ["wc.db"]
        },
        {
            "type": "svn_old",
            "base": ".svn",
            "files": ["entries"]
        },
        #{
        #    "type": "hg",
        #    "base": ".hg",
        #    "files": ["store/00manifest.i"]
        #}
    ]

    SCHEMES = ["HTTP", "HTTPS"]

    def __init__(self, host):
        self.host = URL(host).replace(path = "", query = "", fragment = "")
        self.session = HTTP()
        self.session.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"

    def scan_host(self):
        for scheme in self.SCHEMES:
            for fingerprint in self.FINGERPRINTS:
                for file in fingerprint['files']:
                    url = self.host.replace(path = fingerprint['base'] + "/" + file, scheme = scheme)
                    url = str(url)

                    response = self.session.get(url, verify=False)

                    if response.status_code == 200 and self._filter_false_positive(response.content, fingerprint['type']):
                        return {
                                "file": file,
                                "type": fingerprint['type'],
                                "scheme": scheme,
                                "data": response.content,
                                "host": self.host.replace(scheme = scheme)
                        }
                    else:
                        pass
                        if(response.status_code == 200):
                            pass
                            #print "Failed: File exists, but failed verification."
                        else:
                            pass
                            #print "Failed: HTTP " + str(response.status_code)

        return False

    def _filter_false_positive(self, data, type):
        if "<html" in data and "</html>" in data:
            return False

        if type == "git":
            if data[0:4] != "DIRC":
                return False

        if type == "svn_old":
            if "dir" not in data or "file" not in data:
                return False

        if type == "svn":
            if data[0:13] != "SQLite format":
                return False

        if type == "hg":
            if not data.statswith(".hgtag"):
                return False

        return True

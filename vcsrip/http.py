from requests import Session, packages
import logging
import os
import sys

logging.getLogger("requests").setLevel(logging.WARNING)
packages.urllib3.disable_warnings()

class HTTP(Session):
    def __init__(self, *args, **kwargs):
        super(HTTP, self).__init__(*args, **kwargs)

        #TODO: Allow for custom user-agent
        self.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 " \
                                             "(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"


    def get_file(self, url, dest, with_data = None):
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))

        with open(dest, "wb") as f:
            if not with_data:
                response = self.get(url, stream=True, timeout=2)

                if response.status_code != 200:
                    return False

                written = 0

                for block in response.iter_content(1024):
                    written += 1024
                    f.write(block)

                logging.debug("Wrote {} to file {}".format(self.readable_size(written), dest))
            else:
                f.write(with_data)

        return True

    def readable_size(self, num, suffix='B'):
        for unit in ['','K','M','G','T','P','E','Z']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)
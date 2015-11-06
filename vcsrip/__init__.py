import argparse
import logging

from scanner import Scanner
from RipperGIT import RipperGIT
from RipperSVN import RipperSVN
from RipperSVNOLD import RipperSVNOLD

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("url", help="url to target site")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                         action="store_true")
    parser.add_argument("--git-download-pack", help="attempt to download git pack files",
                         action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    scanner = Scanner(args.url)
    vulnerability = scanner.scan_host()

    if vulnerability:
        if vulnerability['type'] == 'git':
            logging.info("Attempting to download public git repository.")
            git = RipperGIT(vulnerability)

            logging.info("Downloading git meta files.")
            git.get_meta_files()

            if args.git_download_pack:
                logging.info("Attempting to download git pack files.")
                git.get_pack_files()

            logging.info("Downloading git objects.")
            git.get_objects()

            logging.info("Unpacking git objects")
            git.unpack_objects()

            logging.info("Done.")

        elif vulnerability['type'] == 'svn':
            svn = RipperSVN(vulnerability)
            svn.parse_wc()

        elif vulnerability['type'] == 'svn_old':
            svn = RipperSVNOLD(vulnerability)
            svn.parse_entries()

        elif vulnerability['type'] == "hg":
            raise NotImplementedError("TODO")
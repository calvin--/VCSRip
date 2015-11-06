import struct
import binascii

def parse_index(index_file):
    f = open(index_file, "rb")

    def read(format):
        format = "! " + format
        bytes = f.read(struct.calcsize(format))
        return struct.unpack(format, bytes)[0]

    index = {}
    entries = []

    index["signature"] = f.read(4).decode("ascii")
    index["version"] = read("I")

    for e in range(read("I")):
        entry = {}

        f.seek(40, 1)
        entry["sha1"] = binascii.hexlify(f.read(20)).decode("ascii")
        entry["flags"] = read("H")

        entry["extended"] = bool(entry["flags"] & (0b01000000 << 8))
        namelen = entry["flags"] & 0xFFF

        entry_length = 62

        if entry["extended"] and (index["version"] == 3):
            f.seek(2, 1)
            entry_length += 2


        if namelen < 0xFFF:
            entry["name"] = f.read(namelen).decode("utf-8", "replace")
            entry_length += namelen
        else:
            name = []
            while True:
                byte = f.read(1)
                if byte == "\x00":
                    break
                name.append(byte)
            entry["name"] = b"".join(name).decode("utf-8", "replace")
            entry_length += 1

        padding = (8 - (entry_length % 8)) or 8
        f.seek(padding, 1)

        entries.append(
            {
                "name": entry["name"],
                "sha1": entry["sha1"]
            })

    return entries
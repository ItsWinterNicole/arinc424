from .record import Record, Arinc424Decoder
from .containers import Collection
import os

def parse(line):
    """
    Parse an ARINC-424 record and convert the
    contents to a record or record group
    instance..
    """
    r = Record.from_line(line)
    if r.read():
        # IF you really must print the decoded record.
        # Arinc424Decoder(rec.read()).decode()
        allrecs.append(r)
        return True
    return False

def search(file, filters):
    """
    Search an ARINC-424 file and find all the
    records that contain given substrings.
    """
    with open(file) as f:
        count = 0
        for line in f.readlines():
            r = Record()
            if r.read(line) is False:
                continue
            if isinstance(filters, str):
                if filters not in r.raw:
                    continue
            elif isinstance(filters, list):
                if all(map(r.raw.__contains__, filters)) is False:
                    continue
            count = count + 1
        print(f"Found {count} records that contain {filters}")


def read_file(path):
    """
    Parse all ARINC-424 records within a file.
    """
    allrecs = Collection()
    with open(path) as f:
        for line in f.readlines():
            parse(line)
            print(line[123:128])
    print (f"Allrecs has {len(allrecs)} items")
    print (f"Found {len(allrecs.barerec)} solo records,")
    print (f"{len(allrecs.recgroups)} record groups,")
    print (f"{len(allrecs.boundaryrecseqs)} boundary seqs and")
    print (f"{len(allrecs.recseqs)} other sequences.")
    return allrecs

def read_folder(path):
    """
    Parse all ARINC-424 records for every file in a given folder.
    """
    fldr_recs = Collection()
    for file in os.scandir(path):
        fldr_recs.extend(read_file(os.path.join(path, file.name)))
    return fldr_recs

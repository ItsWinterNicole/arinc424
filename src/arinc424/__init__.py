from termcolor import colored
from .record import Record, MultiRecord, SeqType
from .record import Arinc424Decoder
from .containers import RecGroup, SeqGroup, Collection
import os

allrecs = Collection()
def parse(line):
    """
    Parse an ARINC-424 record and convertthe
    contents to a record or record group
    instance..
    """
    r = Record.from_line(line)
    if r.read():
        #print ("Read completed on:")
        #print (line)
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
            #print(r.raw)
            count = count + 1
        print(colored(f"Found {count} records that contain {filters}", 'green' if count else 'red'))


def read_file(path):
    """
    Parse all ARINC-424 records within a file.
    """
    allrecs.clear()
    with open(path) as f:
        for line in f.readlines():
            #print()
            parse(line)
            print(line[123:128])
    # PRINT: The next two lines are the parts that print everything out!!!
    #for rec in allrecs:
    #    Arinc424Decoder(rec.read()).decode()
        pass
    print (f"Allrecs has {len(allrecs)} items")
    print (f"Found {len(allrecs.barerec)} solo records,")
    print (f"{len(allrecs.recgroups)} record groups, and")
    print (f"{len(allrecs.recseqs)} sequences.")
    return allrecs

def read_folder(path):
    """
    Parse all ARINC-424 records for every file in a given folder.
    """
    frec = []
    fgr = []
    for file in os.scandir(path):
        (x, y) = read_file(os.path.join(path, file.name))
        frec.extend(x)
        fgr.extend(y)
    return (frec, fgr)

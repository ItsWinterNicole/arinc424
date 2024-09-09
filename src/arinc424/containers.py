from .record import Record, MultiRecord, SeqType
from collections import UserList
# TODO Might want this later for searching & returning items from
# containers according to enum'd types.  But we don't use it currently.
#from arinc424.decoder import Field

# TODO self.barerec, self.recgroups, self.recseqs, clear and all the work
# in parse() to build them, could probably all be done in
# the containers sub-lib.  Just pass it a rec & let it 
# build all the containers and give them back when we run out of
# records.
class Collection(UserList):
    def __init__(self, arg = None):
        self.data = []
        self.barerec = []
        self.recgroups = []
        self.recseqs = []
        self.lastrecgroup = None
        self.lastseqgroup = None
        
    def append(self, nr):

    def extend(self, iter):
        for i in iter:
            self.append(i)

    def clear(self):
        self.data.clear()
        self.barerec.clear()
        self.recgroups.clear()
        self.recseqs.clear()
        self.lastrecgroup = None
        self.lastseqgroup = None

# For organizational purposes we need to return some values so the
# higher levels of code can pass a record & get back... something..
# that will tell it what to do with that record:
#   1. Keep it as a stand alone record.
#   2. Drop it as part of an already seen record group or sequence.
#   3. Drop it and pick up a new record, or new sequence it's been added to.
# At the end this will give us one list with a set of records, record groups,
# and sequences.  All of which will be similarly processed by whatever the
# higher  code wants to do.

    def try_rg_add(self, r):
        # try group add:
        rnf = True
        m = None
        #print("Looking for rg")
        for group in self.recgroups:
            if group.validate(r):
                #print("Found rg")
                m = group
                group.append(r)
                rnf = False
                r.rec_group = group
                break
        if rnf:
            #print("Not found, trying new rg")
            # Must be a new record group.
            try:
                new_rg = RecGroup()
                new_rg.append(r)
                self.recgroups.append(new_rg)
                r.rec_group = new_rg
                m = new_rg
                #print("completd new rg!")
            except:
                #print("Failed new rg.. adding to regular records")
                self.barerec.append(r)
                m = r
            # Now try adding to a seq, cuz it could still be
            # a seq too...
            #print ("trying seq add from rec_add")
            try_seq_add(m)
        #print('try_rg_add done')

    def try_seq_add(self, r):
        # Try seq add:
        snf = True
        if isinstance(r, SeqType) is not True:
            #print("Not a sequencable record")
            return
        #print("Looking for seq")
        for seq in self.recseqs:
            if seq.validate(r):
                #print("Found seq")
                seq.append(r)
                snf = False
                break
        if snf:
            #print("Not found, trying new seq")
            try:
                #print("A")
                new_sg = SeqGroup()
                #print("B")
                new_sg.append(r)
                #print("C")
                self.recseqs.append(new_sg)
                #print("completd new seq!")
            except Exception as e:
                #print(f"{e}") # DEBUG
                # It's not part of a seq, but it will already be part of
                # either a group, or the solo list.  Nothing to do here.
                print("Unexpected new seq fail.")
        #print('try_seq_add done')

def _getmatchval(x, *args):
    # Return a tuple that is easy to use later for comparison.
    xprime = ''
    for r in args:
        xprime += x[r.start:r.stop]
    return (xprime, args)

def _checkmatch(xmatch, y):
    ymatch = _getmatchval(y, *(xmatch[1]))
    if (xmatch == ymatch):
        return True
    return False
    
class RecGroup(UserList):
    def __init__(self, arg = None):
        self.data = []
        if (arg is not None):
            for rec in arg:
                self.append(rec)
        
    def validate(self, nr):
        # NR is the new rec to validate.
        if ((isinstance(nr, MultiRecord) is False)
            or (nr.cont_no == 0)
            or ((self.data != [])
                and (_checkmatch(self.rec_matchstr, nr.line) is False))):
            return False
        return True

    def __setitem__(self, idx, nr):
        #print (f"s: {self.data}")
        if self.validate(nr):
            if (self.data == []):
                self.rec_matchstr = _getmatchval(nr.line, *nr.cont_cmprange)
                #print(f"ms: {self.matchstr}")
            if ((self.data == []) or (idx == 0)):
                self.line = nr.line
            while (len(self.data) < idx):
                self.data.append(None)
            if(idx >= len(self.data)):
                self.data.append(nr)
            else:
                self.data[idx] = nr
            nr.rec_group = self
            if (isinstance(nr, SeqType) and (idx == 0)):
                self.seq_no = nr.seq_no
                self.seq_cmprange = nr.seq_cmprange
                self.seq_no_pos = nr.seq_no_pos
        else:
            raise (ValueError("Not a valid item for this group"))
        #print (f"s2: {self.data}")

    def insert(self, idx, nr):
        #print("i")
        if (isinstance(nr, MultiRecord)):
            self[idx] = nr

    def append(self, nr):
        #print("a")
        if (isinstance(nr, MultiRecord)):
            self[nr.cont_no - 1] = nr
   
    def read(self):
        rl = []
        for r in self.data:
            rl.extend(r.read())
        return rl

class SeqGroup(UserList):
    def __init__(self, arg = None):
        self.data = []
        if (arg is not None):
            self.extend(arg)
        
    def validate(self, nr):
        # First test: make sure the record type is right and if it's part of 
        # a group, that we have the full group, not a single rec out of that
        # group.
        if ((isinstance(nr, MultiRecord) and (nr.cont_no != 0))
            or (isinstance(nr, RecGroup) 
                and ((nr == []) or (isinstance(nr[0], SeqType) is False)))
            or (isinstance(nr, Record) and (isinstance(nr, SeqType) is False))):
            return False
        # Second test: Confirm two things:
        #   1) nr is a match for whatever other records we have in this seq..
        #      ie. same sec/subsec, same route, boundary, Apch etc. 
        #   2) nr is not a seq no that is already present in the list.
        if ((self.data != [])
            and ((_checkmatch(self.seq_matchstr, nr.line) is False)
                 or (nr.seq_no in self.seq_nos))):
            return False
        return True

    """ Maybe __setitem__ and insert shouldn't be implemented. 
    def __setitem__(self, idx, nr):
        # We'll ignore the index, cuz we want things ordered by seq no.
        #print (f"s: {self.data}")
        if self.validate(nr):
            if (self.data == []):
                self.seq_matchstr = _getmatchval(nr.line, *nr.seq_cmprange)
            self.data.__setitem__(idx, nr)
            self.data.sort(key=SeqType.get_seq_no)
    """
    
    """ This isn't necessarily the best way either.
    __setitem__ = None
    insert = None
    reverse = None
    """

    # I've seen this done...
    __setitem__ = property()
    insert = property()
    reverse = property()

    def append(self, item):
        if self.validate(item):
            if (self.data == []):
                self.seq_matchstr = _getmatchval(item.line, *item.seq_cmprange)
            self.data.append(item)
            self.data.sort(key=SeqType.get_seq_no)
            item.seq_group = self
        else:
            raise (ValueError("Not a valid item for this sequence"))

    def extend(self, iter):
        for i in iter:
            self.append(i)

    @property
    def seq_nos(self):
        rv = []
        for r in self.data:
            rv.append(r.seq_no)
        return rv

    # TODO Think about doing this:
    # def __getitem__(self, idx):


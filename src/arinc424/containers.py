from .record import Record, MultiRecord, SeqType
from collections import UserList
# TODO Might want this later for searching & returning items from
# containers according to enum'd types.  But we don't use it currently.
#from arinc424.decoder import Field

class Collection(UserList):
    def __init__(self, arg = None):
        self.data = []
        self.barerec = []
        self.recgroups = []
        self.recseqs = []
        if arg is not None:
            self.extend(arg)

    def append(self, nr):
        target = nr
        if (isinstance(target, Record)):
            self.barerec.append(target)
        r = self._try_rg_add(target)
        if (r[0] is True):
            if (r[1] is not None):
                target = r[1]
            else:
                # Nothing more to do.
                return
        if (isinstance(target, RecGroup)):
            self.recgroups.append(target)
        r = self._try_seq_add(target)
        if (r[0] is True):
            if (r[1] is not None):
                target = r[1]
            else:
                # Nothing more to do.
                return
        if (isinstance(target, SeqGroup)):
            self.recseqs.append(target)
        self.data.append(target)

    def extend(self, iter):
        for i in iter:
            self.append(i)

    def clear(self):
        self.data.clear()
        self.barerec.clear()
        self.recgroups.clear()
        self.recseqs.clear()

    # For organizational purposes try_x_add needs to return some values so
    # that append can pass a record & get back... something..
    # that will tell it what to do with that record:
    #   1. Keep it as a stand alone record.
    #   2. Drop it as part of an already seen record group or sequence.
    #   3. Drop it and pick up a new record, or new sequence it's been added to.
    # At the end this will give us one list with a set of records, record groups,
    # and sequences.  All of which will be similarly processed by whatever the
    # collection holder wants to do.

    def _try_rg_add(self, r):
        # If it's not groupable, no sense running the rest of the func.
        if RecGroup.validate(r) is False:
            return (False, None)
        # Reverse the group in hope of some search optimization.
        for group in reversed(self.recgroups):
            try:
                group.append(r)
                r.rec_group = group
                return (True, None)
            except ValueError:
                # TODO ValueError is too generic. We should have a specific
                # err that indicates r wasn't a match to the record group.
                pass
        # Must be a new record group.
        new_rg = RecGroup()
        new_rg.append(r)
        r.rec_group = new_rg
        return (True, new_rg)

    def _try_seq_add(self, r):
        # Try seq add:
        if SeqGroup.validate(r) is False:
            return (False, None)
        # Reverse the group in hope of some search optimization.
        for seq in reversed(self.recseqs):
            #print(type(seq))
            #print(type(r))
            #print(isinstance(r, MultiRecord))
            #print(isinstance(r, RecGroup))
            try:
                # TODO If seq contains an rg, we may need to try adding r
                # to that, instead of adding r to the seq directly.
                if (isinstance(seq[0], RecGroup)
                    and RecGroup.validate(r)):
                    #print(f"Trying add to a zrec group: {seq[0]}")
                    seq[0].append(r)
                else:
                    #print(f"Trying plain add to {seq}")
                    seq.append(r)
                return (True, None)
            except ValueError:
                # TODO see ValueError exception in try_rg_add
                #print ("Failed, passing.")
                pass
        new_sg = SeqGroup()
        new_sg.append(r)
        return (True, new_sg)

    def debug(self):
        for x in self:
            if   (isinstance(x, Record)):
                print(f"BR: {x.rec_no}")
            elif (isinstance(x, RecGroup)):
                print(f"RG:")
                for y in x:
                    print(f"    {y.rec_no}")
            elif (isinstance(x, SeqGroup)):
                print(f"Seq:")
                for y in x:
                    if (isinstance(y, RecGroup)):
                        print("    RG:")
                        for z in y:
                            print(f"        {z.rec_no}")
                    else:
                        print(f"    {y.rec_no}")
            else:
                print(f"Big oops! {x}")

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

    @staticmethod
    def validate(nr):
        if ((isinstance(nr, MultiRecord) is False)
            or (nr.cont_no == 0)):
            return False
        return True

    def _validate(self, nr):
        # NR is the new rec to validate.
        if ((self.__class__.validate(nr) is False)
            or ((self.data != [])
                and (_checkmatch(self.rec_matchstr, nr.line) is False))):
            return False
        return True

    def __setitem__(self, idx, nr):
        #print (f"s: {self.data}")
        if self._validate(nr):
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

    @staticmethod
    def validate(nr):
        # First test: make sure the record type is right and if it's part of
        # a group, that we have the full group, not a single rec out of that
        # group.
        if ((isinstance(nr, MultiRecord) and (nr.cont_no != 0))
            or (isinstance(nr, RecGroup)
                and ((nr == []) or (isinstance(nr[0], SeqType) is False)))
            or (isinstance(nr, Record) and (isinstance(nr, SeqType) is False))):
            #print("va gonna return False")
            return False
        #print("va gonna return True")
        return True

    def _validate(self, nr):
        # (First test see static method validate)
        # Second test: Confirm two things:
        #   1) nr is a match for whatever other records we have in this seq..
        #      ie. same sec/subsec, same route, boundary, Apch etc.
        #   2) nr is not a seq no that is already present in the list.
        if ((self.__class__.validate(nr) is False)
            or (self.data != []
                and ((_checkmatch(self.seq_matchstr, nr.line) is False)
                     or (nr.seq_no in self.seq_nos)))):
            #print("_va gonna return False")
            return False
        #print("_va gonna return True")
        return True

    # These shouldn't be implemented because we want to tightly control
    # the order of records in a sequence group and these violate that.
    __setitem__ = property()
    insert = property()
    reverse = property()

    def append(self, item):
        if self._validate(item):
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


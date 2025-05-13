from .record import Record, MultiRecord, SeqType, BoundaryDefPtSeqType, FIR_UIR
from .decoder import Field_5_118
from collections import UserList
import math

nmi2mtr = 1852
# TODO Might want this later for searching & returning items from
# containers according to enum'd types.  But we don't use it currently.
#from arinc424.decoder import Field

class Collection(UserList):
    def __init__(self, arg = None):
        self.data = []
        self.barerec = []
        self.recgroups = []
        self.recseqs = []
        self.boundaryrecseqs = []
        if arg is not None:
            self.extend(arg)

    def append(self, nr):
        # print(f"append starts with a {type(nr)}")
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
        # print(f"After recgroup add it's a {type(target)}")
        r = self._try_boundaryseq_add(target)
        if (r[0] is True):
            # print(f"Got added as a boundary seq")
            if (r[1] is not None):
                target = r[1]
            else:
                return
        else:
            # print(f"Missed the boundary seq add, trying a"
            #       f"plain seq")
            r = self._try_seq_add(target)
            if (r[0] is True):
                # print(f"got added as a plain seq")
                if (r[1] is not None):
                    target = r[1]
                else:
                    # Nothing more to do.
                    return
        # print(f"After trying adds, it's a {type(target)}")
        if (isinstance(target, BoundaryDefSeqGroup)):
            self.boundaryrecseqs.append(target)
        elif (isinstance(target, SeqGroup)):
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
        self.boundaryrecseqs.clear()

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
        # print("_try_rg_add")
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
        # print ("_try_seq_add")
        if SeqGroup.validate(r) is False:
            return (False, None)
        # Reverse the group in hope of some search optimization.
        for seq in reversed(self.recseqs):
            #print(type(seq))
            #print(type(r))
            #print(isinstance(r, MultiRecord))
            #print(isinstance(r, RecGroup))
            try:
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

    def _try_boundaryseq_add(self, r):
        # print("_try_boundaryseq_add")
        # Try seq add:
        if BoundaryDefSeqGroup.validate(r) is False:
            # print("We think the BDSG.validate failed")
            return (False, None)
        # Reverse the group in hope of some search optimization.
        for seq in reversed(self.boundaryrecseqs):
            # print(type(seq))
            # print(type(r))
            # print(isinstance(r, MultiRecord))
            # print(isinstance(r, RecGroup))
            try:
                if (isinstance(seq[0], RecGroup)
                    and RecGroup.validate(r)):
                    # print(f"Trying add to a zrec group: {seq[0]}")
                    seq[0].append(r)
                else:
                    # print(f"Trying plain add to {seq}")
                    seq.append(r)
                return (True, None)
            except ValueError:
                # TODO see ValueError exception in try_rg_add
                # print ("Failed, passing.")
                pass
        new_sg = BoundaryDefSeqGroup()
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

# TODO Code to do this interpolation.
def rhumb_interpolate(r, distance, endpt):
    """ Interpolates the rhumb line defined by r from point
        r.point_geodesy to endpt.point_geodesy with distance
        being the maximum dist in nmi between interpolated points.

        Returns a list of points with type LatLon
        r and endpt are records of type BoundaryDefPtSeqType.
        distance is a float in nmi.
        """
    # We'll need azimuth & distance.
    pg0 = r.point_geodesy
    pg1 = endpt.point_geodesy
    rhumb_azimuth = pg0.rhumbAzimuthTo(pg1)
    rhumb_distance = pg0.rhumbDistanceTo(pg1)
    # Now use distance to work out an even distance between
    # interpolated points
    interp_points = math.ceil(rhumb_distance/(distance * nmi2mtr))
    true_dist = rhumb_distance/interp_points
    # Finally, interpolate the points.
    resultlist = []
    for n in range(interp_points):
        resultlist.append(pg0.rhumbDestination(true_dist * n, rhumb_azimuth))
    return resultlist

def arc_interpolate(r, distance, endpt):
    """ Interpolates the arc defined by r from point r.point_geodesy to
        the point endpt.point_geodesy with distance being the maximum degrees
        between interpolated points.

        Returns a list of points with type LatLon.
        r and endpt are records of type BoundaryDefPtSeqType.
        distance is a float in degrees."""
    if ((r.bound_via == Field_5_118.CCWARC) or
        (r.bound_via == Field_5_118.CCWARC_RET)):
        direction = -1
    else:
        direction = 1
    # Bering to the startpoint is r.arc_bering.
    # Need to find bering to the endpoint.
    if (r is not endpt):
        # if r and endpt are not the same, we need to identify end_bering, and
        # calc a true_dist that gives us evenly spaced points no farther apart
        # than distance (in degrees).
        start_bering = r.arc_bering
        temp = r.arc_focus_geodesy.distanceTo2(endpt.point_geodesy)
        end_bering = temp[1]
        bering_range = end_bering - start_bering
        if (((bering_range > 0) and (direction > 0)) or
            ((bering_range < 0) and (direction < 0))):
            bering_range = abs(bering_range)
        else:
            bering_range = 360 - (bering_range * direction * -1)
    else:
        # if r and endpt are the same, we have the special case of a circle.
        # Start bering can be 0, end bering & bering_range 360, and we can
        # calculate true_dist off of that.
        start_bering = 0
        end_bering = 360
        bering_range = 360
    interp_points = math.ceil(bering_range/distance)
    true_dist = bering_range/interp_points
    rvlist = []
    for n in range(interp_points):
        res_pt = r.arc_focus_geodesy.destination(
            r.arc_radius * nmi2mtr,
            (start_bering + (n * true_dist * direction)))
        rvlist.append(res_pt)
    #print (f"Arc complete.")
    return rvlist

class BoundaryDefSeqGroup(SeqGroup):
    rhumb_interp_distance = .1  # nmi
    arc_interp_distance = 5     # degrees

    @staticmethod
    def validate(nr):
        #print("bdsg validate:")
        #print(SeqGroup.validate(nr))
        #print(isinstance(nr, RecGroup))
        #if (isinstance(nr, RecGroup)):
        #    print(isinstance(nr[0], BoundaryDefPtSeqType))
        #print(isinstance(nr, BoundaryDefPtSeqType))
        if ((SeqGroup.validate(nr) is False) or
            (isinstance(nr, BoundaryDefPtSeqType) is False) or
            ((isinstance(nr, RecGroup) is True) and
             (isinstance(nr[0], BoundaryDefPtSeqType) is False))):
            return False
        return True

    @property
    def boundary_point_geodesy_list(self):
        rvdict = {}
        # Build the rv dict in a two stage approach.
        # Stage one: parse thru all the records and work out the
        #     A, B, C, etc. record sets.
        for r in self.data:
            if (isinstance(r, RecGroup) is True):
                pointrec = r[0]
            else:
                pointrec = r
            if (type(pointrec) is FIR_UIR):
                multiple_id = ''
            else:
                multiple_id = pointrec.line[19]
            if (multiple_id not in rvdict.keys()):
                rvdict[multiple_id] = {
                    'start': pointrec,
                    'reclist': [pointrec],
                    'pointlist': []
                    }
            else:
                rvdict[multiple_id]['reclist'].append(pointrec)

        # Stage two: parse & interpolate the individual record sets
        #     into point lists
        for k in rvdict:
            reclist = rvdict[k]['reclist']
            for n in range(len(reclist)):
                pointrec = reclist[n]
                n_plus_one = (n + 1) % len(reclist)
                nextpointrec = reclist[n_plus_one]

                if ((pointrec.bound_via == Field_5_118.GCIRC) or
                    (pointrec.bound_via == Field_5_118.GCIRC_RET)):
                    # Great circle doesn't require any interpolation, just put the
                    # point in.
                    rvdict[k]['pointlist'].append(pointrec.point_geodesy)
                elif ((pointrec.bound_via == Field_5_118.RHUMB) or
                      (pointrec.bound_via == Field_5_118.RHUMB_RET)):
                    rvdict[k]['pointlist'].extend(
                        rhumb_interpolate(pointrec,
                                          self.rhumb_interp_distance,
                                          nextpointrec))
                elif ((pointrec.bound_via == Field_5_118.CIRC) or
                      (pointrec.bound_via == Field_5_118.CIRC_RET)):
                    rvdict[k]['pointlist'].extend(
                        arc_interpolate(pointrec,
                                        self.arc_interp_distance,
                                        pointrec))
                elif ((pointrec.bound_via == Field_5_118.CCWARC) or
                      (pointrec.bound_via == Field_5_118.CWARC) or
                      (pointrec.bound_via == Field_5_118.CCWARC_RET) or
                      (pointrec.bound_via == Field_5_118.CWARC_RET)):
                    # Circles, cw, and ccw arcs are all just different cases of
                    # arc interpolation.
                    rvdict[k]['pointlist'].extend(
                        arc_interpolate(pointrec,
                                        self.arc_interp_distance,
                                        nextpointrec))
                # End records need a closing data point added.
                if ((pointrec.bound_via == Field_5_118.GCIRC_RET) or
                    (pointrec.bound_via == Field_5_118.CIRC_RET) or
                    (pointrec.bound_via == Field_5_118.RHUMB_RET) or
                    (pointrec.bound_via == Field_5_118.CCWARC_RET) or
                    (pointrec.bound_via == Field_5_118.CWARC_RET)):
                    rvdict[k]['pointlist'].append(
                        rvdict[k]['pointlist'][0]
                    )
            del rvdict[k]['reclist']

        if (type(pointrec) is FIR_UIR):
            return rvdict['']['pointlist']
        return rvdict

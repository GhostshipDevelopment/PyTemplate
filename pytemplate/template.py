from struct import unpack, pack
from collections import OrderedDict as OD

class DataTypeReader(object):
    def __init__(self, endian="<", dry_run=False):
        self.endian = endian
        self.dry_run = dry_run
    def integer(self, f_obj):
        return self._dtype_gen_read("i", 1, 4, f_obj)
    def long_integer(self, f_obj):
        return self._dtype_gen_read("l", 1, 8, f_obj)
    def short(self, f_obj):
        return self._dtype_gen_read("h", 1, 2, f_obj)
    def string(self, f_obj, st_length):
        return self._dtype_gen_read("s", st_length, st_length, f_obj)
    def char(self, f_obj):
        return self._dtype_gen_read("c", 1, 1, f_obj)
    def byte(self, f_obj):
        return self._dtype_gen_read("b", 1, 1, f_obj)
    def _dtype_gen_read(self, dtype, dtype_count, dtype_size, f_obj):
        if self.dry_run:
            #must handle strings differently, since they are unpacked based on size and count.
            if dtype == "s":
                f_obj.seek(f_obj.tell() + dtype_size)
            else:
                f_obj.seek(f_obj.tell()  + (dtype_size * dtype_count))
            yield None
        else:
            yield unpack("%s%s%s" % (self.endian, dtype_count, dtype), f_obj.read(dtype_size))[0]

class DataTypeWriter(object):
    def __init__(self, endian="<"):
        self.endian = endian
    def integer(self, f_obj, value):
        return self._dtype_gen_write("i", value, 1, f_obj)
    def long_integer(self, f_obj):
        return self._dtype_gen_write("l", value, 1, f_obj)
    def short(self, f_obj, value):
        return self._dtype_gen_write("h", value, 1, f_obj)
    def string(self, f_obj, value):
        return self._dtype_gen_write("s", value, len(value), f_obj)
    def char(self, f_obj, value):
        return self._dtype_gen_write("c", value, 1, f_obj)
    def byte(self, f_obj, value):
        return self._dtype_gen_write("b", value, 1, f_obj)
    def _dtype_gen_write(self, dtype, value, dtype_count, f_obj):
        yield f_obj.write(pack("%s%s%s" % (self.endian, dtype_count, dtype), value))

class Template(object):
    def __init__(self, writer=None):
        self.writer = writer
    def define(self, odict):
        self.definition = odict
    def extract(self):
        values = dict()
        for v_name in self.definition:
            values[v_name] = list(self.definition[v_name])[0]
        return values
    def write(self):
        for v_name, v_gen_write in self.definition.iteritems():
            list(v_gen_write)

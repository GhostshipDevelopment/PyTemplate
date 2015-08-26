from collections import OrderedDict as OD
from pytemplate import DataTypeReader as DTR_U
from pytemplate import DataTypeWriter as DTW_U
from pytemplate import Template as T

#create bindings for read/write objects
DTR = DTR_U()
DTW = DTW_U()

#for testing
import sqlite3
import os

#easy dbg
from pprint import PrettyPrinter as PP
p = PP().pprint

def read_header(f_obj):
    template = T()
    t_dict = OD()
    t_dict["header_string"] = DTR.string(f_obj, 16)
    t_dict["page_size"] = DTR.short(f_obj)
    t_dict["ff_write_version"] = DTR.byte(f_obj)
    t_dict["ff_read_version"] = DTR.byte(f_obj)
    t_dict["max_embedd_payload_frac"] = DTR.byte(f_obj)
    t_dict["min_embedd_payload_frac"] = DTR.byte(f_obj)
    t_dict["leaf_payload_frac"] = DTR.byte(f_obj)
    t_dict["f_change_counter"] = DTR.integer(f_obj)
    t_dict["header_db_size"] = DTR.integer(f_obj)
    t_dict["first_freelist_trunk_page_num"] = DTR.integer(f_obj)
    t_dict["freelist_trunk_page_count"] = DTR.integer(f_obj)
    t_dict["schema_cookie_offset"] = DTR.integer(f_obj)
    t_dict["schema_format_number"] = DTR.integer(f_obj)
    t_dict["default_page_cache_size"] = DTR.integer(f_obj)
    t_dict["largest_root_btree_page"] = DTR.integer(f_obj)
    t_dict["db_text_encoding"] = DTR.integer(f_obj)
    t_dict["user_version"] = DTR.integer(f_obj)
    t_dict["vacuum_mode"] = DTR.integer(f_obj)
    t_dict["application_id"] = DTR.integer(f_obj)
    t_dict["expansion_space"] = DTR.string(f_obj, 20)
    t_dict["version_valid_for"] = DTR.integer(f_obj)
    t_dict["sqlite_version_number"] = DTR.integer(f_obj)
    template.define(t_dict)
    return template.extract()

def _main_create_db(path):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE test(var1 int, var2 int);")
    connection.commit()
    connection.close()

def main():
    _main_create_db("test.db")
    with open("test.db", "rb") as db_file:
        header = read_header(db_file)
        print db_file.tell()
        p(header)
    if os.path.exists("test.db"):
        os.remove("test.db")


if __name__ == '__main__':
    main()

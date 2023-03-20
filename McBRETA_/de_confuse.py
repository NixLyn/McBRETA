# LOCAL
from File_man import File_Man
from which_hash import WhichHash_


# SYS_BASE
import subprocess
from threading import Thread
import time
import socket
import struct
import textwrap
import codecs
#from pcapkit import extract, IP, HTTP



# ! MY_OWN_TSHARK
class DeFuse_():
    def __init__(self, **kw):
        super(DeFuse_, self).__init__(**kw)
        self.FM                 = File_Man()
        self.WH                 = WhichHash_()
        self.pack_num           = 0
        self.decrypt            = 0




    def from_x_hex(self, payload_, prof_dir):
        self.pack_num += 1
        try:
            byt_it = str(payload_).split(r"\x")
            d_sp = ""
            for it_ in byt_it:
                d_sp += str(it_)
            print("\n\t ~~~~[HASHI_LISTIn']", str(d_sp))
            self.hash_id_r(d_sp, prof_dir)
        except Exception as e:
            print(f"\n\t ~~~~[E]:[FROM_xHEX_lT]:[{str(e)}]")

        try:
            # ? Decode...
            hashi_0 = payload_.decode('utf-16')
            print(f"\n\t ~~~~[UTF-16]:[{str(hashi_0)}]")
            self.hash_id_r(hashi_0, prof_dir)
        except Exception as e:
            print(f"\n\t ~~~~[E]:[FROM_xHEX_t_01]:[{str(e)}]")

        try:
            # ? Decode...
            hashi_1 = codecs.decode(payload_)
            print(f"\n\t ~~~~[CODECS_]:[{str(hashi_1)}]")
            self.hash_id_r(hashi_1, prof_dir)
        except Exception as e:
            print(f"\n\t ~~~~[E]:[FROM_xHEX_t1]:[{str(e)}]")

        try:
            hashi_2 = payload_.decode('utf-8')
            print(f"\n%%%%%[UTF-8]\n\t ~~~~[UTF-8]:[{str(hashi_2)}]")
            self.hash_id_r(hashi_2, prof_dir)
        except Exception as e:
            print(f"\n\t ~~~~[E]:[FROM_xHEX_t2]:[{str(e)}]")


    # ! TODO: DECRYPT PAYLOAD_
    def to_sting(self, data_list):
        try:
            # Iterate through list:
            # Convert each hex to str
            # Append to ret_list
            pass
        except Exception as e:
            print(f"\n\t ~~~~[E]:[To_String]:[{str(e)}]")


    def hash_id_r(self, payload_, prof_dir):
        try:
            print("[CHECKING_HASH]")
            h_type = self.WH.get_type(payload_)
            print(f"\n##########\n[HASH_ID]:[{h_type}]\n##########\n")
            if h_type is not None:
                to_write = f"[PAYLOAD]:[>{str(payload_)}<]\n[CRYPT_TYPE]:[>{str(h_type)}<]\n%%\n"
                self.FM.write_file(prof_dir+"de_decoed.txt", to_write, "$", "a+")
        except Exception as e:
            print(f"\n\t ~~~~[E]:[FROM_xHEX_t0]:[{str(e)}]")






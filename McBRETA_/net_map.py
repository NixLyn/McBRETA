# BASE
import subprocess

# LOCAL
from File_man import File_Man
import time

# TODO:
    # ! CLEAN_DATA
    # ? TCP
    # ? UDP
    # ? SSH
    # ? FTP
    # ? SQL
    # ? SMTP/POP3
    # ? SSL/TLS
    # ? etc

class NetMap():
    def __init__(self, **kw):
        super(NetMap, self).__init__(**kw)
        self.FM                 = File_Man()

    # FILTER - PORTS [PARAM]
    def get_param(self, data, param_):
        try:
            ret_data = []
            for index in data:
                if str(param_) in str(index):
                    print(f"[PARAM_]::[{str(index)}]")
                    ret_data.append(str(index))
            return ret_data
        except Exception as e:
            print(f"[E]:[GET_TCP]:[{str(e)}]")


    # FILTER - PORTS [TCP(s)]
    # ! ONLY_TCP
    def get_tcp(self, data_str):
        print("\n-- -- [FILTERING_TCP]")
        data = data_str.split(" ")
        time.sleep(5)
        try:
            print("\n--*-- -- [FILTERING_TCP]")
            ret_data = []
            for index in data:
                #print("[NET_MAP_INDEX]:",str(index))
                if "/tcp" in str(index):
                    pudding = str(index.split("\n")[1])[:-4]
                    print(f"[TCP]::[{str(index)}]")
                    print(f"[PUDDIN']::[{str(pudding)}]")
                    if str(pudding) not in str(ret_data):
                        ret_data.append(str(pudding))
            time.sleep(5)
            return ret_data
        except Exception as e:
            print(f"[E]:[GET_TCP]:[{str(e)}]")


    # ! BASH_SCRIPTED
    def og_scan(self, type_, host_, file_dir, flags_, params_):
        try:
            tcp_ = []
            print(f"[RUNNING]:[NET_MAP]:[>{type_}<]")
            to_run      = "nmap -A "+flags_+" "+host_
            nmap_return = subprocess.getoutput(to_run)
            self.FM.save_scan(file_dir, f"nmap_scan_{type_}.csv", nmap_return)
            print("[NET_MAP]:[SAVED]")
            tcp_ = self.get_tcp(nmap_return)
            print("[OG_SCAN-TCP_]:",str(tcp_))
            self.FM.write_file(file_dir+f"/nmap_tcp_{type_}.csv", tcp_, ",", "w")
            #self.FM.save_scan(file_dir, f"nmap_tcp_{type_}.csv", tcp_)
            print("[TCP]:[SAVED]")
            #if params_:
            #    par_ = self.get_param(nmap_return, params_)
            #    self.FM.save_scan(file_dir, "nmap_paras.csv", nmap_return)
            #    print("[PARAMS]:[SAVED]")
            #    return par_
            #else:
            return tcp_
        except Exception as e:
            print(f"[E]:[OG_NMAP]:[>{str(e)}<]")


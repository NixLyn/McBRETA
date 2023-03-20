# LOCAL
from File_man import File_Man

# TOOLS_
from brute_ssh import BruteSSH
from net_map import NetMap
from micro_scans import MicroScans
from meta_fab import MetaFab
from dir_scan import DirScan_
from listen_ import Listen_

# SYS_BASE
import sys
import threading
import ipaddress
import time


class TestCase_0():
    def __init__(self, **kw):
        super(TestCase_0, self).__init__(**kw)
        self.FM         = File_Man()
        self.BSS         = BruteSSH()
        self.NM         = NetMap()
        self.MS         = MicroScans()
        self.META       = MetaFab()
        self.DiS        = DirScan_()
        self.LI         = Listen_()


    # ! BUILD PROFILE
    def make_profile(self, tar_type, tar_val, port_, l_host, l_port, f_name):
        try:
            prof_ = "profiles_/"


            file_dir = ""
            if "http://" in str(tar_val):
                print("[DO NOT USE 'HTTP(S)://']")
                return "HTTP", "ERROR"


            if "URL" in  tar_type.upper():
                IP_ = self.MS.dis_lookup(tar_val)
                print("[URL-IP]:", str(IP_))
            else:
                IP_ = tar_val

            IP_val = self.MS.dis_lookup(tar_val)
            to_save_ = f"[TAR_TYPE]:[>{str(tar_type)}<]\n[TAR_VAL]:[>{str(tar_val)}<]\n[IP_VAL]:[{str(IP_val)}]\n[Re_PORT]:[>{str(port_)}<]\n[L_HOST]:[>{str(l_host)}<]\n[L_PORT]:[>{str(l_port)}<]"


            if f_name:
                file_dir = f_name
            else:
                file_dir = IP_.replace(".", "_")
            print(f"[MAIN_FILE_DIR]:[>{str(file_dir)}<]")

            make_dir = prof_+file_dir
            print(f"[TEST_DIR]:[{str(make_dir)}]")
            make_dir = str(self.FM.check_prof_(make_dir, 0))
            print(f"[AVAILABLE_DIR]:[{str(make_dir)}]")

            save_at = make_dir+"/profile.csv"
            self.FM.make_dir(make_dir)
            print(f"\n@@\n[DIR_TO_MAKE]:[{make_dir}]")
            self.FM.write_file(save_at, to_save_, "\n", "a+")
            print("[IP_OF_PROFILE]:",str(IP_))
            return make_dir, IP_
        except Exception as e:
            print(f"[E]:[MAKING_PROFILE]:[>{str(e)}<]")
            return str(e)

    # ! LOW_GRADE_BRUTES
    def base_brutes(self, type_, target_, port_, file_dir):
        IP_ = ""
        try:
            IP_ = ""
            if type_ == "URL":
                print("[TYPE_URL]...\n[FETCHING_IP]...")
                # ! NS_LOOK_UP -> IP_
                IP_ = self.MS.dis_lookup(target_)
                print(f"[IP_FOUND]:[>{str(IP_)}<]")
                print(f"[STARTING_]:[BASE_BRUTES]")

            # INITS
            try:
                # @ BASE BRUTES
                # ! HYDRA
                self.hydra_ = threading.Thread(target=self.BSS.go_hydra, args=(IP_, file_dir, ))
                # !MEDUSA
                self.medusa_ = threading.Thread(target=self.BSS.go_medusa, args=(IP_, file_dir, ))
            except Exception as e:
                print(f"[E]:[BRUTE_TRHEADS]:[>{str(e)}<]")

            # RUN_THREADS
            try:
                print("[$]:[HYDRA]:[START]")
                self.hydra_.start()
                print("[$]:[MEDUSA]:[START]")
                self.medusa_.start()
            except Exception as e:
                print(f"[E]:[START_THREADS]:[>{str(e)}<]")
            print("[BRUTES_LAUNCHED]")
            return True
        except Exception as e:
            print(f"[E]:[BASE_BRUTES]:[>{str(e)}<]")
            return False

    # ! BASE SCANS
    # ! THREAD TO FINISH BEFORE NEXT ONE CAN START
    def start_scan(self, type_, target_, port_, file_dir):
        IP_ = ""
        try:
            IP_ = ""
            if type_ == "URL":
                print("[TYPE_URL]...\n[FETCHING_IP]...")
                # ! NS_LOOK_UP -> IP_
                IP_ = self.MS.dis_lookup(target_)
                print(f"[IP_FOUND]:[>{str(IP_)}<]")
                print(f"[STARTING_]:[MICRO_SCANS]:[&&]:[NET_MAP]")
            try:
                # @ BASE SCANNS
                # ! ALL_MICRO_SCANS
                self.MS.all_scans(type_, target_, file_dir)
                # ! NET_MAP_URL -> TCP_LIST
                tcp_ = self.NM.og_scan(type_, target_, file_dir, " ", port_)
                return tcp_
            except Exception as e:
                print(f"[E]:[STD_SCANS]:[>{str(e)}<]")
            print("[SCANS_COMPLETED]")

        except Exception as e:
            print(f"[E]:[START_SCAN]:[>{str(e)}<]")
            return ["ERROR", "OG_SCAN", "START_SCAN"]

    # ! META_SPLOIT_ATTACK
    def launch_att(self,l_host, l_port, target_, prof_dir, type_, tcp_, thr_):
        try:
            print("[LAUNCHING_McBrEtA_!]")
            IP_ = self.MS.dis_lookup(target_)
            print("\n[IP_TAGERT]:",str(target_))
            # ! META_SPLOIT
            self.META.set_meta_stack_(l_host, l_port, target_, prof_dir, type_, tcp_, thr_)
            # ! WATCH_FILE ! TODO
            print("[McBRETA_RUN_COMPLETE]")
        except Exception as e:
            print(f"[E]:[McBRETA]:[MAIN]:[>{str(e)}<]")

    # ! START LISTENING
    def listen_in(self, addr_, port_, prof_dir):
        try:
            threading.Thread(target=self.LI.main, args=(addr_, port_, prof_dir))
            print("[LiSTENING_STARTED]")
        except Exception as e:
            print(f"[E]:[LISTEN_IN]:[{str(e)}]")


    # ! MAIN
    def main(self):
        try:
            print("\n----------------------------\n[WELCOME]:[McBreta]:[Off-Sec]\n----------------------------\n")
            while True:
                f_name  = input("[FOLDER_NAME]: ")
                type_   = input("[TARGET_TYPE]\n[IP/URL]: ")
                if not type_:
                    type_ = "IP"
                target_ = input("[TAR_VAL]: ")
                if not target_:
                    print("[MUST_HAVE_TARGET]\n[TRY_AGAIN]\n")
                    time.sleep(1)
                    print("[...]")
                    time.sleep(1)
                    print("[.. ]")
                    time.sleep(1)
                    print("[.  ]")
                    return self.main()
                port_  = input("[Re_PORT]: ")
                l_host = input("[L_HOST]: ")
                if not l_host:
                    l_host = "127.0.0.1"
                l_port = input("[L_PORT]: ")
                if not l_port:
                    l_port = "23"
                thr_ = input("[THREADING]-[y/N]: ")
                if not thr_:
                    thr_lvl = "N*0"
                if "Y" in thr_:
                    thr_lvl = "Y*" + input("[THREAD_LVL]:[INT()]:\n[0]-[NO_THREADS]\n[1]:[TWO_BASE_THREADS]\n[2]:[THREAD_PER_PORT]\n[3]:[THREAD_PER_PROCESS]\n>>[#]:")




                print("\n[SETTING_TAGRET]\n")
                prof_dir, IP_ = self.make_profile(type_, target_, port_, l_host, l_port, f_name)
                print("[TAR_DIR]:",str(prof_dir))
                print("[TAR_IP]: ",str(IP_))


                try:
                    ip_cat = ipaddress.ip_address(IP_)
                    tar_type = "IP"

                except:
                    tar_type = "URL"
                    print("[URL]->[DIR_SCAN]")
                    self.DiS.dir_seach(target_, prof_dir)


                print("\n************\n[COMPILED_PROFILE]\n")
                print(f"[TAR_TYPE]:[>{str(tar_type)}<]")
                print(f"[TAR_VAL]:[>{str(IP_)}<]")
                print(f"[Re_PORT]:[>{str(port_)}<]")
                print(f"[L_HOST]:[>{str(l_host)}<]")
                print(f"[L_PORT]:[>{str(l_port)}<]")
                print(f"[THREAD_LVL]:[{str(thr_lvl)}]")



                if "ERROR" not in str(prof_dir):
                    print("[STRATING_SCANS]")
                    tcp_ =self.start_scan(type_, IP_, port_, prof_dir)
                    print("\n************\n[SCANS_COMPLETE]\n")
                    print("[IP_TARGET]:", str(IP_))
                    listen_i = input("[RUN_LISTENER]:[Y/n]")
                    if "N" not in listen_i.upper():
                        self.listen_in(IP_, tcp_, prof_dir)
                    att_ = input("[RUN_ATTACK]:[Y/n]")
                    if "N" not in att_.upper():
                        self.launch_att(l_host, l_port, IP_, prof_dir, type_, tcp_, thr_lvl)
                else:
                    print(f"[E]:[SCAN_NOT_STARTED]")
                print("[_McBRETA_COMPLETED]\n!*!\n\n")

        except Exception as e:
            print(f"[E]:[TEST_CASE]:[MAIN]:[>{str(e)}<]")
            return False



if __name__=="__main__":
    TC_0 = TestCase_0()
    TC_0.main()
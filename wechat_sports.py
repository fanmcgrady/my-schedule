## utf-8
import subprocess

class altera_system_console:
    def __init__(self):
        sc_path = r'program/wechat.exe'
        self.console = subprocess.Popen(sc_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def read_output(self):
        return self.console.stdout.read1(100).decode('utf-8')
        # rtn = ""
        # loop = True
        # i = 0
        # match = r"\x  "
        # while loop:
        #     out = self.console.stdout.read1(1)
        #     tt = bytes(match[i],'utf-8')
        #     if bytes(match[i],'utf-8') == out:
        #         i = i+1
        #         if i==len(match):
        #             loop=False
        #     else:
        #         rtn = rtn + out.decode('utf-8',"ignore")
        # return rtn

    def cmd(self, cmd_string):
        self.console.stdin.write(bytes(cmd_string+'\n','utf-8'))
        self.console.stdin.flush()

def set_step(step, username, password):
    c = altera_system_console()
    print(c.read_output())
    c.cmd(step)
    print(c.read_output())
    c.cmd(username)
    print(c.read_output())
    c.cmd(password)
    print(c.read_output())

if __name__ == '__main__':
    # 秦书记
    set_step("23256", "13980023515", "qy123456")
    # 我
    set_step("34567", "13550345266", "133Fzy09962659")
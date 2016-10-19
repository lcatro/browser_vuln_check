
import os

import crash_poc_valid_logic
import uncrash_poc_valid_logic

BROWSER_PATH='C:\\Program Files (x86)\\Tencent\\QQBrowser\\QQBrowser.exe'

'''

    Using : 
        ready_to_check.py [setting] %browser_exe_path%

    setting :
        /uncrash               valid uncrash poc
        /crash                 valid crash poc
        /gflag                 using gflag debug
        /parameter "%string%"  browser parameter

'''

if __name__=='__main__' :
    uncrash_poc_valid_logic.valid_uncrash_poc(BROWSER_PATH)
    crash_poc_valid_logic.valid_crash_poc(BROWSER_PATH)

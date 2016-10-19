
import os
import pydbg
import time

import server

create_process_pid_list=[]

def add_new_process_pid(process_id) :  #  uncrash poc valid logic using pydbg for kill all subprocess of the browser ..
    global create_process_pid_list
    
    create_process_pid_list.append(process_id)

def kill_all_process() :
    global create_process_pid_list
    
    for sub_process_id_index in create_process_pid_list :
        try :
            os.kill(sub_process_id_index,9)
        except :
            pass
        
def create_process_debug_event_handle(self) :
    new_process_pid=self.dbg.dwProcessId
    
    add_new_process_pid(new_process_pid)
    
    return pydbg.defines.DBG_CONTINUE

def monitor_browser_crash(browser_path,command_line) :
    debugger=pydbg.pydbg()
    
    debugger.load(browser_path,command_line)
    debugger.set_callback(pydbg.defines.CREATE_PROCESS_DEBUG_EVENT,create_process_debug_event_handle)
    debugger.run()
    debugger.wait_for_process_exit()
    debugger.detach()
    kill_all_process()

def valid_uncrash_poc(browser_path) :
    command_line='"http://127.0.0.1:'+str(server.LOCAL_BIND_PORT)+'/uncrash_scan"'

    monitor_browser_crash(browser_path,command_line)


import os
import pydbg

import base_function
import server

create_process_pid_list=[]

def add_new_process_pid(process_id) :
    global create_process_pid_list
    
    create_process_pid_list.append(process_id)

def kill_all_process() :
    global create_process_pid_list
    
    for sub_process_id_index in create_process_pid_list :
        try :
            os.kill(sub_process_id_index,9)
        except :
            pass
    
def get_instruction(debugger,address,pid) :
    for instruction in debugger.disasm_around(address,10,pid) :
        if instruction[0]==address :
            print '->'+str(hex(instruction[0]))[:-1]+':  '+instruction[1]
        else :
            print '  '+str(hex(instruction[0]))[:-1]+':  '+instruction[1]

            
def create_process_debug_event_handle(self) :
    new_process_pid=self.dbg.dwProcessId
    
    add_new_process_pid(new_process_pid)
    
    return pydbg.defines.DBG_CONTINUE

def access_exception_debug_event_handle(self) :
    current_pid=self.dbg.dwProcessId
    current_address=self.exception_address
    
    print 'WARNING! PID:'+str(current_pid)+' Making a Access Exception (0xC0000005) '
    print 'Detail Report :\r\n'
    print '  Exception Address:'+str(current_address)
    print '  EAX:'+str(hex(self.get_register('EAX')))[:-1],'EBX:'+str(hex(self.get_register('EBX')))[:-1],'ECX:'+str(hex(self.get_register('ECX')))[:-1],'EDX:'+str(hex(self.get_register('EDX')))[:-1],'ESP:'+str(hex(self.get_register('ESP')))[:-1],'EBP:'+str(hex(self.get_register('EBP')))[:-1],'ESI:'+str(hex(self.get_register('ESI')))[:-1],'EDI:'+str(hex(self.get_register('EDI')))[:-1]
    print ''
    
    get_instruction(self,current_address,current_pid)
    kill_all_process()
    
    return pydbg.defines.DBG_CONTINUE

def breakpoint_exception_debug_event_handle(self) :
    current_pid=self.dbg.dwProcessId
    current_address=self.exception_address
    
    if not str(hex(current_address))[-3:]=='cf4' :
        print 'WARNING! PID:'+str(current_pid)+' Making a BreakPoint Exception [INT 3 or Hard Breakpoint ](0x80000003) '

        get_instruction(self,current_address,current_pid)
        kill_all_process()

    return pydbg.defines.DBG_CONTINUE

def stack_overflow_debug_event_handle(self) :
    print 'WARNING! PID:'+str(self.dbg.dwProcessId)+' Making a Stack OverFlow Exception (0xC00000FD) '
    
    kill_all_process()
    
    return pydbg.defines.DBG_CONTINUE


def monitor_browser_crash(browser_path,command_line) :
    debugger=pydbg.pydbg()
    
    debugger.load(browser_path,command_line)
    debugger.set_callback(pydbg.defines.CREATE_PROCESS_DEBUG_EVENT,create_process_debug_event_handle)
    debugger.set_callback(pydbg.defines.EXCEPTION_ACCESS_VIOLATION,access_exception_debug_event_handle)
    debugger.set_callback(pydbg.defines.EXCEPTION_BREAKPOINT,breakpoint_exception_debug_event_handle)
    debugger.set_callback(pydbg.defines.EXCEPTION_GUARD_PAGE,access_exception_debug_event_handle)
    debugger.set_callback(pydbg.defines.EXCEPTION_STACK_OVEWFLOW,access_exception_debug_event_handle)
    debugger.run()
    debugger.wait_for_process_exit()
    debugger.detach()

def valid_crash_poc(browser_path) :
    crash_file_list=base_function.list_dir_file(base_function.get_current_path()+'crash_poc')
    
    for crash_file_index in crash_file_list :
        if (crash_file_index[1]=='index.html' or
            -1!=crash_file_index[1].find('CVE') or
            -1!=crash_file_index[1].find('POC')) :
            if '.pdf'==crash_file_index[1][-4:] :
                command_line='"'+crash_file_index[0]+'"'
                monitor_browser_crash(browser_path,crash_file_index[0])
            else :
                crash_poc_relative_path=base_function.get_relative_path(False,crash_file_index[0])
                command_line='"http://127.0.0.1:'+str(server.LOCAL_BIND_PORT)+'/crash_poc?poc_name='+crash_file_index[1]+'"'

                monitor_browser_crash(browser_path,command_line)
                
#            raw_input()

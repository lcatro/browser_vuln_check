
import os
import sys


def resolve_url_parameter(url,url_parameter_name) :  #  Just Resolve First URL Parameter
    url_flag='?'+url_parameter_name+'='
    url_flag_index=url.find(url_flag)
    
    return url[url_flag_index+len(url_flag):]
        
def get_relative_path(is_crash_path,file_path) :
    current_file_path=get_current_path()
    
    if is_crash_path :
        return file_path.replace(current_file_path+'crash_poc\\','')
    
    return file_path.replace(current_file_path+'uncrash_poc\\','')
        
def get_current_path() :  #  Get Script Save Path
    current_file_name=sys.argv[0]
    current_path=current_file_name[:current_file_name.rfind('\\')+1]
    
    return current_path
        
def list_dir_file(file_path) :  #  Get All File and Dir Name at file_path
    output_file_list=[]
    for dir_path,dir_name,file_name in os.walk(file_path) :
        for file_name_index in file_name :
            output_file_list.append((dir_path+'\\'+file_name_index,file_name_index))

    return output_file_list
        
def read_poc(is_crash_poc,poc_name) :  #  Read a PoC File from uncrash/crash PoC dir
    poc_file_list=[]
    poc_file_data=''
    
    if is_crash_poc :
        poc_file_list=list_dir_file('crash_poc')
    else :
        poc_file_list=list_dir_file('uncrash_poc')
        
    for poc_file_index in poc_file_list :
        if poc_file_index[1]==poc_name :
            return read_file(poc_file_index[0])
    
    return ''

def read_file(file_path) :
    poc_file=open(file_path)
    poc_file_data=''

    if poc_file :
        poc_file_data=poc_file.read()
        poc_file.close()

    return poc_file_data

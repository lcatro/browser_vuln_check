#! /user/bin/python
# coding:UTF-8

import logging
import json
import tornado.web
import tornado.ioloop
import socket
import urllib

import crash_poc_valid_logic
import uncrash_poc_valid_logic

from base_function import *


LOCAL_BIND_PORT=80


class uncrash_handle(tornado.web.RequestHandler) :  #  Ready to valid UnCrash PoC 
    def get(self) :
        temple_poc_check_code=read_poc(False,'run.html')  ## Read UnCrash PoC valid Framework Code
        temple_poc_check_code_replace_flag='<!-- %Replace_This_For_Auto_Fill_PoC_Name -->'
        
        if not ''==temple_poc_check_code :
            uncrash_poc_list=list_dir_file(get_current_path()+'uncrash_poc')  ##  Read All UnCrash PoC File
            uncrash_poc_enter_point_list=[]
            
            for uncrash_poc_index in uncrash_poc_list :
                if (uncrash_poc_index[1]=='index.html' or
                    0==uncrash_poc_index[1].find('CVE') or
                    0==uncrash_poc_index[1].find('POC')) :  ##  Filter Main EnterPoint UnCrash CVE PoC File
                    uncrash_poc_enter_point_list.append(get_relative_path(False,uncrash_poc_index[0]))
            
            insert_to_temple_framework_code=''

            for uncrash_poc_enter_point_index in uncrash_poc_enter_point_list :  ##  Build PoC Call <iframe> Code
                insert_to_temple_framework_code+='<iframe src="uncrash_poc?poc_name='+uncrash_poc_enter_point_index+'" style="visibility:hidden;"></iframe>'
                
            output_uncrash_poc_scan_framework_code=\
                temple_poc_check_code.replace(temple_poc_check_code_replace_flag,insert_to_temple_framework_code)  ##  Insert All PoC into valid page
            output_uncrash_poc_scan_framework_code=\
                output_uncrash_poc_scan_framework_code.replace('%log_url%','"http://127.0.0.1:'+str(LOCAL_BIND_PORT)+'/report?log="')  ##  Setting Log URL 
            output_uncrash_poc_scan_framework_code=\
                output_uncrash_poc_scan_framework_code.replace('%poc_count%',str(len(uncrash_poc_enter_point_list)))  ##  Setting PoC Number 
            
            self.write(output_uncrash_poc_scan_framework_code)
        else :
            self.write('Lost temple Framework Code ..')
        
class read_poc_handle(tornado.web.RequestHandler) :  #  Read PoC by Browser Request
    def get(self) :
        url=self.request.uri
        url_split_flag_index=url.rfind('?')
        access_dir=''
        
        if -1!=url_split_flag_index :
            access_dir=url[1:url_split_flag_index]
        
        poc_name=resolve_url_parameter(url,'poc_name')
    
        if 'crash_poc'==access_dir :
            self.write(read_poc(True,poc_name))
        elif 'uncrash_poc'==access_dir :
            self.write(read_poc(False,poc_name))

class report_handle(tornado.web.RequestHandler) :  #  Log Server
    def get(self) :
        log_data_=urllib.unquote(resolve_url_parameter(self.request.uri,'log'))
        log_data=json.loads(log_data_)
        
        if log_data.get('scan_state') :
            if log_data.get('uncrash_poc_scan') :
                print 'uncrash_poc_scan Success .. '
                send_result(uncrash_poc_valid_logic.LOCAL_BIND_PORT,log_data_)
            else :
                print 'crash_poc_scan Success .. '
                send_result(crash_poc_valid_logic.LOCAL_BIND_PORT,log_data_)
        else :
            print log_data_
        
        
def send_result(port,data) :
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(data,('127.0.0.1',port))
    sock.close()
        
def listen(port_args) :
#    try :
        handler = [
            (r'/uncrash_scan',uncrash_handle),
            (r'/uncrash_poc', read_poc_handle),
            (r'/crash_poc',   read_poc_handle),
            (r'/report',      report_handle),
        ]
        http_server = tornado.web.Application(handlers=handler)
        http_server.listen(port_args)
        tornado.ioloop.IOLoop.current().start()
#    except :
#        print 'WARNING ! Check Port had been Using ..'
    
if __name__=='__main__' :
    listen(LOCAL_BIND_PORT)
    
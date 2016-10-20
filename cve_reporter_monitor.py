
import json
import requests


def dump_page(url) :
    request_data=requests.get(url,verify=False)

    if 200==request_data.status_code :
        return request_data.text

    return None
    
def update_new_cve_list() :
    pass

def try_to_read_cve() :
    cve_link_file=open('cve-data.json')
    
    if cve_link_file :
        cve_link_list=None
    
        try :
            cve_link_list=json.loads(cve_link_file.read())
        except :
            print 'cve-data.json File data error ..'
            exit()
    
        for cve_link_index in cve_link_list :
            dump_page(cve_link_index)

if __name__=='__main__' :
#    try_to_read_cve()
    dump_page('https://bugs.chromium.org/p/project-zero/issues/detail?id=878')
            
            
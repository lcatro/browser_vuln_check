
import socket
import urllib

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.bind(('0.0.0.0',80))

sock.listen(1)

while True :
    new_sock,remote_ip=sock.accept()
    if remote_ip[0]=='127.0.0.1' :
        packet=new_sock.recv(512)
        new_sock.send('null')

        json_information=urllib.unquote(packet[packet.find('/log=(')+6:packet.find('HTTP')-2])
        vlun_name=json_information[json_information.find('"')+1:json_information.find(',')-1]
        check_state=json_information[json_information.find(',')+13:-1]
        print vlun_name+' check_state:'+check_state
    new_sock.close()

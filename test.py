#! /bin/python 

import socket
from urlparse import urlparse
import gzip
from StringIO import StringIO
import sys
from time import sleep

TE="Transfer-Encoding: chunked"
CN="Content-Length:"
redirectcount=5
finaldata=''
#remainsize

#url parsing
def inputurlparse (inputurl):
    parsedURL = urlparse(inputurl)
    host=parsedURL.netloc
    path=parsedURL.path
    return host,path

def getheader(inputhost,inputpath,inputmethod,buff):
    cFile=""
    if(inputpath ==''):
	inputpath="/"

    inputhost=inputhost.split(":")
    
    if len(inputhost) > 1:
        conn = socket.create_connection((inputhost[0],inputhost[1])) #connect to the server
    else:
        conn = socket.create_connection((inputhost[0],80))

    header=inputmethod+' '+inputpath+' HTTP/1.1\r\n'+ 'Host: '+inputhost[0]+'\r\n\r\n'
#Send header
    conn.send(header)
#Receive response
    while(1):
        cFile+= conn.recv(buff)
        if "\r\n\r\n" in cFile:
            break; 
    cFile=cFile.split("\r\n\r\n")
    return cFile[0],conn
    

def split(header):
    firstLine=str(header).split(' ')
    output= str(firstLine[1])
    return output


def nonchunked(chunkp,en):
    global finaldata
    chunkp.settimeout(2)
    while(1):
        try:
            data=chunkp.recv(4096)
        except socket.timeout, e:
            err = e.args[0]
            if err == 'timed out':
                sleep(1)                                
                chunkp.close()
                sys.stdout.write(finaldata)
                sys.exit(0)
            else:
                print e
                sys.exit(1)            
        if len(data) == 0:
            if(en=="non chunked encoding"):
                chunkp.close()  
                sys.stdout.write(finaldata)
                sys.exit(0)               
            else:
                print 'orderly shutdown on server end'
                chunkp.close()
                sys.exit(0)
        else:          
            finaldata=finaldata+data
   
def chunkencode(chunkp,en,leftover):
    data=""
    left=leftover
    global finaldata
    while(left>0):
        data+=chunkp.recv(1)
        left=leftover-len(data) 
    finaldata+=data
    return chunkp
    #print finaldata        


#if TE in header:
        
def main(method,url):
    host,path=inputurlparse(url)   
    header,sockp=getheader(host,path,method,1)
    output=split(header)
    #print header     
    if output=='200':
        if TE in header:
            sockp.settimeout(2)
            global finaldata
            while(1):
                try:
                      
                    finalp=chunkencode(sockp,"chunked encoding",leftover+4)
                except socket.timeout,e:
                    err=e.args[0]
                    if err=='timed out':
                        finalp.close()
                        sys.stdout.write(finaldata)
                        sys.exit(0) 
	else:        
            nonchunked(sockp,"non chunked encoding")

           
                     
    if output in ['301','302','303','307']:  #Handling Re-directs
        global redirectcount
        redirectcount-=1
        if(redirectcount==0):
            sys.exit(1)
	redirect=str(header).split('\r\n')
        redirecturl=str(redirect[1])
	redirecturl=str(redirecturl).split(" ")   	  
        reredirecturl= redirecturl[1] 
        sockp.close()
        main(method,reredirecturl)
    
    output=int(outpt)
    output=output/100
    sys.exit(output) 
        



if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])




#Unzip body

#dFile=gzip.GzipFile(fileobj=StringIO(body)).read()












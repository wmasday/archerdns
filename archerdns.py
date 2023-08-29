from multiprocessing.dummy import Pool
from lib.subdomain import Subdomain
from lib.reverseip import ReverseIP
import os

banner = '''
@trustsec;

[ 1 ] Subdomain Finder
[ 2 ] Reverse IPs - Use Domain
'''

def clear():
    try:
        os.system('clear')
    except:
        os.system('cls')
        
def subdomain(domain):
    try:
        subdo = Subdomain(domain)
        subdo.rasenmedia()
        subdo.dnsdumpster()
        subdo.crtsh()
        subdo.alienvault()
        subdo.rapiddns()
        subdo.securitytrails()
        subdo.hackertarget()
    except:pass
    
def reverseip(domain):
    try:
        reverse = ReverseIP(domain)
        reverse.rapiddns()
    except:pass

    
def archerdns():
    clear()
    print (banner)
    option = input("[?] Option : ")
    
    clear()
    filename = input("[?] List   : ")
    domain = open(filename, 'r', encoding='utf8').read().splitlines()
    
    try:
        pp = Pool(10)
        if int(option) == 1:
            pp.map(subdomain, domain)
        elif int(option) == 2:
            pp.map(reverseip, domain)
        else:
            archerdns()
    except:
        pass

if __name__ == '__main__':
    archerdns()
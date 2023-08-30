from multiprocessing.dummy import Pool
from lib.subdomain import Subdomain
from lib.reverseip import ReverseIP
from lib.history import History
import os

banner = '''
@trustsec;

[ 1 ] Subdomain Finder
[ 2 ] Reverse IPs - Use Domain
[ 3 ] Domain History (IP, IPv6, Hostname, Name Server, Email SOA)
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
    
def reverse(domain):
    try:
        reverser = ReverseIP(domain)
        reverser.rapiddns()
        reverser.rasenmedia()
        reverser.hackertarget()
        reverser.securitytrails()
    except:pass

def history(domain):
    try:
        historier = History(domain)
        historier.securitytrails()
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
            pp.map(reverse, domain)
        elif int(option) == 3:
            pp.map(history, domain)
        else:
            archerdns()
    except:
        pass

if __name__ == '__main__':
    archerdns()
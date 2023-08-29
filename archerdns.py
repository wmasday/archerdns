from multiprocessing.dummy import Pool
import os, re, sys, requests
from lib.subdomain import *
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36'}
timeout = 30

banner = '''
@trustsec;

[ 1 ] Subdomain Finder
[ 2 ] Reverse IPs - RAPIDDNS
[ 3 ] 
'''

def subdomain(domain):
    rapiddns(domain)
    
subdomain('ui.ac.id')
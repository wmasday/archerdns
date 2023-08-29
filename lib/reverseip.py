import os, re, sys, requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class ReverseIP:
    def __init__(self, domain):
        self.domain = domain
        self.headers = {'User-Agent': str(self.ua)}
        self.timeout = 30
    
    def regexers(self, data, filename, platform):
        try:
            lines = list(dict.fromkeys(data))
            print (f'[ {platform} ] {self.domain} get {len(lines)}')
            for line in lines:
                open(filename, 'a').write(line +'\n')
        except:pass
        
    def rapiddns(self):
        try:
            response = requests.get('https://rapiddns.io/sameip/'+ self.domain +'?full=1&down=1#result', headers=self.headers, timeout=self.timeout).text
            domains = re.findall(r'</th>\n<td>(.*?)</td>', response)
            self.regexers(domains, 'domain.txt', 'RAPIDDNS SUBDOMAIN')

            ips = re.findall(r'same ip website reverse ip">(.*?)</a>', response)
            self.regexers(ips, 'rapiddns-ip.txt', 'RAPIDDNS')
        except:pass
        
    def rasenmedia(self):
        try:
            data = {'input': self.domain, 'execute': 'Reverse'}
            response = requests.post('https://rasenmedia.my.id/tools/networking/reverse-ip', headers=self.headers, data=data, timeout=self.timeout).text
            soup = BeautifulSoup(response, 'html.parser')
            domains = soup.find('textarea',{'class':'form-control'}).text
            if 'Not Found!' in domains:
                return False
            
            domains = domains.split('\n')
            domains = list(filter(None, domains))
            self.regexers(domains, 'domain.txt', 'RASENMEDIA')
        except:pass
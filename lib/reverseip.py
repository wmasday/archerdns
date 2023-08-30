import os, re, sys, requests, cloudscraper
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
scraper = cloudscraper.create_scraper()

class ReverseIP:
    def __init__(self, domain):
        self.domain = domain
        self.ua = UserAgent()
        self.headers = {'User-Agent': str(self.ua)}
        self.timeout = 30
        self.path = open('securitytrails.path', 'r').read()
        
    def regexers(self, data, filename, platform):
        try:
            lines = list(dict.fromkeys(data))
            print (f'[ {platform} ] {self.domain} get {len(lines)}')
            for line in lines:
                open(filename, 'a').write(line +'\n')
        except:pass
    
    def ipCheck(self):
        return self.domain.replace('.', '').isnumeric()
    
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
    
    def hackertarget(self):
        try:
            domains = []
            response = scraper.get('https://api.hackertarget.com/reverseiplookup/?q='+ self.domain, headers=self.headers, timeout=self.timeout).text
            
            if 'API count exceeded' in response:
                return False
            else:pass
            
            response = response.split('\n')
            response = list(filter(None, response))
            self.regexers(domains, 'domain.txt', 'HACKERTARGET')
        except:pass
    
    def securitytrails(self):
        try:
            if self.ipCheck() == False:
                return False
            else:pass
            
            response = scraper.get('https://securitytrails.com/_next/data/'+ self.path +'/list/ip/'+ self.domain +'.json?ip='+ self.domain, headers=self.headers, timeout=self.timeout).text
            if '<title>Just a moment...</title>' in response:
                return False
            else:pass
            
            domains = re.findall('"hostname":"(.*?)","mail', response)
            self.regexers(domains, 'domain.txt', 'SECURITYTRAILS')
            
            max = re.findall('"pages":(.*?),"records"', response)[0]
            if int(max) == 1:
                return True
            else:pass
            
            for page in range(1, int(max + 1)):
                response = scraper.get('https://securitytrails.com/_next/data/'+ self.path +'/list/ip/'+ self.domain +'.json?page='+ page +'&ip='+ self.domain, headers=self.headers, timeout=self.timeout).text
                if '<title>Just a moment...</title>' in response:
                    return False
                else:pass
                
                domains = re.findall('"hostname":"(.*?)","mail', response)
                self.regexers(domains, 'domain.txt', 'SECURITYTRAILS')
                
        except:pass
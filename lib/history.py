import os, re, sys, requests, cloudscraper
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
scraper = cloudscraper.create_scraper()

class History:
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
    
    def ips(self, data):
        try:
            ips = re.findall('"ip":"(.*?)","ip_count"', data)
            self.regexers(ips, 'securitytrails-ip.txt', 'SECURITYTRAILS IP')
        except:pass

    def ipv6(self, data):
        try:
            ipv6 = re.findall('"ipv6":"(.*?)","ipv6_count"', data)
            self.regexers(ipv6, 'securitytrails-ipv6.txt', 'SECURITYTRAILS IPv6')
        except:pass

    def host(self, data):
        try:
            host = re.findall('"host":"(.*?)","mx_count"', data)
            self.regexers(host, 'securitytrails-host.txt', 'SECURITYTRAILS HOST')
        except:pass

    def nameserver(self, data):
        try:
            nameserver = re.findall('"nameserver":"(.*?)","nameserver_count"', data)
            self.regexers(nameserver, 'securitytrails-ns.txt', 'SECURITYTRAILS NS')
        except:pass

    def email(self, data):
        try:
            email = re.findall('"email":"(.*?)","email_count"', data)
            self.regexers(email, 'securitytrails-email.txt', 'SECURITYTRAILS SOA')
        except:pass
        
    def securitytrails(self):
        try:
            types = ['a', 'aaaa', 'mx', 'ns', 'soa']
            for type in types:
                response = scraper.get('https://securitytrails.com/_next/data/'+ self.path +'/domain/'+ self.domain +'/history/'+ type +'.json?domain='+ self.domain +'&type='+ type, headers=self.headers, timeout=self.timeout).text
                if '<title>Just a moment...</title>' in response:
                    return False
                else:pass

                self.email(response)
                self.nameserver(response)
                self.host(response)
                self.ipv6(response)
                self.ips(response)

                max = re.findall('"pages":(.*?),"records"', response)[0]
                if int(max) == 1:
                    return True
                else:pass

                for page in range(1, int(max + 1)):
                    response = scraper.get('https://securitytrails.com/_next/data/'+ self.path +'/domain/'+ self.domain +'/history/'+ type +'.json?page='+ page +'&domain='+ self.domain +'&type='+ type, headers=self.headers, timeout=self.timeout).text
                    if '<title>Just a moment...</title>' in response:
                        return False
                    else:pass
                    
                    self.email(response)
                    self.nameserver(response)
                    self.host(response)
                    self.ipv6(response)
                    self.ips(response)
                
        except:pass
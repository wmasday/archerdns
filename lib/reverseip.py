import os, re, sys, requests

class ReverseIP:
    def __init__(self, domain):
        self.domain = domain
        self.headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36'}
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
            self.regexers(ips, 'rapiddns-ip.txt', 'RAPIDDNS IP')
        except:pass


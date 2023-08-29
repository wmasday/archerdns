import os, re, sys, requests

class Subdomain:
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

    def alienvault(self):
        try:
            response = requests.get('https://otx.alienvault.com/api/v1/indicators/domain/'+ self.domain +'/passive_dns', headers=self.headers, timeout=self.timeout).text
            regex = re.findall(r'"hostname": "(.*?)", "record_type"', response)
            self.regexers(regex, 'domain.txt', 'ALIENVAULT')
        except:pass

    def crtsh(self):
        try:
            response = requests.get('https://crt.sh/?q='+ self.domain +'&output=json', headers=self.headers, timeout=self.timeout).text
            regex = re.findall(r'"common_name":"(.*?)","name_value"', response)
            self.regexers(regex, 'domain.txt', 'CRT.sh')
        except:pass

    def dnsdumpster(self):
        try:
            sess = requests.session()
            tokenGet = sess.get('https://dnsdumpster.com/')
            cookies = tokenGet.cookies.get_dict()
            csrftoken = cookies['csrftoken']
            token = re.findall('name="csrfmiddlewaretoken" value="(.*?)"', tokenGet.text)[0]

            data = {"csrfmiddlewaretoken": token, "targetip": self.domain, "user": "free"}
            dnsdumpsterHeaders = {"csrftoken": csrftoken, "Referer": "https://dnsdumpster.com/"}

            response = sess.post('https://dnsdumpster.com/', headers=dnsdumpsterHeaders, data=data, timeout=self.timeout).text
            domains = re.findall(r'httpheaders/\?q=http://(.*?)" data-target="#myModal"', response)
            self.regexers(domains, 'domain.txt', 'DNSDUMPSTER SUBDOMAIN')

            ips = re.findall(r'mtr/\?q=(.*?)" data-target="#myModal"', response)
            self.regexers(ips, 'ip.txt', 'DNSDUMPSTER IP')
        except:pass

    def rapiddns(self):
        try:
            response = requests.get('https://rapiddns.io/subdomain/'+ self.domain +'?full=1&down=1#result', headers=self.headers, timeout=self.timeout).text
            domains = re.findall(r'</th>\n<td>(.*?)</td>', response)
            self.regexers(domains, 'domain.txt', 'RAPIDDNS SUBDOMAIN')
        except:pass


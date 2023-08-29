from multiprocessing.dummy import Pool
import os, re, sys, requests

headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36'}
timeout = 30

def regexers(domain, data, filename):
    try:
        lines = list(dict.fromkeys(data))
        print (f'[!] Saving {len(lines)} data from {domain}')
        for line in lines:
            open(filename, 'a').write(line +'\n')
    except:pass

def alienvault(domain):
    try:
        response = requests.get('https://otx.alienvault.com/api/v1/indicators/domain/'+ domain +'/passive_dns', headers=headers, timeout=timeout).text
        regex = re.findall(r'"hostname": "(.*?)", "record_type"', response)
        regexers(domain, regex, 'domain.txt')
    except:pass

def crtsh(domain):
    try:
        response = requests.get('https://crt.sh/?q='+ domain +'&output=json', headers=headers, timeout=timeout).text
        regex = re.findall(r'"common_name":"(.*?)","name_value"', response)
        regexers(domain, regex, 'domain.txt')
    except:pass

def dnsdumpster(domain):
    try:
        sess = requests.session()
        tokenGet = sess.get('https://dnsdumpster.com/')
        cookies = tokenGet.cookies.get_dict()
        csrftoken = cookies['csrftoken']
        token = re.findall('name="csrfmiddlewaretoken" value="(.*?)"', tokenGet.text)[0]
        
        data = {"csrfmiddlewaretoken": token, "targetip": domain, "user": "free"}
        dnsdumpsterHeaders = {
			"csrftoken": csrftoken,
			"Referer":"https://dnsdumpster.com/"
		}
        
        response = sess.post('https://dnsdumpster.com/', headers=dnsdumpsterHeaders, data=data, timeout=timeout).text
        domains = re.findall(r'httpheaders/\?q=http://(.*?)" data-target="#myModal"', response)
        regexers(domain, domains, 'domain.txt')
        
        ips = re.findall(r'mtr/\?q=(.*?)" data-target="#myModal"', response)
        regexers(domain, ips, 'ip.txt')
    except:pass

def rapiddns(domain):
    try:
        response = requests.get('https://rapiddns.io/subdomain/'+ domain +'?full=1&down=1#result', headers=headers, timeout=timeout).text
        domains = re.findall(r'</th>\n<td>(.*?)</td>', response)
        regexers(domain, domains, 'domain.txt')
        
        ips = re.findall(r'same ip website">(.*?)</a>', response)
        regexers(domain, ips, 'rapiddns-ip.txt')
    except:pass


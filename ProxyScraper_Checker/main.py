import requests
import time
import re
import paramiko

# URL TO SCRAPE PROXIES
urls = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "http://www.example2.com/proxies",
    "http://www.example3.com/proxies",
    "http://www.example4.com/proxies",
]

proxies = []
for url in urls:
    response = requests.get(url)

    if response.status_code == 200:
        extracted_proxies = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}\b", response.text)
        proxies.extend(extracted_proxies)

check_url = "https://www.google.com/"
good_proxies = []

for proxy in proxies:
    start = time.time()
    try:
        response = requests.get(check_url, proxies={"http": proxy})
        if response.status_code == 200:
            good_proxies.append(proxy)
            print(f"Proxy {proxy} is working! Response time: {(time.time() - start) * 1000:.2f}ms")
    except:
        print(f"Proxy {proxy} is not working.")
with open("good_proxies.txt", "w") as f:
    for proxy in good_proxies:
        f.write(f"{proxy}\n")

print(f"{len(good_proxies)} good proxies have been saved to good_proxies.txt")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("IP", port=22, username="root", password="PASSWORD")

sftp = ssh.open_sftp()
sftp.put("good_proxies.txt", "/home/narul/good_proxies.txt")
sftp.close()

ssh.close()

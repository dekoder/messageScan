import requests
from bs4 import BeautifulSoup
import time

from threading import Thread


class IPBox:
    def __init__(self):
        self.proxy_check = Google_Proxy_Check()
        self.ip_check = Google_IP_Check()

    def get(self, check):
        if check == "proxy":
            return self.proxy_check.work_proxy
        elif check == "ip":
            return self.ip_check.work_ip



class Google_Proxy_Check:
    """
    #   work_ip: return the ip proxy which can connect google
    #            as (host,port)
    #            if there is no work ip, return ()
    """

    def __init__(self):
        self.__proxies = {}
        self.__ip_list = self.__page_1()
        self.__current_ip_num = 0
        self.work_proxy = ()
        Thread(target=self.__find_work_proxy).start()

    def __page_1(self):

        """
        #   use www.google-proxy.net
        #   return ip list [(ip, port) ... ]
        """

        proxy_page = "http://www.google-proxy.net"
        r = requests.get(proxy_page)
        if r.status_code != requests.codes.ok:
            return []
        soup = BeautifulSoup(r.text)
        ip_addrs = soup.find(id="proxylisttable").tbody.find_all("tr")
        ip_list = []
        for ip_addr in ip_addrs:
            ip_list.append((ip_addr.contents[0].text, ip_addr.contents[1].text))
        return ip_list

    def __get_work_proxy(self):
        if not self.__ip_list:
            return ()

        timeout = 1
        while timeout < 10:
            while self.__current_ip_num < len(self.__ip_list):
                current_ip = self.__ip_list[self.__current_ip_num]
                try:  
                    if self.__check_ip(current_ip, timeout):
                        return current_ip
                except:
                    pass
                self.__current_ip_num += 1
                #print "in __get_work_proxy",self.__current_ip_num 

            self.__current_ip_num = 0
            #print "not found, add timeout"
            timeout += 1

            #print "timeout:",timeout
        return ()

    def __find_work_proxy(self):
        while True:
            self.work_proxy = self.__get_work_proxy()
            #print "proxy:", self.work_proxy
            #print self.work_proxy
            time.sleep(30)


    def __check_ip(self, ip, timeout):
        r = requests.get(
                "http://www.google.com",
                proxies = {"http":ip[0]+":"+ip[1],},
                timeout = timeout
            )
        if r.status_code == 200:
            return True
        else:
            return False

class Google_IP_Check:
    """
    #   work_ip: return the ip which can work
    #            as "ip"
    #            if there is no work ip, return ""
    """

    def __init__(self):
        self.work_ip = ""
        self.__current_ip_num = 0
        Thread(target=self.__find_work_ip).start()

    def __find_work_ip(self):
        while True:
            self.work_ip = self.__get_work_ip()
            #print self.work_ip
            time.sleep(30)

    def __get_work_ip(self):

        ip_table = [ 
                    "1.179.248.105","210.61.221.166","218.176.242.20","1.179.250.89","149.126.86.7",
                    "1.179.248.12","1.179.248.184","84.235.77.76","41.84.159.12","60.199.175.93",
                    "218.176.242.148","1.179.250.236","202.39.143.115","62.201.216.244","60.199.175.100",
                    "60.199.175.6","118.174.25.74","1.179.251.116","197.199.253.50","62.197.198.228",
                    "111.92.162.13","1.179.250.92","1.179.249.241","60.199.175.58","210.61.221.105",
                    "41.206.96.97","118.174.25.53","1.179.252.112","62.197.198.231","203.66.124.139",
                    "93.123.23.58","163.28.83.164","123.205.251.118","210.61.221.165","218.176.242.204",
                    "1.179.249.231","1.179.252.154","60.199.175.12","41.206.96.124","41.206.96.14",
                    "218.189.25.165","1.179.252.107","203.211.0.59","118.174.25.96","87.244.198.178",
                    "203.116.165.181","118.174.25.216","178.45.251.8","93.123.23.17","1.179.252.105",
                    "103.25.178.53","118.174.25.243","118.174.25.81","1.179.252.119","203.66.124.246",
                    "149.126.86.49","178.45.251.5","60.199.175.132","218.189.25.133","93.123.23.54",
                    "1.179.250.205","62.201.216.205","203.66.124.171","93.123.23.43","41.206.96.187",
                    "121.78.74.110","218.176.242.41","118.174.25.29","197.199.254.24","87.244.198.186",
                    "1.179.252.242","41.206.96.229","41.206.96.186","1.179.251.26","210.61.221.72",
                    "203.66.124.211","202.39.143.48","41.206.96.205","1.179.248.224","197.199.254.55",
                    "210.61.221.160","1.179.253.50","1.179.252.225","1.179.250.138","218.176.242.5",
                    "203.66.124.173","84.235.77.210","1.179.248.58","210.61.221.76","88.159.13.209",
                    "62.197.198.238","1.179.251.237","84.235.77.48","218.176.242.50","203.117.34.181",
                    "210.61.221.170","178.45.251.103","1.179.252.181","1.179.248.25","123.205.250.86",
                    "203.211.0.41","203.116.165.185","218.189.25.174","178.45.251.85","123.205.251.84",
                    "218.253.0.171","93.123.23.7","1.179.251.238","203.211.0.49","1.179.250.41","218.176.242.164",
                    "1.179.251.222","178.45.251.6","103.25.178.54","163.28.116.16","88.159.13.223",
                    "210.61.221.95","121.78.74.109","1.179.253.109","149.126.86.53","218.189.25.136",
                    "60.199.175.81","123.205.250.186","88.159.13.229","1.179.253.105","218.176.242.13",
                    "41.206.96.152","84.235.77.218","93.123.23.55","93.123.23.25","163.28.116.38","88.159.13.240",
                    "203.116.165.135","218.176.242.117","61.219.131.117","218.176.242.138","1.179.249.94",
                    "218.176.242.32","203.211.0.23","93.123.23.31","84.235.77.57","1.179.249.238","203.66.124.132",
                    "41.206.96.248","41.206.96.194","178.45.251.58","41.206.96.179","203.66.124.157","1.179.248.95",
                    "88.159.13.207","1.179.251.205","1.179.249.186","218.189.25.183","210.61.221.69","111.92.162.25",
                    "84.235.77.92","1.179.251.32","178.45.251.110","60.199.175.89","121.78.74.107","118.174.25.14",
                    "1.179.253.25","41.206.96.66","118.174.25.168","1.179.249.22","178.45.251.107","123.205.250.91",
                    "93.123.23.38","178.45.251.98","218.253.0.86","41.206.96.141","203.117.34.170","1.179.253.122",
                    "84.235.77.27","1.179.251.146","1.179.249.32","218.253.0.156","1.179.248.9","1.179.250.114",
                    "118.174.25.164","218.176.242.231","218.176.242.242","62.201.216.217","60.199.175.96","62.197.198.248",
                    "1.179.248.31","197.199.253.53","1.179.248.210","60.199.175.117","60.199.175.143","1.179.252.106",
                    "1.179.250.234","1.179.248.211","111.92.162.17","121.78.74.91","60.199.175.173","203.116.165.242",
                    "203.66.124.133","203.66.124.207","84.235.77.102","118.174.25.107","197.199.254.27","111.92.162.30",
                    "218.176.242.27","203.117.34.164","1.179.252.114","1.179.249.214","202.39.143.108","1.179.250.177",
                    "1.179.251.40","203.211.0.16","61.219.131.210","202.39.143.42","1.179.250.123","163.28.83.157",
                    "123.205.250.145","84.235.77.10","1.179.251.228","197.199.253.42","84.235.77.162","210.61.221.82",
                    "218.176.242.18","203.116.165.214","203.211.0.43","60.199.175.47","210.61.221.136","1.179.251.240",
                    "1.179.252.226","202.39.143.9","1.179.251.251","1.179.248.160","1.179.251.22","1.179.250.52",
                    "118.174.25.132","163.28.83.159","1.179.251.78","118.174.25.158","218.176.242.230","218.189.25.184",
                    "1.179.253.18","149.126.86.46","1.179.251.123","84.235.77.17","41.206.96.21","203.66.124.135",
                    "203.116.165.159","93.123.23.27","178.45.251.87","210.61.221.122","62.197.198.242","197.199.254.16",
                    "218.176.242.234","1.179.249.249","62.201.216.207","84.235.77.158","84.235.77.90","1.179.250.182",
                    "210.61.221.68","1.179.249.26","41.206.96.89","41.206.96.46","163.28.83.179","87.244.198.179",
                    "203.66.124.239","41.206.96.52","123.205.251.89","210.61.221.109","210.61.221.159","218.176.242.29",
                    "41.206.96.189","87.244.198.182","121.78.74.70","1.179.252.158","118.174.25.70","203.66.124.213",
                    "173.194.130.4","91.213.30.152","91.213.30.151","91.213.30.150"
                    ]

        timeout = 1
        while timeout < 8:
            while self.__current_ip_num < len(ip_table):
                current_ip = ip_table[self.__current_ip_num]
                try:
                    if self.__check_ip(current_ip, timeout):
                        #print current_ip
                        return current_ip
                except:
                    pass
                self.__current_ip_num += 1
                #print self.__current_ip_num 
            self.__current_ip_num = 0
            #print "not found, add timeout"
            timeout += 1

            #print "timeout:",timeout
        return ""

    def __check_ip(self, ip, timeout):

        headers = {
                  "Content-Type":"application/x-www-form-urlencoded",
                  "Connection":"Keep-Alive",
                  "Referer":'http://www.taobao.com',
                  "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1284.2 Safari/537.13",  
                }

        r = requests.get(
                "http://"+ip,
                timeout = timeout,
                headers = headers
            )
        if r.status_code == 200:
            return True
        else:
            return False


if __name__ == "__main__":
    #proxy_check = Google_Proxy_Check()
    ip_check = Google_IP_Check()
    while True:
        print ip_check.work_ip
        #print proxy_check.work_ip
        time.sleep(5)
    #print check.get_work_proxy()




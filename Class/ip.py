import os.path, urllib.request, gzip, shutil, netaddr, socket, struct, re
from operator import itemgetter
from os import path

subnets = []

class IP:
    def __init__(self):
        print("### Loading IP ###")
        if not path.exists("routeviews.pfx2as"):
            print("Downloading routeviews.pfx2as")
            url = "http://data.caida.org/datasets/routing/routeviews-prefix2as/2020/09/routeviews-rv2-20200908-1000.pfx2as.gz"
            urllib.request.urlretrieve (url, "routeviews.pfx2as.gz")
            with gzip.open('routeviews.pfx2as.gz', 'rb') as f_in:
                with open('routeviews.pfx2as', 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        print("Loading Subnets")
        with open('routeviews.pfx2as', 'r') as file:
            data = file.read()
        parsed = re.findall("([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).([0-9]+)",data, re.MULTILINE)
        parsed = sorted(parsed,key=lambda x: int(x[1]), reverse=True)
        splitted = {}
        for entry in parsed:
            index = self.getFirstBlock(entry[0])
            if int(entry[1]) <= 24:
                try:
                    tmp = splitted[index]
                    tmp = tmp + (entry,)
                    splitted[index] = tmp
                except:
                    splitted[index] = {}
                    splitted[index] = (entry,)
        global subnets
        subnets = splitted

    def Router(self,addresses):
        routerIPs = []
        for address in addresses:
            raw = re.sub('[0-9]+$', '', address[0])
            routerIPs.append(raw+"1")
            routerIPs.append(raw+"254")
            routerIPs.append(raw+"10")
            routerIPs.append(address[0])
        return routerIPs

    def getFirstBlock(self,ip):
        index = re.findall("^([0-9]+)\.",ip)
        index = int(index[0])
        return index

    def resolve(self,ip,range,netmask):
        rangeDecimal = int(netaddr.IPAddress(range))
        ipDecimal = int(netaddr.IPAddress(ip))
        wildcardDecimal = pow( 2, ( 32 - int(netmask) ) ) - 1
        netmaskDecimal = ~ wildcardDecimal
        return ( ( ipDecimal & netmaskDecimal ) == ( rangeDecimal & netmaskDecimal ) );

    def lookup(self,target):
        print("Looking up",target)
        index = self.getFirstBlock(self,target)
        global subnets
        try:
            for subnet in subnets[index]:
                match = self.resolve(self,target,subnet[0],subnet[1])
                if match == True: return subnet
            print("Could not lookup IP")
            return False
        except:
            print(target,"not found")
            return False

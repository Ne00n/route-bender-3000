#Route Bender Runner
import subprocess, re, sys

gateways = ['10.0.1.1','10.0.1.2','10.0.1.3','10.0.1.4','10.0.1.5','10.0.1.6','10.0.1.7','10.0.1.8','10.0.1.9','10.0.1.11']

class Runner:
    def ping(self,ip):
        try:
            result = subprocess.check_output(["ping", "-c", "5", ip])
            m = re.findall("mdev =.*?/([0-9]+.[0-9]+)",result.decode('utf-8'))
            return m[0]
        except:
            return 400

    def findLowest(self,list):
        lowest = []
        i = 0
        while i < len(list):
            if not lowest: lowest = list[i]
            if float(list[i][1]) < float(lowest[1]): lowest = list[i]
            i += 1
        return lowest

    def run(self,subnet,ip,ms):
        print("Route Bender Runner")
        results = []
        for target in gateways:
            subprocess.run(['ip','route','add',ip+'/32','via',target,'dev','vpncloud0','table','BENDER'])
            rtt = self.ping(ip)
            results.append([target,rtt])
            subprocess.run(['ip','route','del',ip+'/32','via',target,'dev','vpncloud0','table','BENDER'])
            print("Bending traffic to",target,"got",rtt,"ms")
        lowest = self.findLowest(results)
        diff = int(ms) - float(lowest[1])
        if diff < 1 and diff > 0:
            print("Difference less than 1ms, skipping",int(ms),"vs",float(lowest[1]),"for",ip)
        elif diff < 1:
            print("Direct route is better, keeping it for",ip,"Lowest we got",float(lowest[1]),"ms vs",int(ms),"ms direct")
        elif float(lowest[1]) < int(ms):
            print("Routed",ip,"via",lowest[0],"improved latency by",diff,"ms")
            subprocess.run(['ip','route','add',subnet,'via',lowest[0],'dev','vpncloud0','table','BENDER'])

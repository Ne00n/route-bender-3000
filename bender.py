#Route Bender 3000
import subprocess, ipaddress, json, time, re, sys
from multiprocessing import Process
from Class.runner import Runner
from Class.ip import IP
routed = []

#echo '333 BENDER' >> /etc/iproute2/rt_tables

def getIPs(interface):
    result = subprocess.run(['timeout','3','tcpdump','-n','-e','-q','-i',interface], stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    m = re.findall("> ([0-9]+.[0-9]+.[0-9]+.[0-9]+)",result.stdout.decode('utf-8'))
    for element in m[:]:
        if ipaddress.ip_address(element).is_private or getCount(m,element) > 1: m.remove(element)
    return m

def getCount(ips,target):
    count = 0
    for ip in ips:
        if ip == target:
            count = count +1
    return count

def pingAll(ping):
    result = subprocess.run(ping, stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    m = re.findall('([0-9.]+) ping.*?(100.00%|median = ([0-9]+))',result.stdout.decode('utf-8'), flags=re.DOTALL)
    for entry in m[:]:
        if entry[1] == "100.00%":
            m.remove(entry)
            print('Dropped',entry[0],"no reply")
    return m

def init():
    print("Flushing Routing Table...")
    subprocess.run(['ip', 'route', 'flush','table','BENDER'])
    ip = IP()

def check(interface):
    global routed
    print("Loading nodes")
    with open('nodes.json') as handle:
        gateways = json.loads(handle.read())
    print("Fetching Outbound IP's")
    ips = getIPs(interface)
    print("Got",len(ips),"addresse(s)")
    print("Resolve Subnets")
    addresses =  []
    for ip in ips:
        data = IP.lookup(IP,ip)
        if not data == False:
            subnet = data[0]+"/"+data[1]
            if not subnet in routed:
                addresses.append([ip,data[0],data[1]])
                routed.append(subnet)
        else:
            print(ip,"no match")
    print("Getting Router IP's")
    routerIPs = IP.Router(IP,addresses)
    ping = ["oping", "-c", "8"]
    ping.extend(routerIPs)
    print("Getting Latency from all IP's")
    response = pingAll(ping)
    print("Grouping results")
    latency = []
    lastRow = ""
    for entry in response:
        data = IP.lookup(IP,entry[0])
        subnet = data[0]+"/"+data[1]
        if subnet != lastRow:
            row = (data[0]+"/"+data[1],entry[0],entry[2])
            latency.append(row)
        lastRow = subnet
    print("Got",len(latency),"answer(s)")
    print("Lets do some bending")
    runner = Runner()
    for element in latency:
        p = Process(target=runner.run, args=(element[0],element[1],element[2],gateways))
        p.start()
        print("Launched",element[0])

print("Route Bender 3000")
if sys.version_info[0] < 3:
    raise Exception("Python 3 needed.")
interface = sys.argv[1]
init()
while True:
    check(interface)
    print("Running again in 120 seconds")
    time.sleep(120)

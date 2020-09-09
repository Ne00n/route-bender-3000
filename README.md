Who needs BGP when you got Route Bender 3000<br />
JUST BEND YOUR WAY DoWN YOUr DESTINY

**Why**<br />
Getting lower latency while gaming online

**Setup**<br />
[Wireguard](https://github.com/wireguard) as transport network + entry point<br />
Wireguard + route bender 3000 running on RPi4, Windows client connects to it

**Prepare**<br />
echo '333 BENDER' >> /etc/iproute2/rt_tables<br />
rename nodes.example.json to nodes.json

**Dependencies**<br />
pip3 install netaddr<br />
apt-get install -y oping tcpdump

**Enable**<br />
iptables -t nat -A POSTROUTING -o pipe+ -j MASQUERADE<br />
iptables -t nat -A POSTROUTING -o server -j MASQUERADE<br />
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE<br />
ip rule add from 0.0.0.0/0 table BENDER<br />

**Usage**<br />
python3 bender.py server

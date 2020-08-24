Who needs BGP when you got Route Bender 3000<br />
JUST BEND YOUR WAY DoWN YOUr DESTINY

**Why**<br />
Getting lower latency while gaming online

**Setup**<br />
[VpnCloud](https://github.com/dswd/vpncloud) as transport network<br />
[openVPN](https://github.com/Nyr/openvpn-install) as entry point (since VpnCloud does not support Windows)<br />
VpnCloud + openVPN + route bender 3000 running on RPi4, Windows client connects to it

**Enable**<br />
echo '333 BENDER' >> /etc/iproute2/rt_tables (only once)<br />
iptables -t nat -D POSTROUTING -s 10.8.0.0/24 ! -d 10.8.0.0/24 -j SNAT --to-source xx.xx.xx.xx<br />
iptables -t nat -A POSTROUTING -o tun0 -j MASQUERADE<br />
iptables -t nat -A POSTROUTING -o vpncloud0 -j MASQUERADE<br />
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE<br />
ip rule add from 0.0.0.0/0 table BENDER<br />

**Dependencies**<br />
pip3 install netaddr<br />
apt-get install -y oping tcpdump

**Usage**<br />
python3 bender.py tun0

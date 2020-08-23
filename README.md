Who needs BGP when you got Route Bender 3000

Why:<br />
Getting lower latency while gaming online

Setup:<br />
[VpnCloud](https://github.com/dswd/vpncloud) as transport network<br />
[openVPN](https://github.com/Nyr/openvpn-install) as entry point (since VpnCloud does not support Windows)<br />
VpnCloud + openVPN + route bender 3000 runs on RPi4, Windows client connects to it

Dependencies:<br />
pip3 install netaddr<br />
apt-get install -y oping tcpdump

Usage:<br />
python3 bender.py

Who needs BGP when you got Route Bender 3000

Why:<br />
Getting lower latency while gaming online

Setup:<br />
vpnCloud as transport network (multiple machina 10.0.1.x)<br />
openVPN as entry point for Windows machina (server runs on RPi4 same as the script)

Dependencies:<br />
pip3 install netaddr<br />
apt-get install -y oping tcpdump

Usage:<br />
python3 bender.py

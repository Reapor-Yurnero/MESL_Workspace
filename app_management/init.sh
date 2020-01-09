# create a docker bridge network as docker1
docker network create -o "com.docker.network.bridge.name"="docker1" -d bridge --subnet 172.25.0.0/16 isolated_nw

# set up the default firewall rules
# decline any communication with external hosts
iptables -I DOCKER-USER -i docker1 -j DROP

# allow communication with host ephemeral ports
iptables -I INPUT 2 -i docker1 -p udp --match multiport --dport 49152:65535 -j ACCEPT
iptables -I INPUT 2 -i docker1 -p tcp --match multiport --dport 49152:65535 -j ACCEPT

# decline any other communication with host
iptables -A INPUT -i docker1 -j DROP


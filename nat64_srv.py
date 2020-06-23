#!/bin/python3

# pre-req: python3, python3-py3dns, netifaces

import socket
import DNS

# https://stackoverflow.com/questions/16276913/reliably-get-ipv6-address-in-python
def get_ip_6(host, port=0):
     # search for all addresses, but take only the v6 ones
     alladdr = socket.getaddrinfo(host,port)
     ip6 = filter(
         lambda x: x[0] == socket.AF_INET6, # means its ip6
         alladdr
     )
     # if you want just the sockaddr
     return map(lambda x:x[4],ip6)

auto = input("Auto-detect local domain? [y/n]:")

if auto == 'y':
    fqdn = socket.getfqdn()
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    
    print("=========================")
    print("Getting host information:")
    print("-------------------------")
    print("FQDN =", fqdn)
    print("Hostname =", hostname)
    print("IP =", ip)
elif auto == 'n':
    fqdn = input("FQDN: ")
    print("FQDN =", fqdn)
else:
    quit()

print("=========================")
print("Detecting NAT64 via SRV:")
print("-------------------------")

detected = False
dns64 = False
fqdn_bcp = fqdn

# https://stackoverflow.com/questions/1189253/how-do-i-resolve-an-srv-record-in-python
DNS.ParseResolvConf()
srv_req = DNS.Request(qtype = 'srv')

while (not detected) and ("." in fqdn):
    print("Resolving: " + '_nat64._ipv6.' + fqdn + "...")
    srv_result = srv_req.req('_nat64._ipv6.' + fqdn)
        
    for result in srv_result.answers:
        priority, weight, port, pool = result['data']
        #print(pool)
        ipv4 = socket.gethostbyname(pool)
        ipv6 = socket.getaddrinfo(pool, None, socket.AF_INET6)[0][4][0]
        print("NAT64 prefix detected: ", ipv6, "/", port // 100, "tanslated into", ipv4, "/", port % 100, ", priority:", priority, ", weight:", weight)
        detected = True
        
    fqdn = fqdn.split(".",1)[1]

print("-------------------------")
fqdn = fqdn_bcp

if detected:
    print("NAT64 detected!")
    
    print("=========================")
    print("Detecting DNS64 via RFC7050:")
    print("-------------------------")
    try:
        rfc7050 = socket.getaddrinfo("ipv4only.arpa", None, socket.AF_INET6)[0][4][0]
        dns64 = True
    except:
        print("DNS64 not provided by DNS resolver")
        dns64 = False

    if not dns64:
        print("=========================")
        print("Detecting DNS64 via SRV:")
        print("-------------------------")
        
        dns64_udp = False
        dns64_tcp = False
        
        while (not dns64_udp) and ("." in fqdn):
            print("Resolving: " + '_dns64._udp.' + fqdn + "...")
            srv_result = srv_req.req('_dns64._udp.' + fqdn)
        
            for result in srv_result.answers:
                priority, weight, port, pool = result['data']
                ipv6 = socket.getaddrinfo(pool, None, socket.AF_INET6)[0][4][0]
                print("DNS64 detected: ", ipv6, "at UDP port:", port , ", priority:", priority, ", weight:", weight)
                dns64_udp = True
                
            fqdn = fqdn.split(".",1)[1]
            
        fqdn = fqdn_bcp
        
        while (not dns64_tcp) and ("." in fqdn):
            print("Resolving: " + '_dns64._tcp.' + fqdn + "...")
            srv_result = srv_req.req('_dns64._tcp.' + fqdn)
        
            for result in srv_result.answers:
                priority, weight, port, pool = result['data']
                ipv6 = socket.getaddrinfo(pool, None, socket.AF_INET6)[0][4][0]
                print("DNS64 detected: ", ipv6, "at TCP port:", port , ", priority:", priority, ", weight:", weight)
                dns64_tcp = True
                
            fqdn = fqdn.split(".",1)[1]
            
        dns64 = dns64_udp or dns64_tcp
        
        print("-------------------------")
        if dns64:
            print("DNS64 detected!")
        else:
            print("DNS64 not detected!")
        print("=========================")
        
else:
    print("No NAT64 prefix detected.")

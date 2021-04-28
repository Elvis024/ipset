import boto3
import json

local_ips=[]
x=[]

print(x)

IP_LIST = [
    {'ip_set_name':'Test','ip_set_id':'e35fbeff-b614-47ed-b5e4-9b2c1bc7ee4d','text_file':'Admin-Team-IPs.json'},
    {'ip_set_name':'Two','ip_set_id':'827aef16-3c69-4139-81f1-d3bdaa7f52ab','text_file':'iplist.txt'},
    # {'ip_set_name':'DevTeam-IPs','ip_set_id':'72219b31-418f-4fde-baf5-c4c159b15f7b','text_file':'DevTeam-IPs.txt'},
    # {'ip_set_name':'IP-Blacklist','ip_set_id':'e7ebe92e-d0dc-40f1-a981-b12b629fe761','text_file':'IP-Blacklist.txt'},
    # {'ip_set_name':'TravisIPs','ip_set_id':'3c8cfb4d-fe05-4757-8631-ee6917e2b904','text_file':'travis.txt'},
    # {'ip_set_name':'NIH-IPs','ip_set_id':'9dd4bb6b-8f5f-4434-b41d-f14385b02539','text_file':'NIH-IPs.txt'}
]
client = boto3.client('wafv2')

for single_ip in IP_LIST:

    ip_set_name= single_ip['ip_set_name']
    ip_set_id = single_ip['ip_set_id']
    text_file = single_ip['text_file']
    if text_file == 'Admin-Team-IPs.json':
        with open('Admin-Team-IPs.json') as f:
            data = json.loads(f.read())
        for key,value in data.items():
            local_ips.append(value)
    #get the ipset
    elif text_file != 'Admin-Team-IPs.json':
        with open(text_file) as fp:
            c=fp.readlines()
            local_ips=[i.rstrip('\n') for i in c]
    response = client.get_ip_set(
        Name=ip_set_name,
        Scope='REGIONAL',
        Id=ip_set_id
    )

    addresses=response['IPSet']['Addresses']
    LockToken=response['LockToken']

    # local_ips=addresses + local_ips
    # local_ips=list(set(local_ips))

    response = client.update_ip_set(
        Name=ip_set_name,
        Scope='REGIONAL',
        Id=ip_set_id,
        Addresses=local_ips,
        LockToken=LockToken
    )
    completed_text = "IP_SET: {} updated from {}".format(ip_set_name,text_file)
    print(completed_text)

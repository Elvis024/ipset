import boto3
import json

local_ips=[]
local_file=[]
x=[]

print(x)

IP_LIST = [
    {'ip_set_name':'Test','ip_set_id':'e35fbeff-b614-47ed-b5e4-9b2c1bc7ee4d','text_file':'Test.json'},
    {'ip_set_name':'Two','ip_set_id':'827aef16-3c69-4139-81f1-d3bdaa7f52ab','text_file':'Two.txt'},
    {'ip_set_name':'Main','ip_set_id':'1d080a42-9031-462d-8706-facc4fe98654','text_file':'Main.json'},
    {'ip_set_name':'Black','ip_set_id':'e14a3a69-c707-4157-9918-58cc0df9f882','text_file':'Black.txt'},
    # {'ip_set_name':'TravisIPs','ip_set_id':'3c8cfb4d-fe05-4757-8631-ee6917e2b904','text_file':'travis.txt'},
    # {'ip_set_name':'NIH-IPs','ip_set_id':'9dd4bb6b-8f5f-4434-b41d-f14385b02539','text_file':'NIH-IPs.txt'}
]
client = boto3.client('wafv2')
def waf_addips(json_file):
    with open(text_file) as f:
        data = json.loads(f.read())
    for key,value in data.items():
        local_ips.append(value)
    response = client.get_ip_set(
        Name=ip_set_name,
        Scope="REGIONAL",
        Id=ip_set_id
    )
    addresses=response['IPSet']['Addresses']
    LockToken=response['LockToken']

    response = client.update_ip_set(
        Name=ip_set_name,
        Scope='REGIONAL',
        Id=ip_set_id,
        Addresses=local_ips,
        LockToken=LockToken
    )
    completed_text = "IP_SET: {} updated from {}".format(ip_set_name,text_file)
    print(completed_text)
def waf_addips2(text_file):
    with open(text_file) as f:
        data = json.loads(f.read())
    for key,value in data.items():
        local_file.append(value)

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
        Addresses=local_file,
        LockToken=LockToken
    )
    completed_text = "IP_SET: {} updated from {}".format(ip_set_name,text_file)
    print(completed_text)

for single_ip in IP_LIST:

    ip_set_name= single_ip['ip_set_name']
    ip_set_id = single_ip['ip_set_id']
    text_file = single_ip['text_file']
    if text_file == 'Test.json':
        waf_addips('Test.json')


    elif text_file == 'Main.json':
        waf_addips('Main.json')

    #get the ipset
    elif text_file == 'Two.txt':
        waf_addips2('Two.txt')

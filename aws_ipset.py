import boto3
import json
import requests

local_ips=[]
local_file=[]
x=[]

print(x)

IP_LIST = [
    {'ip_set_name':'Test','ip_set_id':'15ae6a00-24ed-45bb-881e-bb3fa8fb6251','text_file':'Test.json'},
    {'ip_set_name':'Two','ip_set_id':'8ea71fdc-d95b-4c26-8ae3-761a1aa56ac8','text_file':'Two.txt'},
    {'ip_set_name':'Main','ip_set_id':'f6156ce7-806d-4358-9107-e3f98f06c99a','text_file':'Main.json'},
    {'ip_set_name':'Black','ip_set_id':'c5e33616-6c34-4942-a38d-e179ca0d2a49','text_file':'Black.txt'},
    {'ip_set_name':'Travis','ip_set_id':'bcd2e88b-2905-411c-8f65-2cf14a4bc766','text_file':'Travis.txt'},
    # {'ip_set_name':'NIH-IPs','ip_set_id':'9dd4bb6b-8f5f-4434-b41d-f14385b02539','text_file':'NIH-IPs.txt'}
]
client = boto3.client('wafv2')




TRAVIS_AWS_DICT =  {'ip_set_name':'Travis','ip_set_id':'bcd2e88b-2905-411c-8f65-2cf14a4bc766'}

#local file for storing travis IPs
text_file = "travis_ip_list.txt"

#travis IP local IP list
travis_ips_local = []

#fetch the IPs from Travis server
TRAVIS_IP_URL = 'https://dnsjson.com/nat.macstadium-us-se-1.travisci.net/A.json'
ip_response = requests.get(TRAVIS_IP_URL)
travis_ip_records = ip_response.json()['results']['records']




##Fetch the IPs in the local file
with open(text_file) as fp:
        c=fp.readlines()
        travis_ips_local =[i.rstrip('\n') for i in c]



"""Compare the local file with the IP addresses on travis server
"""

def update_aws():
    client = boto3.client('wafv2')


    ip_set_name = TRAVIS_AWS_DICT['ip_set_name']
    ip_set_id = TRAVIS_AWS_DICT['ip_set_id']


    #get the ipset and ipset LockToken
    response = client.get_ip_set(
        Name=ip_set_name,
        Scope='REGIONAL',
        Id=ip_set_id
    )

    #aws_addresses=response['IPSet']['Addresses']
    LockToken=response['LockToken']

    #update aws IP set
    response = client.update_ip_set(
        Name=ip_set_name,
        Scope='REGIONAL',
        Id=ip_set_id,
        Addresses=travis_ip_records,
        LockToken=LockToken
    )
    completed_text = "IP_SET: {} updated from TRAVIS server records".format(ip_set_name)
    print(completed_text)

def write_ips_to_local():
    with open(text_file,'w') as fp:
        for elem in travis_ip_records:
            fp.write('{}\n'.format(elem))


if set(travis_ip_records) != set(travis_ips_local):
    update_aws()
    write_ips_to_local()
else:
    print("The local file and travis ips match, no need to update.")

def waf_addips(text_file):
    local_ips = []
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

    #check if the local ips match the aws ips
    #if they don't match update aws

    if set(addresses)!=set(local_ips):
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
    with open(text_file) as fp:
        c=fp.readlines()
        local_text=[i.rstrip('\n') for i in c]
    response = client.get_ip_set(
        Name=ip_set_name,
        Scope='REGIONAL',
        Id=ip_set_id
    )

    addresses=response['IPSet']['Addresses']
    LockToken=response['LockToken']

    # local_ips=addresses + local_ips
    # local_ips=list(set(local_ips))


    #check if local_text match aws addresses
    #if they don't match, update aws
    if set(addresses)!=set(local_text):
        response = client.update_ip_set(
            Name=ip_set_name,
            Scope='REGIONAL',
            Id=ip_set_id,
            Addresses=local_text,
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

    elif text_file == 'Black.txt':
        waf_addips2('Black.txt')

    elif text_file == 'Travis.txt':
        waf_addips2('Travis.txt')

import boto3

#IP SET ID
ip_set_name= 'Two'
ip_set_id= '5f483867-819b-4d7f-b112-5649b7cd0998'

client = boto3.client('wafv2')


#get the ipset
response = client.get_ip_set(
    Name=ip_set_name,
    Scope='REGIONAL',
    Id=ip_set_id
)

addresses=response['IPSet']['Addresses']
LockToken=response['LockToken']

print(addresses)

local_ips=[]

with open('iplist.txt') as fp:
    c=fp.readlines()
    local_ips=[i.rstrip('\n') for i in c]

print(local_ips)
local_ips=addresses + local_ips
local_ips=list(set(local_ips))

response = client.update_ip_set(
    Name=ip_set_name,
    Scope='REGIONAL',
    Id=ip_set_id,
    Addresses=local_ips,
    LockToken=LockToken
)

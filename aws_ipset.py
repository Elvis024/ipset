import boto3


IP_LIST = [
    {'ip_set_name':'Two','ip_set_id':'5f483867-819b-4d7f-b112-5649b7cd0998','text_file':'iplist.txt'},
    {'ip_set_name':'Test','ip_set_id':'e35fbeff-b614-47ed-b5e4-9b2c1bc7ee4d','text_file':'two.txt'}
]
client = boto3.client('wafv2')

for single_ip in IP_LIST:
    ip_set_name= single_ip['ip_set_name']
    ip_set_id = single_ip['ip_set_id']
    text_file = single_ip['text_file']

    #get the ipset
    response = client.get_ip_set(
        Name=ip_set_name,
        Scope='REGIONAL',
        Id=ip_set_id
    )

    addresses=response['IPSet']['Addresses']
    LockToken=response['LockToken']

    local_ips=[]

    with open(text_file) as fp:
        c=fp.readlines()
        local_ips=[i.rstrip('\n') for i in c]

    local_ips=addresses + local_ips
    local_ips=list(set(local_ips))

    response = client.update_ip_set(
        Name=ip_set_name,
        Scope='REGIONAL',
        Id=ip_set_id,
        Addresses=local_ips,
        LockToken=LockToken
    )
    completed_text = "IP_SET: {} updated from {}".format(ip_set_name,text_file)
    print(completed_text)

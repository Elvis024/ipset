import boto3

client = boto3.client('wafv2')

ipvalues=[]

getipset = client.get_ip_set(
    Name='Test',
    Scope='REGIONAL',
    Id='e35fbeff-b614-47ed-b5e4-9b2c1bc7ee4d'
)

oldip=getipset['IPSet']['Addresses']
locktoken=(getipset["LockToken"])

print(getipset["LockToken"])
print(oldip)

for oip in oldip:
        oip = oip.rstrip()
        ipvalues.append(oip)

with open('ip-test.txt') as ip:
  string = ip.readlines()

for line in string:
        line = line.rstrip()
        ipvalues.append(line)

response = client.update_ip_set(
Name='Test',
Scope='REGIONAL',
Id='e35fbeff-b614-47ed-b5e4-9b2c1bc7ee4d',
Description='test',
Addresses=ipvalues,
LockToken=locktoken

"""This program will take the IP SET ID, generate a Change token nad update and ipset"""

"""Update dict is in the format
[
        {
            'Action': 'INSERT'|'DELETE',
            'IPSetDescriptor': {
                'Type': 'IPV4'|'IPV6',
                'Value': 'string'
            }
        },
    ]

"""

import boto3

#IP SET ID
ip_set_id= '9149cc4c-a527-47f4-8c29-b86730edc925'

client = boto3.client('waf-regional')
response = client.get_change_token()
change_token = response['ChangeToken']


updates_dict = [
        {
            'Action': 'INSERT',
            'IPSetDescriptor': {
                'Type': 'IPV4',
                'Value': '192.168.2.5/32'
            }
        },
    ]
ip_set_update = client.update_ip_set(
    IPSetId = ip_set_id,
    ChangeToken=change_token,
    Updates=updates_dict
)
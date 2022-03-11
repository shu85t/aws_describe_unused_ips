# AWS Describe Unused IPs

Python Script that describes the following IPv4 information for the specified Subnet.

- CIDR
- CIDR IPs
- Reserved IPs
- Used IPs (by NetworkInterfaces)
- Unused IPs (= CIDR IPs - Reserved IPs - Used IPs)

# Requirements

- \>Python3.8
- boto3
- AWS Permissions
    - ec2:DescribeSubnets
    - ec2:DescribeNetworkInterfaces

# Usage

```
export AWS_DEFAULT_REGION={region name}
export AWS_DEFAULT_PROFILE={aws profile name}
python describe_unused_ips.py {subnet-id} [lb] 
```

lb = Line Break mode

## e.g.

### Normal mode

```
export AWS_DEFAULT_REGION=ap-northeast-1
export AWS_DEFAULT_PROFILE=my_aws_account
python describe_unused_ips.py subnet-000000000000
```

#### output

```
subnet_id='subnet-000000000000' mode='normal'
cidr='10.1.0.0/24'
cidr_ips=['10.1.0.0', '10.1.0.1', '10.1.0.2', '10.1.0.3', '10.1.0.4', ...]
-----------
reserved_ips=['10.1.0.0', '10.1.0.1', '10.1.0.2', '10.1.0.3', '10.1.0.255']
-----------
used_ips=['10.1.0.39']
-----------
unused_ips=['10.1.0.4', '10.1.0.5', '10.1.0.6', ...]
-----------
cidr=10.1.0.0/24 cidr_ips=256 reserved=5 used=1 unused=250
```

### Line Break mode

```
export AWS_DEFAULT_REGION=ap-northeast-1
export AWS_DEFAULT_PROFILE=my_aws_account
python describe_unused_ips.py subnet-000000000000 lb
```

#### output

```
subnet_id='subnet-0775762f52d4a3bd4' mode='lb'
cidr='10.1.0.0/24'
cidr_ips=
10.1.0.0
10.1.0.1
10.1.0.2
10.1.0.3
10.1.0.4
...
-----------
reserved_ips=
10.1.0.0
10.1.0.1
10.1.0.2
10.1.0.3
10.1.0.255
-----------
used_ips=
10.1.0.39
-----------
unused_ips=
10.1.0.4
10.1.0.5
10.1.0.6
...
-----------
cidr=10.1.0.0/24 cidr_ips=256 reserved=5 used=1 unused=250
```
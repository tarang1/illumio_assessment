# Flow Log Parser

This project processes AWS VPC Flow Logs and maps each entry to tags based on a lookup table.
This is a part of the Illumio coding assessment - `FlowLogProcessor` is the main processor class, this is where the main code lies. I am adding a results.txt, which is generated by running the `main.py`, it demonstrates the correctness of my code.

## Features (Based on the requirements)

- Processes AWS VPC Flow Logs (Version 2)
- Maps flow log entries to tags based on destination port and protocol
- Case-insensitive matching
- Generates statistics for tag counts and port/protocol combinations
- Handles files up to 10MB
- Supports up to 10000 tag mappings

## Usage

```bash
python main.py --input flow_logs.txt --lookup lookup.csv --output results.txt
```

### Input Files

#### Flow Logs
The input flow logs should be in AWS VPC Flow Logs Version 2 format.

Example:
```
2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK
```

#### Lookup Table
The lookup table should be a CSV file with the following columns:
- dstport: Destination port number
- protocol: Protocol name (tcp/udp/icmp)
- tag: Tag to apply

Example:
```csv
dstport,protocol,tag
25,tcp,sv_P1
443,tcp,sv_P2
110,tcp,email
```

### Output

The program generates a text file containing:
1. Count of matches for each tag
2. Count of matches for each port/protocol combination

Example output:
```
Tag Counts:
Tag,Count
sv_P1,10
sv_P2,5
email,3
Untagged,2

Port/Protocol Combination Counts:
Port,Protocol,Count
25,tcp,5
443,tcp,3
110,tcp,2
```

## Testing

Basic Unit Testing - wrote a very basic correctness unit test. 
Run tests using pytest (I used a virtual env for this, would recommend doing the same):
```bash
pytest test_flow_log_processor.py
```
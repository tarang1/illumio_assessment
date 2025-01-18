import csv
import urllib.request
from typing import Dict

def load_iana_protocols() -> Dict[str, str]:
    """Load protocol mappings from IANA's protocol numbers list.
    
    Returns:
        Dict mapping protocol numbers to their names.
    """
    url = "https://www.iana.org/assignments/protocol-numbers/protocol-numbers-1.csv"
    protocols = {}
    
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8').splitlines()
            reader = csv.reader(content)
            next(reader)  # Skip header row
            
            for row in reader:
                if row and len(row) >= 2 and row[0].strip() and row[1].strip():
                    protocol_number = row[0].strip()
                    protocol_name = row[1].strip().lower()
                    protocols[protocol_number] = protocol_name
                    
        return protocols
    except Exception as e:
        # Fallback to basic protocols if unable to fetch from IANA
        return {
            '6': 'tcp',
            '17': 'udp',
            '1': 'icmp'
        }
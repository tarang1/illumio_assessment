import csv
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
from protocol_loader import load_iana_protocols

class FlowLogProcessor:
    def __init__(self, lookup_file: str):
        self.tag_mappings = self._load_tag_mappings(lookup_file)
        self.protocol_map = self._get_protocol_map()
        #print(self.protocol_map)
        
    def _load_tag_mappings(self, lookup_file: str) -> Dict[Tuple[str, str], str]:
        """Load tag mappings from CSV file."""
        mappings = {}
        with open(lookup_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert to lowercase for case-insensitive matching
                port = row['dstport'].lower()
                protocol = row['protocol'].lower()
                tag = row['tag']
                mappings[(port, protocol)] = tag
        return mappings
    
    def process_flow_logs(self, input_file: str, output_file: str):
        """Process flow logs and generate statistics."""
        tag_counts = defaultdict(int)
        port_protocol_counts = defaultdict(int)
        
        with open(input_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 14 or parts[0] != '2':  # Verify it's version 2 flow log
                    continue
                    
                # Extract relevant fields
                dst_port = parts[6]
                protocol = self._get_protocol_name(parts[7])
                
                # Count port/protocol combinations
                port_protocol_counts[(dst_port, protocol)] += 1
                
                # Find matching tag
                tag = self._get_tag(dst_port, protocol)
                tag_counts[tag] += 1
        
        self._write_output(output_file, tag_counts, port_protocol_counts)
    
    def _get_protocol_map(self):
        """Fetch IANA protocol numbers."""
        return load_iana_protocols()

    def _get_protocol_name(self, protocol_number: str) -> str:
        """Convert protocol number to name using IANA protocol numbers."""
        if self.protocol_map is None:
            self.protocol_map = self._get_protocol_map()
        else:
            protocol_map = self.protocol_map
        return protocol_map.get(protocol_number, protocol_number).lower()
    
    def _get_tag(self, port: str, protocol: str) -> str:
        """Get tag for given port and protocol combination."""
        return self.tag_mappings.get((port.lower(), protocol.lower()), 'Untagged')
    
    def _write_output(self, output_file: str, 
                     tag_counts: Dict[str, int],
                     port_protocol_counts: Dict[Tuple[str, str], int]):
        """Write statistics to output file."""
        with open(output_file, 'w') as f:
            # Write tag counts
            f.write("Tag Counts:\n")
            f.write("Tag,Count\n")
            for tag, count in sorted(tag_counts.items()):
                f.write(f"{tag},{count}\n")
            
            f.write("\nPort/Protocol Combination Counts:\n")
            f.write("Port,Protocol,Count\n")
            for (port, protocol), count in sorted(port_protocol_counts.items()):
                f.write(f"{port},{protocol},{count}\n")
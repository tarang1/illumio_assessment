import os
import pytest
from ..flow_log_processor import FlowLogProcessor

@pytest.fixture
def sample_lookup_file(tmp_path):
    file_path = tmp_path / "lookup.csv"
    with open(file_path, "w") as f:
        f.write("dstport,protocol,tag\n")
        f.write("25,tcp,sv_P1\n")
        f.write("23,tcp,sv_P1\n")
        f.write("443,tcp,sv_P2\n")
        f.write("110,tcp,email\n")
        f.write("993,tcp,email\n")
        f.write("143,tcp,email\n")
    return file_path

@pytest.fixture
def sample_flow_logs(tmp_path):
    file_path = tmp_path / "flow_logs.txt"
    with open(file_path, "w") as f:
        f.write("2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 23 6 25 20000 1620140761 1620140821 ACCEPT OK\n")
        f.write("2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 23 443 6 15 12000 1620140761 1620140821 REJECT OK\n")
        f.write("2 123456789012 eni-9h8g7f6e 172.16.0.100 203.0.113.102 110 143 6 12 9000 1620140761 1620140821 ACCEPT OK\n")
    return file_path

def test_flow_log_processing(tmp_path, sample_lookup_file, sample_flow_logs):
    # Create output file path
    output_file = tmp_path / "output.txt"
    
    # Process flow logs
    processor = FlowLogProcessor(sample_lookup_file)
    processor.process_flow_logs(sample_flow_logs, output_file)
    
    # Verify output file exists
    assert output_file.exists()
    
    # Read and verify output content
    with open(output_file, "r") as f:
        content = f.read()
        print(content)
        # Check tag counts
        assert "Tag Counts:" in content
        assert "sv_P1,1" in content
        assert "sv_P2,1" in content
        assert "email,1" in content
        
        # Check port/protocol counts
        assert "Port/Protocol Combination Counts:" in content
        assert "443,tcp,1" in content
        assert "23,tcp,1" in content
        assert "143,tcp,1" in content
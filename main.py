import argparse
from flow_log_processor import FlowLogProcessor

def main():
    parser = argparse.ArgumentParser(description='Process VPC Flow Logs and map to tags.')
    parser.add_argument('--input', required=True, help='Input flow log file path')
    parser.add_argument('--lookup', required=True, help='Lookup table CSV file path')
    parser.add_argument('--output', required=True, help='Output file path')
    
    args = parser.parse_args()
    
    processor = FlowLogProcessor(args.lookup)
    processor.process_flow_logs(args.input, args.output)
    
if __name__ == "__main__":
    main()
import csv
from collections import defaultdict

# Function to load the lookup table into a dictionary
def load_lookup_table(lookup_file):
    lookup_dict = {}
    with open(lookup_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = (int(row['dstport']), row['protocol'].lower())
            lookup_dict[key] = row['tag']  
    return lookup_dict

# Function to parse the flow log file and count matches
def process_flow_logs(flow_log_file, lookup_dict):
    tag_count = defaultdict(int)
    port_protocol_count = defaultdict(int)
    with open(flow_log_file, mode='r') as file:
        for line in file:
            parts = line.strip().split()
            
            # Checking if the entry is Valid
            if len(parts) < 8:
                continue

            dstport = int(parts[6])
            if parts[7] == "6":
                protocol = "tcp"
            else:
                protocol = "udp"  
            key = (dstport, protocol)
            if key in lookup_dict:
                tag = lookup_dict[key]
            else:
                tag = "Untagged"
                
            tag_count[tag] += 1
            port_protocol_count[(dstport, protocol)] += 1

    return tag_count, port_protocol_count

# Function to write the results to output files
def generate_output_files(tag_count, port_protocol_count):
    with open('tag_count.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Tag", "Count"])
        for tag, count in tag_count.items():
            writer.writerow([tag, count])
    
    with open('port_protocol_count.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Port", "Protocol", "Count"])
        for (port, protocol), count in port_protocol_count.items():
            writer.writerow([port, protocol, count])

# Main function to run the program
def main():
    lookup_file = 'lookup_table.csv'
    flow_log_file = 'flow_logs.txt'   
    
    lookup_dict = load_lookup_table(lookup_file)
    tag_count, port_protocol_count = process_flow_logs(flow_log_file, lookup_dict)
    
    generate_output_files(tag_count, port_protocol_count)
    print("Output files generated - tag_count.csv, port_protocol_count.csv")

if __name__ == "__main__":
    main()

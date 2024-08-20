from flask import Flask, request, render_template, redirect, url_for, flash
import csv
from collections import defaultdict
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'supersecretkey'  # Required for flash messages

# Function to check allowed file extensions
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

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
def parse_flow_logs(flow_log_file, lookup_dict):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    
    with open(flow_log_file, mode='r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 8:
                continue
            
            try:
                dstport = int(parts[5])  
                protocol = "tcp" if parts[7] == "6" else "udp"  
            except (ValueError, IndexError) as e:
                continue
            
            key = (dstport, protocol)
            if key in lookup_dict:
                tag = lookup_dict[key]
            else:
                tag = "Untagged"
                
            tag_counts[tag] += 1
            port_protocol_counts[(dstport, protocol)] += 1

    return tag_counts, port_protocol_counts

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        lookup_file = request.files['lookup_file']
        flow_log_file = request.files['flow_log_file']

        # Check file extensions
        if not (lookup_file and allowed_file(lookup_file.filename, {'csv'})):
            flash('Invalid lookup file type. Please upload a CSV file.')
            return redirect(request.url)
        
        if not (flow_log_file and allowed_file(flow_log_file.filename, {'txt'})):
            flash('Invalid flow log file type. Please upload a TXT file.')
            return redirect(request.url)

        # Save files
        lookup_filepath = os.path.join(app.config['UPLOAD_FOLDER'], lookup_file.filename)
        flow_log_filepath = os.path.join(app.config['UPLOAD_FOLDER'], flow_log_file.filename)
        
        lookup_file.save(lookup_filepath)
        flow_log_file.save(flow_log_filepath)
        
        # Process files
        lookup_dict = load_lookup_table(lookup_filepath)
        tag_counts, port_protocol_counts = parse_flow_logs(flow_log_filepath, lookup_dict)
        
        return render_template('results.html', tag_counts=tag_counts, port_protocol_counts=port_protocol_counts)
        
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

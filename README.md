# Flow-Log-Processor
 
This project contains two components for processing network flow log data based on a lookup table:
- **Standalone Python Script**: A simple script that processes the flow log data, maps each log entry to a tag using a lookup table, and generates summary reports.
- **Flask Web Application**: A web interface that allows users to upload a lookup table and flow log file, processes the data, and displays the results in a tabulated form.

## Assumptions
- **Log Format and Log Version**: The program supports the default log format (version 2) as described in the problem statement. The fields in the log file are space-separated, with destination port and protocol fields in the expected positions (7th and 8th, respectively).
- **File Types For the Flask App**: The lookup table must be a CSV file, and the flow logs must be in a TXT file format. The program includes validation to ensure that only these file types are processed.

## Directory Structure
```
flow_log_processor/
│
├── app.py                
├── Flow_Log_Processor.py            
├── templates/
│   ├── index.html        
│   └── results.html      
└── uploads/              

```
- `app.py`: Flask application providing a web interface
- `Flow_Log_Processor.py/`: Standalone Python script for processing logs
- `templates /`: HTML template for the web interface
- `uploads /`: The directory for storing files uploaded using the web interface.

## Requirements
- **Python 3.6**
- **Flask**: Only required if running the web interface

## Setup Instructions

### Running the Standalone Script
- Clone the Repository:
  ```
  git clone <repository_url>
  cd flow_log_processor
  ```
- Run the Script:
   Ensure your lookup_table.csv and flow_logs.txt files are in the same directory as Flow_Log_Processor.py.
   Run the script using Python:
   ```
   python Flow_Log_Processor.py
   ```
- The script will output tag_count.csv and port_protocol_count.csv files in the same directory.

### Running the Flask Web Application

### Tests and Validation
  
  

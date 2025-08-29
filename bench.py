import argparse
import requests
import re

url_check = re.compile(r"^https://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

class HostData:
    successCount = 0
    failedCount = 0
    errorCount = 0
    minResponseTime = 0
    maxResponceTime = 0
    avgResponceTime = 0

def hostname_list(arg):
    return arg.split(',')

def save_output(output: str, filepath: str | None):
    if filepath:
        with open(filepath, 'w', encoding='UTF-8') as f:
            f.write(output)
    else:
        print(output)
        
def pingHostname(host, count):
    data = HostData()
    timeSum = 0
    for i in range(count): 
        try:
            responce = requests.get(host, timeout=3)
            data.successCount += responce.ok
            data.failedCount += not responce.ok
            deltaSeconds = responce.elapsed.total_seconds()
            timeSum+=deltaSeconds
            data.minResponseTime = min(data.minResponseTime, deltaSeconds) if data.minResponseTime != 0 else deltaSeconds
            data.maxResponceTime = max(data.maxResponceTime, deltaSeconds)
        except requests.ConnectTimeout:
            data.errorCount+=1
        except Exception as e:
            raise e
    if data.failedCount | data.successCount:
        data.avgResponceTime = timeSum / (data.failedCount+data.successCount)
    return data


parser = argparse.ArgumentParser(prog = 'Bench', description='Basic bench for domain ping test', epilog='Help me')
parser.add_argument('-C', '--count',
    type=int,
    help='Number of requests to send for each hosts',
    nargs='?',
    const=1,
    default=1
    )
parser.add_argument('-H', '--hosts',
    type=hostname_list,
    help='Hostnames separated by \',\', with no spaces between',
    default=[],
    )
parser.add_argument('-F', '--file', 
    help='address list')
parser.add_argument('-O', '--output', 
    help='Path to file to save output || By default output to console')
args = parser.parse_args()

if args.hosts and args.file:
    parser.error('You can specify either only one argument (-H or -F)')

if args.file:
    with open(args.file, 'r', encoding='UTF-8') as f:
        args.hosts = [line.strip() for line in f if line.strip()]

output_lines = []

for host in args.hosts:
    if not url_check.match(host):
        output_lines.append(f"Incorrect input: {host} || _EXPECTED_ https://example.com")
        output_lines.append("-" * 40)
        continue
    try:
        data = pingHostname(host, args.count)
        output_lines.append(f"Host:    {host}")
        output_lines.append(f"Success: {data.successCount}")
        output_lines.append(f"Failed:  {data.failedCount}")
        output_lines.append(f"Errors:  {data.errorCount}")
        output_lines.append(f"Min:     {data.minResponseTime}")
        output_lines.append(f"Max:     {data.maxResponceTime}")
        output_lines.append(f"Avg:     {data.avgResponceTime}")
        output_lines.append("-" * 40)
    except Exception as e:
        output_lines.append(f"Host: {host} || Error: {e}")
        output_lines.append("-" * 40)

output_text = "\n".join(output_lines)
save_output(output_text, args.output)

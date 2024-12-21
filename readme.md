# Simple Port Scanner

This is a simple asynchronous port scanner written in Python. It scans a range of ports on a target IP address and identifies which ports are open.

## Features

- Asynchronous scanning using `asyncio`
- Progress bar using `tqdm`
- Pretty output with colored text using `termcolor` and `pyfiglet`

## Requirements

- Python 3.7+
- `tqdm` library
- `termcolor` library
- `pyfiglet` library

You can install the required libraries using pip:

```bash
pip install tqdm termcolor pyfiglet
```

## Usage

To run the port scanner, execute the `main.py` script:

```bash
python main.py
```

You will be prompted to enter the target IP address and the port range to scan. If you do not provide any input, the default values will be used (127.0.0.1 for the IP address and 1-1000 for the port range).

## Example

```bash
Enter target IP (default: 127.0.0.1): 192.168.1.1
Enter port range (default: 1-1000): 1-1024
```

The script will then scan the specified range of ports on the target IP address and display the results with a progress bar and colored output.

## Output

The output will display the open ports in green text with a yellow background, the total number of closed ports, and the total time taken for the scan.

```plaintext
Scan Complete
Open ports on 192.168.1.1: 22, 80, 443
Total closed ports: 1021
Total time taken: 12.34 seconds
```

import asyncio
import time
from tqdm import tqdm
from termcolor import colored
from pyfiglet import Figlet
import sys

class SimplePortScanner:
    def __init__(self, target, ports):
        # Initialize the scanner with target IP and port range
        self.target = target
        self.ports = ports

    async def scan_port(self, port):
        # Scan a single TCP port
        try:
            reader, writer = await asyncio.open_connection(self.target, port)
            writer.close()
            await writer.wait_closed()
            return port, True
        except (OSError, asyncio.TimeoutError):
            return port, False

    async def run_scan(self):
        # Run the port scan with a semaphore to limit concurrency
        semaphore = asyncio.Semaphore(200)
        start_time = time.time()

        async def limited_scan(port):
            # Scan a port with semaphore limit
            async with semaphore:
                return await self.scan_port(port)

        tasks = [limited_scan(port) for port in self.ports]
        
        # Add progress bar and collect results
        results = []
        try:
            for f in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Scanning ports"):
                results.append(await f)
        except KeyboardInterrupt:
            # Handle user interruption
            print(colored("\nScan interrupted by user.", 'red'))
            return
        except Exception as e:
            # Handle other exceptions
            print(colored(f"\nAn error occurred: {e}", 'red'))
            return
        
        # Process results
        open_ports = [port for port, status in results if status]
        closed_ports = len(self.ports) - len(open_ports)

        end_time = time.time()
        total_time = end_time - start_time

        # Pretty output
        figlet = Figlet(font='slant')
        print(colored(figlet.renderText('Scan Complete'), 'cyan'))
        
        if open_ports:
            open_ports_str = ', '.join(map(str, open_ports))
            print(colored(f"Open ports on {self.target}: {open_ports_str}", 'black', 'on_green'))
        else:
            print(colored(f"No open ports on {self.target}.", 'red'))
        
        print(colored(f"Total closed ports: {closed_ports}", 'yellow'))
        print(colored(f"Total time taken: {total_time:.2f} seconds", 'blue'))

if __name__ == "__main__":
    # Get user input for target IP and port range
    target = input("Enter target IP (default: 127.0.0.1): ").strip() or "127.0.0.1"
    port_range = input("Enter port range (default: 1-1000): ").strip() or "1-1000"

    try:
        # Parse port range
        start_port, end_port = map(int, port_range.split('-'))
        ports = range(start_port, end_port + 1)

        # Create scanner instance and run scan
        scanner = SimplePortScanner(target, ports)
        asyncio.run(scanner.run_scan())
    except ValueError:
        # Handle invalid port range input
        print(colored("Invalid port range. Please use the format 'start-end', e.g., 1-1024.", 'red'))
    except KeyboardInterrupt:
        # Handle user interruption
        print(colored("\nScan interrupted by user.", 'red'))
        sys.exit(0)
    except Exception as e:
        # Handle other exceptions
        print(colored(f"Error: {e}", 'red'))
        sys.exit(1)

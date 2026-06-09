import socket
import time
import os

TARGET_DOMAIN = "hidalgocountydems.org"
LOG_FILE = "spoofed_domains.log"

def generate_variations(domain):
    """Generate common typosquatting variations for a domain."""
    variations = set()
    name, tld = domain.rsplit('.', 1)
    
    # 1. TLD variations
    for new_tld in ['com', 'net', 'info', 'co', 'us', 'io']:
        variations.add(f"{name}.{new_tld}")
        
    # 2. Character omission
    for i in range(len(name)):
        variations.add(f"{name[:i]}{name[i+1:]}.{tld}")
        
    # 3. Character repetition
    for i in range(len(name)):
        variations.add(f"{name[:i]}{name[i]}{name[i:]}.{tld}")
        
    # 4. Homoglyphs (simple substitutions)
    substitutions = {'o': '0', 'l': '1', 'i': '1', 'a': 'e'}
    for i, char in enumerate(name):
        if char in substitutions:
            variations.add(f"{name[:i]}{substitutions[char]}{name[i+1:]}.{tld}")

    # Remove the original domain just in case
    if domain in variations:
        variations.remove(domain)
        
    return list(variations)

def scan_domains(domains):
    """Check if variations resolve to an IP address (meaning they are registered)."""
    found = []
    for d in domains:
        try:
            ip = socket.gethostbyname(d)
            print(f"[!] Lookalike domain found: {d} -> {ip}")
            found.append((d, ip))
        except socket.gaierror:
            pass # Domain not found or not resolving
        time.sleep(0.05) # Brief pause to avoid flooding DNS resolvers
    return found

if __name__ == "__main__":
    print(f"Scanning for typosquats of {TARGET_DOMAIN}...")
    variations = generate_variations(TARGET_DOMAIN)
    print(f"Generated {len(variations)} variations to check.")
    
    found_domains = scan_domains(variations)
    
    # Get absolute path relative to the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(script_dir, LOG_FILE)
    
    with open(log_path, "w") as f:
        f.write(f"Typosquatting scan results for {TARGET_DOMAIN}\n")
        f.write("="*50 + "\n")
        if not found_domains:
            f.write("No active lookalike domains found during this scan.\n")
        else:
            for d, ip in found_domains:
                f.write(f"WARNING: {d} resolves to {ip}\n")
            
    print(f"\nScan complete. Found {len(found_domains)} registered lookalike domains.")
    print(f"Results logged to {log_path}")

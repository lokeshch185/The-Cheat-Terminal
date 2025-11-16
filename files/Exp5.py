import hashlib
import os

def compute_hashes(file_path):
    """Compute MD5, SHA-1, SHA-256, and SHA-512 hashes of a file."""
    hashes = {
        'MD5': hashlib.md5(),
        'SHA-1': hashlib.sha1(),
        'SHA-256': hashlib.sha256(),
        'SHA-512': hashlib.sha512()
    }
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            for h in hashes.values():
                h.update(chunk)
    return {name: h.hexdigest() for name, h in hashes.items()}

def write_hash_report(file_path, report_path):
    """Write all hashes to a report file."""
    hashes = compute_hashes(file_path)
    with open(report_path, 'w') as f:
        f.write(f"Hash Report for: {os.path.basename(file_path)}\n")
        for name, digest in hashes.items():
            f.write(f"{name}: {digest}\n")
    print(f"Hash report written to {report_path}")

def create_checksum_file(file_path):
    """Create a checksum file with SHA-256 hash and filename."""
    sha256_hash = compute_hashes(file_path)['SHA-256']
    checksum_filename = f"{os.path.basename(file_path)}.sha256"
    with open(checksum_filename, 'w') as f:
        f.write(f"{sha256_hash}  {os.path.basename(file_path)}\n")
    print(f"Checksum file created: {checksum_filename}")

def verify_checksum(checksum_file, directory='.'):
    """Verify file integrity using checksum file."""
    with open(checksum_file, 'r') as f:
        line = f.readline().strip()
        expected_hash, filename = line.split('  ')
    file_path = os.path.join(directory, filename)
    actual_hash = compute_hashes(file_path)['SHA-256']
    if actual_hash == expected_hash:
        print("Checksum OK (Authentic)")
    else:
        print("Checksum FAILED (Tampered)")

if __name__ == "__main__":
    sample_file = "example.txt"
    hash_report_file = "hash_report.txt"

    # Step 1: Generate hashes and write report
    write_hash_report(sample_file, hash_report_file)

    # Step 2: Create checksum file
    create_checksum_file(sample_file)

    # Step 3: Verify checksum (before tampering)
    print("\nVerifying checksum before tampering:")
    verify_checksum(f"{sample_file}.sha256")

    # Step 4: Tampering test 
    with open(sample_file, 'a') as f:
        f.write("X")  # Add a character to tamper
    print("\nVerifying checksum after tampering:")
    verify_checksum(f"{sample_file}.sha256")
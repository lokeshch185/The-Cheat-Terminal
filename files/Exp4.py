import secrets
import hashlib
import sys
import math

# Miller-Rabin primality test
def is_probable_prime(n, k=10):
    """Miller-Rabin probabilistic primality test."""
    if n < 2:
        return False
    small_primes = [2,3,5,7,11,13,17,19,23,29]
    for p in small_primes:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2  # random in [2, n-2]
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        composite = True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                composite = False
                break
        if composite:
            return False
    return True

# Safe prime generator
def generate_safe_prime(bits=512, k=10):
    if bits < 16:
        raise ValueError("bits too small")
    while True:
        q = secrets.randbits(bits - 1) | (1 << (bits - 2)) | 1  # ensure top bit and odd
        if not is_probable_prime(q, k=k):
            continue
        p = 2 * q + 1
        if is_probable_prime(p, k=k):
            return p, q

# Generator selection
def find_generator(p, q=None):
    if q is None:
        for g in range(2, 1000):
            if pow(g, p-1, p) == 1:
                return g
        raise RuntimeError("Couldn't find generator (non-safe-prime fallback).")
    else:
        for _ in range(1000):
            h = secrets.randbelow(p - 3) + 2
            g = pow(h, 2, p) 
            if pow(g, q, p) != 1 and pow(g, 2, p) != 1:
                if g > 1:
                    return g
        for g in range(2, p-1):
            if pow(g, q, p) != 1:
                return g
        raise RuntimeError("No generator found.")

# Key generation, KDF, demo
def generate_private_key(p):
    """Select private key in [2, p-2] using secrets."""
    return secrets.randbelow(p - 3) + 2

def public_from_private(g, a, p):
    return pow(g, a, p)

def compute_shared(A_or_B, own_priv, p):
    return pow(A_or_B, own_priv, p)

def kdf_sha256_int(K_int):
    """Derive a 32-byte key from integer K via SHA-256(K_bytes)."""
    if K_int == 0:
        K_bytes = b"\x00"
    else:
        K_bytes = K_int.to_bytes((K_int.bit_length() + 7) // 8, byteorder="big")
    return hashlib.sha256(K_bytes).digest()

def xor_stream_encrypt(key_bytes, plaintext_bytes):
    """
    Simple XOR-stream: derive keystream by hashing key + counter.
    Not secure for real use — only for lab demo.
    """
    out = bytearray()
    counter = 0
    idx = 0
    while idx < len(plaintext_bytes):
        ctr_bytes = counter.to_bytes(8, "big")
        block = hashlib.sha256(key_bytes + ctr_bytes).digest()
        take = min(len(block), len(plaintext_bytes) - idx)
        for i in range(take):
            out.append(plaintext_bytes[idx + i] ^ block[i])
        idx += take
        counter += 1
    return bytes(out)

# Pretty printing helpers
def short_hex(i):
    return hex(i)[2:66] + ("..." if i.bit_length() > 64*4 else "")

def show_param_summary(p, g):
    print("\nPublic parameters summary:")
    print(f"  p (bits) = {p.bit_length()} bits")
    print(f"  p (short hex) = {short_hex(p)}")
    print(f"  g = {g}\n")

# Menu / main
def main():
    p = None
    g = None
    q = None  
    alice = {"priv": None, "pub": None}
    bob   = {"priv": None, "pub": None}

    while True:
        print("\n--- Diffie-Hellman Lab ---")
        print("1) Select / Generate Public Parameters (p, g)")
        print("2) Generate Keys for Alice and Bob")
        print("3) Compute Shared Secret and Verify")
        print("4) Derive Symmetric Key & Demo Encrypt/Decrypt (Optional)")
        print("5) Show current parameters / keys summary")
        print("0) Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            print("\nParameter options:")
            print(" a) Generate a safe prime.")
            print(" b) Use a generated-but-not-safe prime.")
            print(" c) Enter custom p and g.")
            opt = input("Choose a/b/c: ").strip().lower()
            if opt == "a":
                bits = input("Enter desired bit-length for p (recommended 512 or 1024 for lab; 2048 may be slow): ").strip()
                try:
                    bits = int(bits)
                    print(f"Generating a safe prime p of {bits} bits. This may take a while for large sizes...")
                    p_new, q_new = generate_safe_prime(bits=bits)
                    q = q_new
                    p = p_new
                    g = find_generator(p, q)
                    print("Safe prime (p) and generator (g) generated.")
                    show_param_summary(p, g)
                except Exception as e:
                    print("Error generating safe prime:", e)
            elif opt == "b":
                bits = input("Enter bits for quick prime (e.g., 256 or 512): ").strip()
                try:
                    bits = int(bits)
                    while True:
                        cand = secrets.randbits(bits) | (1 << (bits-1)) | 1
                        if is_probable_prime(cand):
                            p = cand
                            q = None
                            g = 2
                            print("Quick prime generated (not necessarily safe prime).")
                            show_param_summary(p, g)
                            break
                except Exception as e:
                    print("Error:", e)
            elif opt == "c":
                p_str = input("Paste p (decimal): ").strip()
                g_str = input("Paste g (decimal): ").strip()
                try:
                    p = int(p_str)
                    g = int(g_str)
                    q = None
                    print("Custom parameters loaded.")
                    show_param_summary(p, g)
                except Exception as e:
                    print("Invalid input:", e)
            else:
                print("Invalid option.")
        elif choice == "2":
            if p is None or g is None:
                print("Please set parameters (p, g) first (option 1).")
                continue
            # Generate keys
            alice_priv = generate_private_key(p)
            alice_pub = public_from_private(g, alice_priv, p)
            bob_priv = generate_private_key(p)
            bob_pub = public_from_private(g, bob_priv, p)
            alice = {"priv": alice_priv, "pub": alice_pub}
            bob   = {"priv": bob_priv, "pub": bob_pub}
            print("\nKeys generated.")
            show_mask = input("Display private keys? (y/N): ").strip().lower()
            if show_mask == "y":
                print(f"Alice private a = {alice_priv}")
                print(f"Alice public A = {alice_pub}")
                print(f"Bob   private b = {bob_priv}")
                print(f"Bob   public B = {bob_pub}")
            else:
                print(f"Alice public A = {alice_pub}")
                print(f"Bob   public B = {bob_pub}")
                print("Private keys are hidden (use option to display them).")
        elif choice == "3":
            if any(x is None for x in (p, g, alice["pub"], bob["pub"], alice["priv"], bob["priv"])):
                print("Parameters and keys must be generated first (options 1 & 2).")
                continue
            K_A = compute_shared(bob["pub"], alice["priv"], p)
            K_B = compute_shared(alice["pub"], bob["priv"], p)
            print("\nComputed shared secrets:")
            print(f"  K_A (Alice's computed) short hex: {short_hex(K_A)}")
            print(f"  K_B (Bob's computed)   short hex: {short_hex(K_B)}")
            if K_A == K_B:
                print("SUCCESS: K_A == K_B (shared secret matches).")
            else:
                print("ERROR: shared secrets differ!")
        elif choice == "4":
            if any(x is None for x in (p, g, alice["pub"], bob["pub"], alice["priv"], bob["priv"])):
                print("Parameters and keys must be generated first (options 1 & 2).")
                continue
            K = compute_shared(bob["pub"], alice["priv"], p)
            K2 = compute_shared(alice["pub"], bob["priv"], p)
            if K != K2:
                print("Shared secret mismatch. Abort.")
                continue
            sym_key = kdf_sha256_int(K)
            print("\nDerived symmetric key (SHA-256 of shared secret):")
            print("  key (hex) =", sym_key.hex())
            msg = input("Enter a short plaintext message to encrypt (or press Enter to use default): ").strip()
            if not msg:
                msg = "Hello from Alice -> Bob"
            pt = msg.encode("utf-8")
            ct = xor_stream_encrypt(sym_key, pt)
            print("\nDemo: XOR-stream encryption (lab demo only)")
            print("  Plaintext:", msg)
            print("  Ciphertext (hex):", ct.hex())
            # Decrypt:
            recovered = xor_stream_encrypt(sym_key, ct)
            print("  Recovered plaintext:", recovered.decode("utf-8"))
        elif choice == "5":
            print("\nCurrent state summary:")
            if p is None:
                print("  Parameters: NOT SET")
            else:
                show_param_summary(p, g)
            def show_keypair(name, obj):
                if obj["priv"] is None:
                    print(f"  {name}: No keys")
                else:
                    print(f"  {name} public (short hex): {short_hex(obj['pub'])}")
                    print(f"    private hidden by default (bits: {obj['priv'].bit_length()})")
            show_keypair("Alice", alice)
            show_keypair("Bob", bob)
        elif choice == "0":
            print("Exiting. Goodbye.")
            sys.exit(0)
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()

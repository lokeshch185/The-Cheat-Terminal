import random
from math import gcd

def is_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    while True:
        p = random.getrandbits(bits)
        p |= (1 << bits - 1) | 1  
        if is_prime(p):
            return p

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    return x % m

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def generate_keys(bits):
    p = generate_prime(bits)
    q = generate_prime(bits)
    while q == p:
        q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    if gcd(e, phi) != 1:
        e = 3
        while gcd(e, phi) != 1:
            e += 2
    d = modinv(e, phi)
    return (e, d, n)

def encrypt(m, e, n):
    return pow(m, e, n)

def decrypt(c, d, n):
    return pow(c, d, n)

def main():
    e = d = n = None
    while True:
        print("\nRSA Cryptosystem Menu")
        print("1) Generate RSA Keys")
        print("2) Encrypt message")
        print("3) Decrypt message")
        print("4) Quit")
        choice = input("Enter your choice: ")
        if choice == '1':
            bits = int(input("Enter bit length for primes (e.g., 16, 32, 64): "))
            e, d, n = generate_keys(bits)
            print(f"Public Key (e, n): ({e}, {n})")
            print(f"Private Key (d, n): ({d}, {n})")
        elif choice == '2':
            if not (e and n):
                print("Generate keys first!")
                continue
            m = int(input(f"Enter plaintext as integer (0 <= m < {n}): "))
            if not (0 <= m < n):
                print("Plaintext out of range!")
                continue
            c = encrypt(m, e, n)
            print(f"Ciphertext: {c}")
        elif choice == '3':
            if not (d and n):
                print("Generate keys first!")
                continue
            c = int(input(f"Enter ciphertext as integer (0 <= c < {n}): "))
            if not (0 <= c < n):
                print("Ciphertext out of range!")
                continue
            m = decrypt(c, d, n)
            print(f"Recovered Plaintext: {m}")
        elif choice == '4':
            print("Exiting.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
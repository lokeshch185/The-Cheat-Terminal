def rail_fence_encrypt(text, rails):
    fence = [['' for _ in range(len(text))] for _ in range(rails)]
    rail, var = 0, 1
    for i, char in enumerate(text):
        fence[rail][i] = char
        rail += var
        if rail == 0 or rail == rails - 1:
            var = -var
    return ''.join(''.join(row) for row in fence)

def rail_fence_decrypt(cipher, rails):
    fence = [['' for _ in range(len(cipher))] for _ in range(rails)]
    idx = 0
    for r in range(rails):
        rail, var = 0, 1
        for i in range(len(cipher)):
            if rail == r:
                fence[rail][i] = '*'
            rail += var
            if rail == 0 or rail == rails - 1:
                var = -var
    for r in range(rails):
        for i in range(len(cipher)):
            if fence[r][i] == '*' and idx < len(cipher):
                fence[r][i] = cipher[idx]
                idx += 1
    result = []
    rail, var = 0, 1
    for i in range(len(cipher)):
        result.append(fence[rail][i])
        rail += var
        if rail == 0 or rail == rails - 1:
            var = -var
    return ''.join(result)

def columnar_encrypt(text, key):
    key_order = sorted(list(enumerate(key)), key=lambda x: x[1])
    n_cols = len(key)
    n_rows = -(-len(text) // n_cols)
    matrix = [['' for _ in range(n_cols)] for _ in range(n_rows)]
    idx = 0
    for r in range(n_rows):
        for c in range(n_cols):
            if idx < len(text):
                matrix[r][c] = text[idx]
                idx += 1
            else:
                matrix[r][c] = 'X'
    cipher = ''
    for col_idx, _ in key_order:
        for row in matrix:
            cipher += row[col_idx]
    return cipher

def columnar_decrypt(cipher, key):
    key_order = sorted(list(enumerate(key)), key=lambda x: x[1])
    n_cols = len(key)
    n_rows = -(-len(cipher) // n_cols)
    matrix = [['' for _ in range(n_cols)] for _ in range(n_rows)]
    idx = 0
    for col_idx, _ in key_order:
        for r in range(n_rows):
            if idx < len(cipher):
                matrix[r][col_idx] = cipher[idx]
                idx += 1
    plain = ''
    for r in range(n_rows):
        for c in range(n_cols):
            plain += matrix[r][c]
    return plain.rstrip('X')

def double_trans_encrypt(text, key1, key2):
    return columnar_encrypt(columnar_encrypt(text, key1), key2)

def double_trans_decrypt(cipher, key1, key2):
    return columnar_decrypt(columnar_decrypt(cipher, key2), key1)

def main():
    while True:
        print("\nChoose Transposition Cipher:")
        print("1 - Rail Fence Cipher")
        print("2 - Columnar Transposition Cipher")
        print("3 - Double Transposition Cipher")
        print("4 - Quit\n")
        choice = input("Enter your choice (1/2/3/4): ")
        if choice == '4':
            print("Exiting program.")
            break
        if choice not in ['1', '2', '3']:
            print("Invalid choice.")
            continue
        action = input("Type 'e' for encryption or 'd' for decryption: ").lower()
        if action not in ['e', 'd']:
            print("Invalid action.")
            continue
        text = input("Enter the text: ").replace(" ", "").upper()
        if choice == '1':
            rails = int(input("Enter number of rails: "))
            if action == 'e':
                encrypted = rail_fence_encrypt(text, rails)
                print("Encrypted (Rail Fence):", encrypted)
            else:
                decrypted = rail_fence_decrypt(text, rails)
                print("Decrypted (Rail Fence):", decrypted)
        elif choice == '2':
            key = input("Enter columnar key (e.g., '4312567'): ")
            if action == 'e':
                encrypted = columnar_encrypt(text, key)
                print("Encrypted (Columnar):", encrypted)
            else:
                decrypted = columnar_decrypt(text, key)
                print("Decrypted (Columnar):", decrypted)
        elif choice == '3':
            key1 = input("Enter first key for double transposition: ")
            key2 = input("Enter second key for double transposition: ")
            if action == 'e':
                encrypted = double_trans_encrypt(text, key1, key2)
                print("Encrypted (Double Transposition):", encrypted)
            else:
                decrypted = double_trans_decrypt(text, key1, key2)
                print("Decrypted (Double Transposition):", decrypted)

if __name__ == "__main__":
    main()
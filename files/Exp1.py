import numpy as np

# -------------------- Caesar Cipher --------------------
def caesar_cipher(text, shift=3):
    result = ""
    for char in text:
        if char.isalpha():
            base = 'A' if char.isupper() else 'a'
            result += chr((ord(char) - ord(base) + shift) % 26 + ord(base))
        else:
            result += char
    return result

def caesar_decipher(text, shift=3):
    return caesar_cipher(text, -shift)

# -------------------- Playfair Cipher --------------------
def generate_playfair_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    for char in key:
        if char not in matrix and char.isalpha():
            matrix.append(char)
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in matrix:
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def playfair_prepare(text):
    text = text.upper().replace("J", "I")
    prepared = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        if a == b:
            prepared += a + 'X'
            i += 1
        else:
            prepared += a + b
            i += 2
    if len(prepared) % 2 != 0:
        prepared += 'X'
    return prepared

def playfair_cipher(text, key="KEYWORD"):
    matrix = generate_playfair_matrix(key)
    prepared = playfair_prepare(text)
    encrypted = ""
    for i in range(0, len(prepared), 2):
        a, b = prepared[i], prepared[i+1]
        ax, ay = [(row, col) for row in range(5) for col in range(5) if matrix[row][col] == a][0]
        bx, by = [(row, col) for row in range(5) for col in range(5) if matrix[row][col] == b][0]
        if ax == bx:
            encrypted += matrix[ax][(ay+1) % 5] + matrix[bx][(by+1) % 5]
        elif ay == by:
            encrypted += matrix[(ax+1) % 5][ay] + matrix[(bx+1) % 5][by]
        else:
            encrypted += matrix[ax][by] + matrix[bx][ay]
    return encrypted

def playfair_decipher(text, key="KEYWORD"):
    matrix = generate_playfair_matrix(key)
    decrypted = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        ax, ay = [(row, col) for row in range(5) for col in range(5) if matrix[row][col] == a][0]
        bx, by = [(row, col) for row in range(5) for col in range(5) if matrix[row][col] == b][0]
        if ax == bx:
            decrypted += matrix[ax][(ay-1) % 5] + matrix[bx][(by-1) % 5]
        elif ay == by:
            decrypted += matrix[(ax-1) % 5][ay] + matrix[(bx-1) % 5][by]
        else:
            decrypted += matrix[ax][by] + matrix[bx][ay]
    return decrypted

# -------------------- Hill Cipher --------------------
def hill_cipher(text, key_matrix):
    text = text.upper().replace(" ", "")
    while len(text) % 2 != 0:
        text += "X"
    encrypted = ""
    for i in range(0, len(text), 2):
        pair = [ord(text[i]) - 65, ord(text[i+1]) - 65]
        result = np.dot(key_matrix, pair) % 26
        encrypted += chr(result[0] + 65) + chr(result[1] + 65)
    return encrypted

def mod_inv(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("No modular inverse")

def hill_decipher(text, key_matrix):
    text = text.upper().replace(" ", "")
    while len(text) % 2 != 0:
        text += "X"
    det = int(np.round(np.linalg.det(key_matrix))) % 26
    det_inv = mod_inv(det, 26)
    matrix_inv = (
        det_inv * np.round(det * np.linalg.inv(key_matrix)).astype(int) % 26
    )
    decrypted = ""
    for i in range(0, len(text), 2):
        pair = [ord(text[i]) - 65, ord(text[i+1]) - 65]
        result = np.dot(matrix_inv, pair) % 26
        decrypted += chr(int(result[0]) + 65) + chr(int(result[1]) + 65)
    return decrypted

# -------------------- Main Menu --------------------
def main():
    while True:
        print("\nChoose Encryption Method:")
        print("1 - Caesar Cipher")
        print("2 - Playfair Cipher")
        print("3 - Hill Cipher")
        print("4 - Quit\n")
        choice = input("Enter your choice (1/2/3/4): ")
        if choice == '4':
            print("Exiting program.")
            break
        if choice not in ['1', '2', '3']:
            print("Wrong input! Please choose 1, 2, 3, or 4.")
            continue
        action = input("Type 'e' for encryption or 'd' for decryption: ").lower()
        if action not in ['e', 'd']:
            print("Invalid action! Please enter 'e' or 'd'.")
            continue
        text = input("Enter the text: ")
        if choice == '1':
            shift = int(input("Enter shift value (default 3): ") or 3)
            if action == 'e':
                encrypted = caesar_cipher(text, shift)
                print("Encrypted (Caesar):", encrypted)
            else:
                decrypted = caesar_decipher(text, shift)
                print("Decrypted (Caesar):", decrypted)
        elif choice == '2':
            key = input("Enter Playfair key (default 'KEYWORD'): ") or "KEYWORD"
            if action == 'e':
                encrypted = playfair_cipher(text, key)
                print("Encrypted (Playfair):", encrypted)
            else:
                decrypted = playfair_decipher(text, key)
                print("Decrypted (Playfair):", decrypted)
        elif choice == '3':
            print("Using default 2x2 key matrix [[3, 3], [2, 5]]")
            key_matrix = np.array([[3, 3], [2, 5]])
            if action == 'e':
                encrypted = hill_cipher(text, key_matrix)
                print("Encrypted (Hill):", encrypted)
            else:
                try:
                    decrypted = hill_decipher(text, key_matrix)
                    print("Decrypted (Hill):", decrypted)
                except Exception as e:
                    print("Error in decryption:", e)

if __name__ == "__main__":
    main()
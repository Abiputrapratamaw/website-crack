import re
import sys

def deobfuscate_bash_script(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        obfuscated_content = f.read()

    # Mendeteksi urutan escape dan mengonversinya
    def decode_escape_sequences(match):
        return bytes.fromhex(match.group(0).replace("\\x", "")).decode('utf-8', errors='ignore')

    # Mengganti urutan escape hex
    deobfuscated_content = re.sub(r'(\\x[0-9A-Fa-f]{2})+', decode_escape_sequences, obfuscated_content)

    # Menyimpan hasil deobfuscate ke output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(deobfuscated_content)

    print(f"Deobfuscation selesai, hasil disimpan di {output_file}")

# Mengecek apakah argumen input dan output telah diberikan
if len(sys.argv) != 3:
    print("Usage: python3 deobfuscate_bash.py <input_file> <output_file>")
    sys.exit(1)

# Mendapatkan nama file input dan output dari argumen
input_file = sys.argv[1]
output_file = sys.argv[2]

# Menjalankan deobfuscation
deobfuscate_bash_script(input_file, output_file)

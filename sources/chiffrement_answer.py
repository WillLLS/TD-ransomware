# Il s'agit d'une opération xor
# Il faut donc 2 élements pour obtenir le 3ème

from xorcrypt import xorcrypt

plaintext = b"HellowWorld"
key = b"123"

# Test with repetitive word :

plaintext_rep = "_".join([str(plaintext, encoding="utf-8") for _ in range(3)])
print(plaintext_rep)
print(f"""
PLAINTEXT :\t {plaintext}
KEY :\t\t {key}
""")


ciphertext = xorcrypt(plaintext, key)
print("PLAINTEXT xor KEY ")
print("CIPHER TEXT:\t", ciphertext)

res = xorcrypt(ciphertext, key)
print("\nCIPHER TEXT xor KEY")
print("RES: \t\t", res)

res = xorcrypt(plaintext, ciphertext)
print("\nCIPHER TEXT xor CIPHER TEXT")
print("RES: \t\t", res)


ciphertext = xorcrypt(bytes(plaintext_rep, encoding="utf-8"), key)
print("\nPLAINTEXT xor KEY ")
print("CIPHER TEXT:\t", ciphertext)

print("""
    Si des mots se répètent dans le fichier, nous pouvons voir des réptitions
    dûe à la répétition de la clef elle meme
    """)
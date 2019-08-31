import struct
import os

test_file = "/home/genicleito/Downloads/teste_caracteres.txt"
out_file = test_file.replace(".txt", "_limpo.txt")

special_char_to_remove = []
for e in [x for x in range(1, 32) if x != 10]:
    special_char_to_remove.append(struct.pack("B", e))

os.system("sed -r 's/" + "|".join(special_char_to_remove) + "//g' " + test_file + " > " + out_file)
# print(special_char_to_remove)
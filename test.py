import base64

read_file = open('tl1.jpg', 'rb')
data = read_file.read()

b64 = base64.b64encode(data)

print (b64)

# Save file
decode_b64 = base64.b64decode(b64)
out_file = open('out_newgalax.png', 'wb')
out_file.write(decode_b64)
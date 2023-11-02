import base64 
file_path = "test.txt"
with open(file_path, 'rb') as f:
    file_data = f.read()
    encoded_data = base64.b64encode(file_data).decode('utf-8')
print(encoded_data)

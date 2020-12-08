import socket
import threading
import base64
import datetime
s = socket.socket()
HOST = socket.gethostname()
print('Server will start on host:', HOST)
PORT = 1234
s.bind((HOST, PORT))

s.listen(1)

conn, addr = s.accept()
print(addr, 'has connected')


def save_file(type, data):
    filename = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + type
    file = open(filename, 'wb')
    if type != '.txt':
        data = base64.b64decode(data[8:])
        file.write(data)
    else:
        file.write(data[8:])
    file.close()
    print('Done')


def reciver_message():
    while 1:
        try:
            file_data = conn.recv(1024 * 25)
            check = file_data[:8].decode('utf-8')
            if check == 'file_txt':
                save_file('.txt', file_data)
            elif check == 'file_png':
                save_file('.png', file_data)
            elif check == 'file_jpg':
                save_file('.jpg', file_data)
            else:
                # reciver message
                try:
                    incoming_mgs = file_data.decode('utf-8')
                    print('CLient:>>', incoming_mgs)
                except Exception as ex:
                    print('Server disconected !!!')
                    print(ex)
                    conn.close()
                    break
        except Exception as ex:
            print('Something wrong!!!')
            print(ex)
            conn.close()
            break

def file_type(filename, codecheck):
    file = open(filename, 'rb')
    if codecheck != 'file_txt':
        file_data = codecheck.encode('utf-8') + base64.b64encode(file.read(1024 * 25))
    else:
        file_send = codecheck.encode('utf-8') + file.read(1024 * 25)
        file_data = file_send
    conn.send(file_data)

def send_file():
    while 1:
        try:
            mgs = input(str())
            if mgs[-4:] == '.txt':
                file_type(mgs, 'file_txt')
            elif mgs[-4:] == '.png':
                file_type(mgs, 'file_png')
            elif mgs[-4:] == '.jpg':
                file_type(mgs, 'file_jpg')
            else:
                # send message
                try:
                    conn.send(mgs.encode('utf-8'))
                except Exception as ex:
                    print('An error occured!')
                    conn.close()
                    print(ex)
                    break
        except Exception as ex:
            conn.close()
            print(ex)
            break

receive_thread = threading.Thread(target=reciver_message)
receive_thread.start()

write_file_thread = threading.Thread(target=send_file)
write_file_thread.start()


import socket
import threading
import datetime
import base64

s = socket.socket()
HOST = input(str('Please enter host name: '))
PORT = 1234

try:
    s.connect((HOST, PORT))
    print('Connect to ', HOST, 'is successfully')
except:
    print('Connect fail')

def file_type(filename, codecheck):
    file = open(filename, 'rb')
    if codecheck != 'file_txt':
        file_data = codecheck.encode('utf-8') + base64.b64encode(file.read(1024 * 25))
    else:
        file_send = codecheck.encode('utf-8') + file.read(1024 * 25)
        file_data = file_send
    s.send(file_data)


def send_message():
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
                    s.send(mgs.encode('utf-8'))
                except Exception as ex:
                    print('An error occured!')
                    s.close()
                    print(ex)
                    break
        except Exception as ex:
            s.close()
            print(ex)
            break


def save_file(type, data):
    filename = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + type
    file = open(filename, 'wb')
    if type == '.jpg' or type == '.png':
        data = base64.b64decode(data[8:])
        file.write(data)
    else:
        file.write(data[8:])
    file.close()
    print('Done')


def reciver_file():
    while 1:
        try:
            file_data = s.recv(1024 * 25)
            check = file_data[:100].decode('utf-8')
            if check[:8] == 'file_txt':
                save_file('.txt', file_data)
            elif check[:8] == 'file_png':
                save_file('.png', file_data)
            elif check[:8] == 'file_jpg':
                save_file('.jpg', file_data)
            else:
                # reciver message
                try:
                    incoming_mgs = file_data.decode('utf-8')
                    check = file_data.decode('utf-8')[:100]
                    print(check[:100])
                    if check[:8] != 'file_txt' or check[:8] != 'file_png' or check[:8] != 'file_jpg':
                        print('Server:>>', incoming_mgs)
                except Exception as ex:
                    print('Server disconected !!!')
                    print(ex)
                    s.close()
                    break
        except Exception as ex:
            print('Something wrong!!!')
            print(ex)
            s.close()
            break


write_thread = threading.Thread(target=send_message)
write_thread.start()

reciver_file_thread = threading.Thread(target=reciver_file)
reciver_file_thread.start()


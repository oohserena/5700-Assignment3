import ssl
import os
from socket import *
import base64

username = os.getenv('EMAIL_USER', '')
password = os.getenv('EMAIL_PASS', '')
recipient_email = ""

msg = "\r\nI love computer networks!"
endmsg = "\r\n.\r\n"

mailserver = "smtp.gmail.com"
mailport = 587

try:
   
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailserver, mailport))
    recv = clientSocket.recv(1024).decode()
    print(f"Server: {recv}")
    if recv[:3] != '220':
        raise Exception('220 reply not received from server.')


    ehloCommand = 'EHLO Alice\r\n'
    clientSocket.send(ehloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(f"Server: {recv1}")
    if recv1[:3] != '250':
        raise Exception('250 reply not received from server.')


    starttlsCommand = 'STARTTLS\r\n'
    clientSocket.send(starttlsCommand.encode())
    recv_tls = clientSocket.recv(1024).decode()
    print(f"Server: {recv_tls}")
    if recv_tls[:3] != '220':
        raise Exception('220 reply not received from server.')


    context = ssl.create_default_context(cafile="")

    clientSocket = context.wrap_socket(clientSocket, server_hostname=mailserver)

    clientSocket.send(ehloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(f"Server: {recv1}")
    if recv1[:3] != '250':
        raise Exception('250 reply not received from server.')


    clientSocket.send(b'AUTH LOGIN\r\n')
    recv_auth = clientSocket.recv(1024).decode()
    print(f"Server: {recv_auth}")
    

    clientSocket.send(base64.b64encode(username.encode()) + b'\r\n')
    recv_username = clientSocket.recv(1024).decode()
    print(f"Server: {recv_username}")


    clientSocket.send(base64.b64encode(password.encode()) + b'\r\n')
    recv_password = clientSocket.recv(1024).decode()
    print(f"Server: {recv_password}")

    # Send MAIL FROM command
    mailfromCommand = f'MAIL FROM: <{username}>\r\n'
    clientSocket.send(mailfromCommand.encode())
    recv2 = clientSocket.recv(1024).decode()
    print(f"Server: {recv2}")
    if recv2[:3] != '250':
        raise Exception('250 reply not received from server.')

    # Send RCPT TO command
    rcpttoCommand = f'RCPT TO: <{recipient_email}>\r\n'
    clientSocket.send(rcpttoCommand.encode())
    recv3 = clientSocket.recv(1024).decode()
    print(f"Server: {recv3}")
    if recv3[:3] != '250':
        raise Exception('250 reply not received from server.')

    # Send DATA command
    dataCommand = 'DATA\r\n'
    clientSocket.send(dataCommand.encode())
    recv4 = clientSocket.recv(1024).decode()
    print(f"Server: {recv4}")
    if recv4[:3] != '354':
        raise Exception('354 reply not received from server.')

    # Send message data and ending
    clientSocket.send((msg + endmsg).encode())
    recv5 = clientSocket.recv(1024).decode()
    print(f"Server: {recv5}")
    if recv5[:3] != '250':
        raise Exception('250 reply not received from server.')

    # Send QUIT command
    quitCommand = 'QUIT\r\n'
    clientSocket.send(quitCommand.encode())
    recv6 = clientSocket.recv(1024).decode()
    print(f"Server: {recv6}")
    if recv6[:3] != '221':
        raise Exception('221 reply not received from server.')

    print("Email sent successfully!")

except Exception as e:
    print(f"Error: {e}")
finally:
    clientSocket.close()

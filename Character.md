Character
===
HTB{tH15_1s_4_r3aLly_l0nG_fL4g_i_h0p3_f0r_y0Ur_s4k3_tH4t_y0U_sCr1pTEd_tH1s_oR_els3_iT_t0oK_qU1t3_l0ng!!}

```python=
import socket

def send_receive_data():
    # IP address and port of the server
    server_ip = ""94.237.49.166""
    server_port = 33099
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_file = client_socket.makefile(""rb"")
    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))
        print(""Connected to the server"")
        for i in range(103):
            data = socket_file.read(65)
            client_socket.sendall(str(i).encode()+b""\n"")
            data = socket_file.readline()
            data = data.decode()
            data = data.replace(""Character at index ""+str(i)+"": "", """")
            data = data.replace(""\n"", """")
            print(f""{data}"")
    except ConnectionRefusedError:
            print(""Connection to the server refused."")
            
if __name__ == ""__main__"":
    send_receive_data()
```
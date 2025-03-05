StopDropRoll
===


> HTB{1_wiLl_sT0p_dR0p_4nD_r0Ll_mY_w4Y_oUt!}

```python
import socket

def send_receive_data():
    # IP address and port of the server
    server_ip = ""94.237.61.21""
    server_port = 41751
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_file = client_socket.makefile(""rb"")
    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))
        print(""Connected to the server"")
        for _ in range(12):
            data = socket_file.readline()
            print(data.decode().strip())
        data = socket_file.read(21)
        print(data.decode().strip())
        # Respond with ""y""
        client_socket.sendall(b""y\n"")
        print(""Sent: y"")
        data = socket_file.readline()
        print(f""Received line: {data}"")

        # Infinite loop until ""HTB{"" is received in the response
        while True:
            # Receive the second line
            data = socket_file.readline().decode().strip()
            data = data.replace(""What do you do? "", """")
            print(f""Received line: {data}"")
            # Split the response into parts using "", "" as delimiter
            if len(data) != 5 or 6 or 4:
                parts = data.split("", "")
                print(f""Split response into parts: {parts}"")

            # Prepare the response based on the components
            response = """"
            for i, part in enumerate(parts):
                if i > 0:  # Add a hyphen before appending subsequent parts
                    response += ""-""
                if ""GORGE"" in part:
                    response += ""STOP""
                if ""PHREAK"" in part:
                    response += ""DROP""
                if ""FIRE"" in part:
                    response += ""ROLL""

            # Send back the response
            client_socket.sendall(response.encode()+b""\n"")
            print(f""Sent response: {response}"")

            # Check if ""HTB{"" is present in the response
            if ""HTB{"" in response:
                print(""Received flag!"")
                break  # Exit the loop if ""HTB{"" is received

    except ConnectionRefusedError:
        print(""Connection to the server refused."")
    finally:
        # Close the socket
        client_socket.close()
        print(""Connection closed."")

if __name__ == ""__main__"":
    send_receive_data()
```

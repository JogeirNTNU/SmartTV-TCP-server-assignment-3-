import socket

def create_client_socket():
  return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server(sock, host, port):
  sock.connect((host, port))
  print(f"Connected to server on port {port}")

def receive_data(sock):
  return sock.recv(1024)

def read_send_command(sock):
  while True:
    command = input("IDATA2304>> ")
    sock.sendall(command.encode())
    response = sock.recv(1024).decode().strip()
    print(response)
    if command.lower() == "quit":
      break

def main():
  host = "127.0.0.1"
  
  # Available TV ports
  tv_ports = {
    1: 65432,  # TV-1
    2: 65433,  # TV-2
    3: 65434   # TV-3
  }
  
  print("Available TV servers:")
  print("1. TV-1 (port 65432)")
  print("2. TV-2 (port 65433)")  
  print("3. TV-3 (port 65434)")
  
  try:
    choice = int(input("Select TV to connect to (1-3): "))
    if choice not in tv_ports:
      print("Invalid choice")
      return
      
    port = tv_ports[choice]
    print(f"Connecting to TV-{choice} on port {port}...")
    
  except ValueError:
    print("Invalid input. Please enter a number.")
    return
  
  sock = create_client_socket()
  try:
    connect_to_server(sock, host, port)
    response = receive_data(sock)
    print(response.decode(errors = "ignore"))
    read_send_command(sock)
  except ConnectionRefusedError:
    print(f"Could not connect to TV-{choice}. Make sure the server is running on port {port}.")
  except Exception as e:
    print(f"An error occurred: {e}")
  finally:
    sock.close()
  
if __name__ == "__main__":
  main()
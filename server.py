import socket
from SmartTVClass import SmartTV


def create_socket():
  return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def bind_socket(sock, host, port):
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow port reuse
  sock.bind((host, port))

def listen_for_connection(sock, tv_id):
  sock.listen(1)  # Allow only 1 connection at a time
  print(f"Server listening on {sock.getsockname()} for {tv_id}")

def accept_connection(sock):
  return sock.accept()

def receive_command(conn):
  try:
    data = conn.recv(1024)
    if not data:
      return None
    return data.decode().strip()
  except:
    return None
  
def close_socket(sock):
  sock.close()
  print("Server closed")

def main():
  host = "127.0.0.1"
  
  # Available TV ports and their corresponding TV instances
  tv_ports = {
    1238: "TV-1",
    1239: "TV-2", 
    1240: "TV-3"
  }
  
  print("Available TV servers:")
  for port, tv_name in tv_ports.items():
    print(f"Port {port}: {tv_name}")
  print("Or press Enter for default port 1238")
  
  try:
    port_input = input("Select port to start server on: ").strip()
    if port_input == "":
      selected_port = 1238
      tv_name = "Default-TV"
    else:
      selected_port = int(port_input)
      if selected_port not in tv_ports:
        print("Invalid port selected")
        return
      tv_name = tv_ports[selected_port]
  except ValueError:
    print("Invalid input")
    return
  server_socket = create_socket()
  
  # Create a SmartTV instance for this specific TV
  smart_tv = SmartTV()
  
  try:
    bind_socket(server_socket, host, selected_port)
    listen_for_connection(server_socket, tv_name)
    
    while True:
      print(f"Waiting for client connection to {tv_name}...")
      conn, addr = accept_connection(server_socket)
      print(f"Client {addr} connected to {tv_name}")
      conn.sendall(f"Welcome to {tv_name}. Type 'help' for commands or 'quit' to exit.\n".encode())
      
      # Handle client commands
      while True:
        command = receive_command(conn)
        if not command or command.lower() == "quit":
          conn.sendall(b"Goodbye!\n")
          break
        
        # Use the SmartTV instance to handle the command
        response = smart_tv.handle_command(command)
        conn.sendall((response + "\n").encode())
      
      conn.close()
      print(f"Client {addr} disconnected from {tv_name}")
      print(f"{tv_name} is ready for new connections")
      
  except KeyboardInterrupt:
    print("\nServer shutdown requested")
  except Exception as e:
    print(f"Server error: {e}")
  finally:
    close_socket(server_socket)

if __name__ == "__main__":
  main()


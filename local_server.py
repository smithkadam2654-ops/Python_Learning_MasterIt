import http.server
import socketserver
import os
import socket

def get_local_ip():
    try:
        # Create a dummy socket to find local IP on the network
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def start_server(port=8000):
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            local_ip = get_local_ip()
            print("="*50)
            print("🌐 Local Network File Server Started!")
            print("="*50)
            print(f"Serving folder : {os.getcwd()}")
            print(f"Local link     : http://localhost:{port}")
            print(f"Network link   : http://{local_ip}:{port}")
            print("You can access the Network link from your phone or another PC on the same Wi-Fi.")
            print("Press Ctrl+C to stop the server.")
            print("="*50)
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped. Have a nice day!")
    except OSError as e:
        print(f"\n[ERROR] Could not start server on port {port}. It might be in use.")
        print(e)

if __name__ == "__main__":
    start_server(port=8000)

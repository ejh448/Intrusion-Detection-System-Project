import customtkinter as ctk
import socket



def get_local_ip():
    """Get the local IP Address of the machine."""
    #socket.AF_INET: specifies IPv4 address family.
    #socket.SOCK_DGRAM: specifies the socket will be used for (UDP) the user datagram protocol
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0)
    try:
        # the IP address 10.254.254.254 is an ip address that is unlikely to exist.
        sock.connect(('10.254.254.254', 1))
        local_ip_address = sock.getsockname()[0]
        local_socket = sock.getsockname()[1]
        ip_socket = [local_ip_address, local_socket]
    except Exception:
        ip_socket = ["error receiving local ip address...", "error receiving local socket..."]
    finally:
        sock.close()
    return ip_socket

# Options: "System" (default), "Dark", "Light"
ctk.set_appearance_mode("dark") 
# Options: "blue", "green", "dark-blue"
ctk.set_default_color_theme("blue")  
# Create app window
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Intrusion Detection System")
        self.geometry("400x300")

        # Label
        self.label = ctk.CTkLabel(self, text="Hello, CustomTkinter!", font=("Arial", 20))
        self.label.pack(pady=20)

        # Entry
        self.entry = ctk.CTkEntry(self, placeholder_text="Type something...")
        self.entry.pack(pady=10)

        # Button
        self.button = ctk.CTkButton(self, text="local ip address", command=self.local_ip)
        self.button.pack(pady=10)

        self.button1 = ctk.CTkButton(self, text="local socket", command=self.local_socket)
        self.button1.pack(pady=10)


        # Switch
        self.switch = ctk.CTkSwitch(self, text="Toggle me")
        self.switch.pack(pady=10)

    def local_ip(self):
        ip_address = get_local_ip()
        self.label.configure(text=f"local IP Address: {ip_address[0]}")
    
    def local_socket(self):
        socket = get_local_ip()[1]
        self.label.configure(text=f"current local Socket: {socket}")




if __name__ == "__main__":
    app = App()
    app.mainloop()

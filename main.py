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
        self.geometry("600x400")

        # Setting up grid layout
        self.grid_columnconfigure(0, weight=1) # Left
        self.grid_columnconfigure(1, weight=3) # Middle
        self.grid_columnconfigure(2, weight=1) # Right
        self.grid_rowconfigure(5, weight=1) # Footer

        """Left Column"""
        # Labels
        self.left_tools_label = ctk.CTkLabel(self, text="Tools", font=("Arial", 15))
        self.left_tools_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.left_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.left_label.grid(row=1, column=0, padx=5, pady=5)

        # Buttons
        self.get_ip_button = ctk.CTkButton(self, text="local ip address", command=self.local_ip)
        self.get_ip_button.grid(row=2, column=0, padx=5, pady=5)

        self.get_current_local_socket = ctk.CTkButton(self, text="local socket", command=self.local_socket)
        self.get_current_local_socket.grid(row=3, column=0, padx=5, pady=5)

        """Middle Column"""
        self.middle_main_label = ctk.CTkLabel(self, text="Logs", font=('Arial', 15))
        self.middle_main_label.grid(row=0, column=1, padx=5, pady=5)

        """Right Column"""
        self.right_main_label = ctk.CTkLabel(self, text="Misc.", font=('Arial', 15))
        self.right_main_label.grid(row=0, column=2, padx=5, pady=5)


        """Footer"""

        self.footer = ctk.CTkLabel(self, text="© 2025 Evan Howell - All rights reserved", font=("Arial", 12))
        self.footer.grid(row=6, column=0, columnspan=3, sticky="we", padx=10, pady=(20, 10))

        # Switch
        #self.switch = ctk.CTkSwitch(self, text="Toggle me")
        #self.switch.pack(pady=10)

    def local_ip(self):
        ip_address = get_local_ip()
        self.left_label.configure(text=f"local IP Address: {ip_address[0]}")
    
    def local_socket(self):
        socket = get_local_ip()[1]
        self.left_label.configure(text=f"current local Socket: {socket}")




if __name__ == "__main__":
    app = App()
    app.mainloop()

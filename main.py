import customtkinter as ctk
import socket
import threading
from scapy.all import sniff


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
        self.geometry("800x600")

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

        #adding scroll frame for logs
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=400, height=300)
        self.scroll_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        #adding another grid for better ui design
        self.middle_frame = ctk.CTkFrame(self)
        self.middle_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        self.sniff_button = ctk.CTkButton(self.middle_frame, text="Start Sniffing", command=lambda: self.start_sniffing(10000))
        self.sniff_button.grid(row=0, column=0, padx=5, pady=5)

        self.clear_scroll_frame_button = ctk.CTkButton(self.middle_frame, text="clear scroll", command=self.clear_scroll_frame)
        self.clear_scroll_frame_button.grid(row=0, column=1, padx=5, pady=5)

        """Right Column"""
        self.right_main_label = ctk.CTkLabel(self, text="Misc.", font=('Arial', 15))
        self.right_main_label.grid(row=0, column=2, padx=5, pady=5)

        self.right_button = ctk.CTkButton(self, text="placeholder button", command="")
        self.right_button.grid(row=1, column=2, padx=5, pady=5)

        """Footer"""
        self.footer = ctk.CTkLabel(self, text="© 2025 Evan Howell - All rights reserved", font=("Arial", 12))
        self.footer.grid(row=6, column=0, columnspan=3, sticky="we", padx=10, pady=(20, 10))

    def local_ip(self):
        ip_address = get_local_ip()
        self.left_label.configure(text=f"local IP Address: {ip_address[0]}")
    
    def local_socket(self):
        socket = get_local_ip()[1]
        self.left_label.configure(text=f"current local Socket: {socket}")

    def populate_scroll_frame(self):
        for i in range(30):
            label = ctk.CTkLabel(self.scroll_frame, text=f"Item {i + 1}")
            label.pack(pady=5, padx=10, anchor="w")    
 
    def clear_scroll_frame(self):
        # Clears the labels within the scroll frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        # Moves the scroll bar to the original position
        try:
            self.scroll_frame._parent_canvas.yview_moveto(0)
        except AttributeError:
            pass # fixes possible error with scroll frame not being scrollable yet. 
    
    def start_sniffing(self, packet_count=10):
        thread = threading.Thread(target=self.sniff_packets, args=(packet_count,))
        thread.daemon = True
        thread.start()

    def sniff_packets(self, packet_count):
        sniff(prn=self.display_packet, count=packet_count, store=False)

    def display_packet(self, packet):
        summary = packet.summary()
        # Use `after()` to safely update the GUI from another thread
        self.after(0, self.add_packet_to_scroll_frame, summary)

    def add_packet_to_scroll_frame(self, text):
        label = ctk.CTkLabel(self.scroll_frame, text=text, anchor="w")
        label.pack(pady=2, padx=10, anchor="w")
if __name__ == "__main__":
    app = App()
    app.mainloop()

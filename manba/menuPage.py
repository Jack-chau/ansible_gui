import customtkinter as ctk
from PIL import Image

class SwitchMenu(ctk.CTkFrame):
    def __init__(self, master, show_page_callback):
        super().__init__(master)
        self.show_page_callback = show_page_callback
        self.grid(row=0, column=0, rowspan=4, sticky="ns")

        # 設定按鈕圖示
        self.docker_icon = ctk.CTkImage(Image.open("images/docker.png"), size=(30, 30))
        self.ansible_icon = ctk.CTkImage(Image.open("images/ansible.png"), size=(30, 30))

        # Docker 按鈕
        self.docker_btn = ctk.CTkButton(
            self,
            text="",
            image=self.docker_icon,
            width=50,
            height=50,
            fg_color="transparent",
            hover_color="#444444",
            command=lambda: self.show_page_callback("docker")
        )
        self.docker_btn.pack(pady=(20, 10))

        # Ansible 按鈕
        self.ansible_btn = ctk.CTkButton(
            self,
            text="",
            image=self.ansible_icon,
            width=50,
            height=50,
            fg_color="transparent",
            hover_color="#444444",
            command=lambda: self.show_page_callback("ansible")
        )
        self.ansible_btn.pack(pady=(0, 10))
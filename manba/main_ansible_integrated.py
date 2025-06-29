import customtkinter as ctk
from menuPage import SwitchMenu
from dockerPage import ContainerManagement
from automationPage import AutomationPage  # 新增模組

def main():
    app = Notorious()
    app.mainloop()

class Notorious(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('./theme/rime.json')
        ctk.set_widget_scaling(1.0)

        self.title("Dream Big")
        self.geometry(f'{1800}x{1200}+180+80')

        # Layout
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=2)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=15)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Menu Page
        self.switch_menu = SwitchMenu(self, self.show_page)

        # Pages
        self.containerManagement = ContainerManagement(self)
        self.containerManagement.grid(row=0, column=4, rowspan=4, sticky="nsew")

        self.automationPage = AutomationPage(self)
        self.automationPage.grid(row=0, column=4, rowspan=4, sticky="nsew")
        self.automationPage.grid_remove()  # 初始不顯示

    def show_page(self, page_name):
        self.containerManagement.grid_remove()
        self.automationPage.grid_remove()

        if page_name == "docker":
            self.containerManagement.grid()
        elif page_name == "ansible":
            self.automationPage.grid()

if __name__ == "__main__":
    main()
import customtkinter
import pywinstyles

root = customtkinter.CTk()

pywinstyles.change_header_color(root, color="blue")
pywinstyles.apply_style(root, style='acrylic')

root.mainloop()
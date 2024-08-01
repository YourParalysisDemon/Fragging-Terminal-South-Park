import customtkinter as ck
import PIL
import pymem.exception
from PIL import Image
from pymem import *
from pymem.process import *
from pymem.ptypes import RemotePointer


# The game were hacking
mem = Pymem("SouthPark_TFBW")
# The dll we write to
module = module_from_name(mem.process_handle, "SouthPark_TFBW.exe").lpBaseOfDll
# static pointer offsets
health_offsets = [0x448, 0x110, 0x0, 0x0, 0x50, 0x438, 0x24]


def getpointeraddress(base, offsets):
    remote_pointer = RemotePointer(mem.process_handle, base)
    for offset in offsets:
        if offset != offsets[-1]:
            remote_pointer = RemotePointer(mem.process_handle, remote_pointer.value + offset)
        else:
            return remote_pointer.value + offset


def health_hack():
    addr = getpointeraddress(module + 0x03CDD688, health_offsets)
    if addr is not None:
        try:
            mem.write_int(addr, 0x57550000)
        except pymem.exception.MemoryWriteError as e:
            print(f"Error writing memory: {e}")


class App(ck.CTk):
    width = 300
    height = 300

    def __init__(self):
        super().__init__()
        s = self
        s.title("Fragging Terminal")
        s.geometry(f"{s.width}x{s.height}")
        s.attributes("-topmost", 1)
        s.resizable(False, False)

        # Menu background
        image = PIL.Image.open("back/back.jpg")
        background_image = ck.CTkImage(image, size=(540, 480))
        bg_lbl = ck.CTkLabel(s, text="", image=background_image)
        bg_lbl.place(x=0, y=0)

        # Menu buttons
        s.button = ck.CTkButton(s, text="Health", fg_color="black", bg_color="black", text_color="red",
                                hover_color="gray", command=health_hack)
        s.button.grid(row=0, column=0, padx=20, pady=10)
        s.button = ck.CTkButton(s, text="Exit Menu", fg_color="red", bg_color="red", text_color="black",
                                hover_color="gray", command=s.destroy)
        s.button.grid(row=1, column=0, padx=20, pady=10)


# End loop
if __name__ == "__main__":
    app = App()
    app.mainloop()

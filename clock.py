from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from datetime import datetime
from math import sin, cos, radians


class Clock:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI Analog Clock")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#021e2f")

        title = Label(self.root, text="Webcode Analog Clock", font=("times new roman", 50, "bold"), bg="#04444a",
                      fg="white")
        title.pack()

        self.lbl = Label(self.root, bg="white", bd=20, relief=RAISED)
        self.lbl.place(x=450, y=150, height=400, width=400)

        self.working()

    def clock_image(self, hr, min_, sec_):
        clock = Image.new("RGB", (400, 400), (255, 255, 255))
        draw = ImageDraw.Draw(clock)

        # Background image
        bg = Image.open("c1.png")
        bg = bg.resize((300, 300), Image.LANCZOS)
        clock.paste(bg, (50, 50))

        origin = 200, 200
        draw.line((origin, 200 + 50 * sin(radians(hr)), 200 - 50 * cos(radians(hr))), fill="black", width=4)
        draw.line((origin, 200 + 80 * sin(radians(min_)), 200 - 80 * cos(radians(min_))), fill="blue", width=3)
        draw.line((origin, 200 + 100 * sin(radians(sec_)), 200 - 100 * cos(radians(sec_))), fill="green", width=2)
        draw.ellipse((195, 195, 210, 210), fill="black")

        clock.save("clock_new.png")

    def working(self):
        h = datetime.now().hour
        m = datetime.now().minute
        s = datetime.now().second

        hr = (h % 12 + m / 60 + s / 3600) * 30  # 360 degrees / 12 hours
        min_ = (m + s / 60) * 6  # 360 degrees / 60 minutes
        sec_ = s * 6  # 360 degrees / 60 seconds

        self.clock_image(hr, min_, sec_)
        self.img = ImageTk.PhotoImage(file="clock_new.png")
        self.lbl.config(image=self.img)
        self.lbl.after(1000, self.working)  # Update every second


root = Tk()
obj = Clock(root)
root.mainloop()

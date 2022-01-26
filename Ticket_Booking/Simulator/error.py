import tkinter as tk
import tkinter.messagebox
import requests

class Error:
    def __init__(self):
        self.window_width = 1300
        self.window_height = 900
        self.podCheckboxes = {}
        self.selected_box = []
        self.BASE_URL = "http://127.0.0.1:5657"
        self.errors = 0

    def main(self):
        root = tk.Tk()
        root.configure(bg='black')
        root.title('Pod Error')
        root.geometry(f'{self.window_width}x{self.window_height}')
        root.resizable(False, False)
        canvas = tk.Canvas(root)
        canvas.config(height=600, width=1066, bg="black", highlightthickness=0)
        canvas.place(x=100, y=65)
        self.rectangles(canvas)
        # self.initCheckboxes(root)
        deactivateButton = tk.Button(root, background='red', text="DEACTIVATE",width =  10,height = 2,
                                     command=lambda: self.Send_Deactivation(),borderwidth=0)
        deactivateButton.place(x=480, y=800)
        reactivateButton = tk.Button(root, background='red', text="REACTIVATE", width=10, height=2,
                                     command=lambda: self.Send_Reactivation(), borderwidth=0)
        reactivateButton.place(x=600, y=800)
        root.mainloop()

    def rectangles(self, canvas):
        for i in range(13):
            for j in range(2, 8):
                Platform_Label = tk.Label(canvas, text=f"{i + 1}", fg="white", bg="black")
                Platform_Label.grid(row=1, column=i, pady=3, padx=6)
                bt = tk.Button(canvas, bg="green", height=5, width=4,command = lambda row = i, col =  j: self.select_button(row,col))
                self.podCheckboxes[f"{i+1}X{j-2}"] =  bt
                bt.grid(row=j + 1, column=i, pady=5, padx=12)

    def select_button(self,i,j):
        print(f"The value of i is {i}")
        print(f"The value of j is {j}")
        if(len(self.selected_box)<2 and f"{i}X{j-2}" not in self.selected_box ):
            self.podCheckboxes[f"{i+1}X{j-2}"].config(bg = "red")
            self.selected_box.append(f"{i}X{j-2}")
            print(self.selected_box)
        elif(len(self.selected_box)>=2 and f"{i}X{j-2}" not in self.selected_box):
            tkinter.messagebox.showerror(title = "Error - POD Selection",message = "You can deactivate only 2 boxes at once")
        elif(f"{i}X{j-2}" in self.selected_box):
            self.podCheckboxes[f"{i + 1}X{j - 2}"].config(bg="green")
            self.selected_box.remove(f"{i}X{j - 2}")
            print(self.selected_box)

    def toggle(self):  # to toggle
        if self.errors == 2:
            print("Cannot exceed 2 failures")
            self.resetActive()
            self.errors = 0
        else:
            self.errors += 1

    def resetActive(self):  # Resets any active squares
        for i in range(13):
            for j in range(6):
                if self.podCheckboxes[i][j].instate(['selected']):
                    self.podCheckboxes[i][j].state(['!selected'])

    def Send_Deactivation(self):
        S = ",".join(self.selected_box)
        print(S)
        d  = requests.post(f"{self.BASE_URL}/PodBroken/{S}").json()
        print(d)

    def Send_Reactivation(self):
        S = ",".join(self.selected_box)
        print(S)
        d = requests.post(f"{self.BASE_URL}/Repair/{S}").json()
        print(d)


obj = Error()
obj.main()

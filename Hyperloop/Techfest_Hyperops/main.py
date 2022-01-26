import sys
import time
import tkinter
import threading
#import keyboard


class Simulator:
    def __init__(self):
        self.ARRANGEMENT: list = []  # CURRENT ARRANGEMENT FOR SENDING THE CONVOYS
        self.CONVOYDISTANCE: int = 0  # DISTANCE BETWEEN TWO CONVOYS
        self.EXIT = False
        self.GRID_REF_DICT = {}
        self.Mumbai_Portal = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]  # DEFAULT LAYOUT OF THE MUMBAI PORTAL (1-TRUE/0-FALSE).
        self.matrix = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.Option_Menu =  {1:[1,1,1,1,1,1],2:[2,1,1,1,1],3:[2,2,1,1],4:[3,1,1,1],5:[4,1,1],6:[2,2,2],7:[3,2,1],8:[5,1],9:[2,4],10:{3,3},11:{6},12: "EXIT"}

    #def Exit_Listener(self):
    #    while True:
    #        if keyboard.is_pressed("q") == True:
    #            self.EXIT = True
            #    sys.exit(0)
            #     break

    def Startup_Grid_Maker(self):
        for i in range(1, 7):
            for j in range(1, 14):
                Grid_Square = tkinter.Label(self.Mumbai_Portal_Screen, width="5", height="2", text="", bg="red")
                Grid_Square.grid(row=i, column=j, pady=2, padx=2)
                key = str(i) + str(j)
                self.GRID_REF_DICT[key] = Grid_Square

    def Final_Layout(self,Cell_List):

        self.Mumbai_Portal_Final =  self.Mumbai_Portal
        for j in range(len(Cell_List)):
            for i in range(6):
                self.Mumbai_Portal_Final[i][Cell_List[j]] = 0
        k =  self.Mumbai_Portal

    def Update_Screen(self):
        for i in range(6):
            for j in range(13):
                if(self.matrix[i][j] ==  0):
                    key =  str(i+1)+str(j+1)
                    self.GRID_REF_DICT[key].config(bg =  "green")


    def Rotate_List(self):

        list_to_be_rotated = self.method
        output_list = []
        num =  1
        for item in range(len(list_to_be_rotated) - num, len(list_to_be_rotated)):
            output_list.append(list_to_be_rotated[item])

        for item in range(0, len(list_to_be_rotated) - num):
            output_list.append(list_to_be_rotated[item])

        return output_list

    def Controller(self):
        # self.Exit_Listner_thread = threading.Thread(target=self.Exit_Listener)
        # self.Exit_Listner_thread.start()
        Option = self.Option
        Cell_list :list =  self.cell_list
        self.method =  self.Option_Menu[Option]
        self.Final_Layout(Cell_list)
        while self.EXIT != True or self.Mumbai_Portal_Final != self.matrix:
            o =  self.matrix
            for j in range(len(Cell_list)): #[1,2,3,4,5,6] ---> 0
                    self.counter = 0
                    for l in range(self.method[j]): #[2,1,1,1,1,1
                        for i in range(6):
                            o = self.matrix
                            if(self.matrix[i][Cell_list[j]]==1):
                                print(f"The value of f is {i}")
                                self.matrix[i][Cell_list[j]] = 0
                                self.counter =  self.counter  + 1
                                break


            self.Update_Screen()
            self.method = self.Rotate_List()
            time.sleep(30)



        sys.exit(0)


    def main(self):
        self.Input_Selection()
        self.Mumbai_Portal_Screen = tkinter.Tk()
        self.Startup_Grid_Maker()
        Thread_Controller = threading.Thread(target =  self.Controller)
        Thread_Controller.start()
        self.Mumbai_Portal_Screen.mainloop()

    def Input_Selection(self):
        self.Option = int(input(
            "Please enter the arrangement which you want to use\n1, 1, 1, 1, 1, 1\n2)2, 1, 1, 1, 1\n3)2, 2, 1, "
            "1\n4)3, 3, 1, 1\n5)1, 1, 4\n6)2,2,2\n7)3,2,1\n8)1,5\n9)2,4\n10)3,3\n11)6\n12)Exit\n--------------------> "))
        if self.Option == 12:
            sys.exit()
        else:
            cells = input("Which rows do you want to apply the arrangement(Separate the rows by commas): ")
            self.cell_list = cells.split(",")
            for i in range(0, len(self.cell_list)):
                self.cell_list[i] = int(self.cell_list[i])



Simulator().main()

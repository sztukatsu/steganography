#Kevin Tu
#Finals


from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
from PIL import Image

class Application(Frame):
    """creates GUI interface"""
    
    def __init__(self,master):
        """initializes the frame"""
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()

    def str_bin(self,s):
        ords = (ord(c) for c in s)
        shifts = (7,6,5,4,3,2,1,0)
        return [(o >> shift) & 1 for o in ords for shift in shifts]

    def create_widgets(self):
        """creates the widgets"""
        #instruction label
        self.opt = StringVar()
        self.pic_trig = "false"
        self.doc_trig = "false"
        
        self.inst_lbl = Label(self,text="Kevin Tu's Steganography Encoder")
        self.inst_lbl.grid(row = 0, column = 0, columnspan = 2)
        
        self.radio1 = Radiobutton(self,text = "\nEncode Message\n", value = "msg", variable = self.opt)
        self.radio1.grid(row = 1, column = 0, sticky = W)

        self.lbl = Label(self, text="Message:")
        self.lbl.grid(row = 1, column =1, sticky = E)

        self.entry = Entry(self)
        self.entry.grid(row = 1, column = 2, sticky = W, columnspan= 3)

        self.radio2 = Radiobutton(self,text = "\nEncode Text File\n", value = "txt", variable = self.opt)
        self.radio2.grid(row =2, column = 0, sticky = W)

        self.upload = Button(self, text = "Open File",command = self.askopenfile)
        self.upload.grid(row = 2, column = 1, sticky = E)

        self.direc = Entry(self)
        self.direc.grid(row = 2, column = 2, sticky = W, columnspan = 3)

        self.lbl = Label(self, text="Host Picture:\n")
        self.lbl.grid(row = 3, column = 0)

        self.upload2 = Button(self, text = "Open File",command = self.askopenfile2)
        self.upload2.grid(row = 3, column = 1, sticky = E)

        self.pic = Entry(self)
        self.pic.grid(row = 3, column = 2, sticky = W, columnspan = 3)

        self.submit_bttn = Button(self,text = "Encode!", command = self.procedure)
        self.submit_bttn.grid(row = 10, column = 0)
        
        self.status = Text(self, width = 50, height = 5, wrap = WORD)
        self.status.grid(row = 11, column = 0, columnspan = 3)

        self.file_opt2 = options = {}
        options['defaultextension'] = '.png'
        options['filetypes'] = [('png images', '.png')]
        options['initialdir'] = '%homepath%/Downloads/'
        options['title'] = 'sztukatsu'

        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('text files', '.txt')]
        options['initialdir'] = '%homepath%/Downloads/'
        options['title'] = 'sztukatsu'

    def askopenfile(self):
        self.filename = tkFileDialog.askopenfilename(**self.file_opt)
        self.direc.delete(0, END)
        self.direc.insert(0, self.filename)
        self.doc_trig = "true"
    
    def askopenfile2(self):
        self.filename2 = tkFileDialog.askopenfilename(**self.file_opt2)
        self.pic.delete(0, END)
        self.pic.insert(0, self.filename2)
        self.pic_trig = "true"

    def update(self,txt):
        self.output_txt += txt
        self.output_txt += "\n"
        self.status.delete(0.0,END)
        self.status.insert(0.0,self.output_txt)

    def asksaveasfile(self):
        self.filename3 =  tkFileDialog.asksaveasfilename(**self.file_opt2)
    
    def procedure(self):
        con_proc = "t"
        self.output_txt = ""
        self.status.delete(0.0, END)
        if self.pic_trig == "true":
            self.update("host image found")
            image = Image.open(self.filename2)
            (width, height) = image.size
            self.update("host image " + str(width) + " by " + str(height) + " pixels")
        else:
            self.update("ERROR:\nno host image found")
            con_proc = "f"
        if self.opt.get():
            if self.opt.get() == "msg":
                pre_text = self.entry.get()
            elif self.opt.get() == "txt":
                if self.doc_trig == "true":
                    with open(self.filename,"r") as myfile:
                        pre_text = myfile.read()
                else:
                    self.update("ERROR:\nno text file found")
            else:
                self.update("ERROR:\nencode option not selected properly")
                con_proc = "f"
        else:
            self.update("ERROR:\nplease select an encode option")
            con_proc = "f"
        if con_proc == "t":
            if len(pre_text) >= 1:
                bomb = [1,0,1,1,0,0,1,0]
                bin_text = bomb + self.str_bin(pre_text) + bomb
                if len(bin_text) >  (width * height)/3:
                    self.update("ERROR:\nMessage too large for designated image")
                else:
                    composite = [bin_text[x:x+8] for x in range(0,len(bin_text),8)]
                    mod_range = len(composite)
                    mod_x = int((image.size[0])/3)
                    mod_y = int(mod_range/mod_x)
                    if mod_y == 0:
                        self.update("encoding 1 line of pixels")
                        x_coord = 0
                        for i in range(mod_range):
                            r1,g1,b1 = image.getpixel((x_coord,0))
                            r2,g2,b2 = image.getpixel((x_coord+1,0))
                            r3,g3,b3 = image.getpixel((x_coord+2,0))
                            mod_seq = [r1,g1,b1,r2,g2,b2,r3,g3,b3]
                            for l in range(len(mod_seq)):
                                mod_seq[l] =int('{0:08b}'.format(mod_seq[l]))
                            mod_bin = composite[i]
                            for e in range(len(mod_bin)):
                                if mod_seq[e]%10 == 0:
                                    mod_seq[e] = mod_seq[e] + mod_bin[e]
                                else:
                                    mod_seq[e] = mod_seq[e] - 1 + mod_bin[e]
                            for j in range(len(mod_seq)):
                                mod_seq[j] = int(str(mod_seq[j]),2)
                            image.putpixel((x_coord,0),(mod_seq[0],mod_seq[1],mod_seq[2]))
                            image.putpixel((x_coord+1,0),(mod_seq[3],mod_seq[4],mod_seq[5]))
                            image.putpixel((x_coord+2,0),(mod_seq[6],mod_seq[7],int(mod_seq[8])))
                            x_coord += 3
                    else:
                        self.update("encoding " + str(mod_y) + " lines of pixels")
                        for z in range(mod_y):
                            x_coord = 0
                            for i in range(mod_x):
                                r1,g1,b1 = image.getpixel((x_coord,z))
                                r2,g2,b2 = image.getpixel((x_coord+1,z))
                                r3,g3,b3 = image.getpixel((x_coord+2,z))
                                mod_seq = [r1,g1,b1,r2,g2,b2,r3,g3,b3]
                                for l in range(len(mod_seq)):
                                    mod_seq[l] =int('{0:08b}'.format(mod_seq[l]))
                                mod_bin = composite[i]
                                for e in range(len(mod_bin)):
                                    if mod_seq[e]%10 == 0:
                                        mod_seq[e] = mod_seq[e] + mod_bin[e]
                                    else:
                                        mod_seq[e] = mod_seq[e] - 1 + mod_bin[e]
                                for j in range(len(mod_seq)):
                                    mod_seq[j] = int(str(mod_seq[j]),2)
                                image.putpixel((x_coord,z),(mod_seq[0],mod_seq[1],mod_seq[2]))
                                image.putpixel((x_coord+1,z),(mod_seq[3],mod_seq[4],mod_seq[5]))
                                image.putpixel((x_coord+2,z),(mod_seq[6],mod_seq[7],int(mod_seq[8])))
                                x_coord += 3
                        x_coord = 0
                        for g in range(mod_range%mod_y):
                            r1,g1,b1 = image.getpixel((x_coord,mod_y+1))
                            r2,g2,b2 = image.getpixel((x_coord+1,mod_y+1))
                            r3,g3,b3 = image.getpixel((x_coord+2,mod_y+1))
                            mod_seq = [r1,g1,b1,r2,g2,b2,r3,g3,b3]
                            for l in range(len(mod_seq)):
                                 mod_seq[l] =int('{0:08b}'.format(mod_seq[l]))
                            mod_bin = composite[i]
                            for e in range(len(mod_bin)):
                                if mod_seq[e]%10 == 0:
                                    mod_seq[e] = mod_seq[e] + mod_bin[e]
                                else:
                                    mod_seq[e] = mod_seq[e] - 1 + mod_bin[e]
                            for j in range(len(mod_seq)):
                                mod_seq[j] = int(str(mod_seq[j]),2)
                            image.putpixel((x_coord,mod_y+1),(mod_seq[0],mod_seq[1],mod_seq[2]))
                            image.putpixel((x_coord+1,mod_y+1),(mod_seq[3],mod_seq[4],mod_seq[5]))
                            image.putpixel((x_coord+2,mod_y+1),(mod_seq[6],mod_seq[7],int(mod_seq[8])))
                            x_coord += 3
                        
            else:
                self.update("ERROR:\nNo text to hide")
            self.asksaveasfile()
            image.save(self.filename3)
            self.update("encoding successful")

def main():
    """This creates the root window and loops it"""
    root = Tk()
    Application(root).pack()
    root.title("sztukatsu")
    root.geometry("500x300")
    app = Application(root)
    root.mainloop()

main()

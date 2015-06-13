#Kevin Tu
#Finals

from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
from PIL import Image


class Application(Frame):
    """creates GUI"""

    def __init__(self,master):
        """initializes the frame"""
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """creates the widgets"""

        self.pic_trig = "false"
        
        self.inst_lbl = Label(self,text="K2's steganography tool")
        self.inst_lbl.grid(row = 0, column = 0, columnspan = 2)
        
        self.upload = Button(self,text="Open Image:", command = self.askopenfile2)
        self.upload.grid(row = 1, column = 0, sticky = E)
        
        self.pic = Entry(self)
        self.pic.grid(row = 1, column = 1, sticky = W)

        self.lbl = Label(self, text = "")
        self.lbl.grid(row = 2)
        
        self.submit_bttn = Button(self,text = "Decode!", command = self.decode)
        self.submit_bttn.grid(row = 3, column = 0)
        
        self.status = Text(self, width = 35, height = 5, wrap = WORD)
        self.status.grid(row = 4, column = 0, sticky = W, columnspan = 2)

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

    def bin_char(self,bl):
        bi = iter(bl)
        bytes = zip(*(bi,) * 8)
        shifts = (7,6,5,4,3,2,1,0)
        for byte in bytes:
            yield chr(sum(bit << s for bit, s in zip(byte, shifts)))

    def bin_str(self,bl):
        return ''.join(self.bin_char(bl))

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
        self.filename3 =  tkFileDialog.asksaveasfilename(**self.file_opt)
    
    def decode(self):
        from PIL import Image
        self.status.delete(0.0, END)
        con_proc = "t"
        self.output_txt = ""
        if self.pic_trig == "true":
            if self.filename2 != "":
                self.update("host image found")
                image = Image.open(self.filename2)
                (width, height) = image.size
            else:
                self.update("ERROR:\nno host image found")
                con_proc = "f"
        else:
            self.update("ERROR:\nno host image found")
            con_proc = "f"
        if con_proc == "t":
            r1,g1,b1 = image.getpixel((0,0))
            r2,g2,b2 = image.getpixel((1,0))
            r3,g3,b3 = image.getpixel((2,0))
            mod_seq = [r1,g1,b1,r2,g2,b2,r3,g3]
            check_start = 0
            for l in range(len(mod_seq)):
                check_start = check_start*10 + mod_seq[l]%2
            if check_start == 10110010:
                self.update("encoded message found")
                x_pix = int(width/3)
                dec_bin = []
                end = "false"
                x_coord = 3
                y_coord = 0
                while end == "false":
                    r1,g1,b1 = image.getpixel((x_coord,y_coord))
                    r2,g2,b2 = image.getpixel((x_coord+1,y_coord))
                    r3,g3,b3 = image.getpixel((x_coord+2,y_coord))
                    mod_seq = [r1,g1,b1,r2,g2,b2,r3,g3]
                    for l in range(len(mod_seq)):
                        mod_seq[l] = mod_seq[l]%2
                    if mod_seq == [1,0,1,1,0,0,1,0]:
                        end = "true"
                    else:
                        dec_bin += mod_seq
                        if x_coord +3 == x_pix*3:
                            y_coord += 1
                            x_coord = 0
                        else:
                            x_coord +=3
                message = self.bin_str(dec_bin)
                self.asksaveasfile()
                file = open(self.filename3, "w")
                file.write(message)
                file.close()
                self.update("decoding successful")
                
            else:
                self.update("no encoded message found")

def main():
    """This creates the root window and loops it"""
    root = Tk()
    Application(root).pack()
    root.title("sztukatsu")
    root.geometry("300x200")
    app = Application(root)
    root.mainloop()

main()

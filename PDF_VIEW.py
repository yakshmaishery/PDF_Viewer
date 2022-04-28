from tkinter import *
from tkinter import ttk,filedialog,messagebox
import os
import fitz
from PIL import Image,ImageTk

class Application:
    def __init__(self):
        self.FileURL=""
        self.FileName=""
        self.Pointer=0
        self.total_pdf_pages=0
        self.Ratio=0.5
        self.FullScreen_Active=False
        pass

    def User_Interface(self,*args):
        self.root=Tk()
        self.root.title("Untitled")
        self.root.rowconfigure(0,weight=1)
        self.root.columnconfigure(0,weight=1)
        self.root.state("zoomed")
        # main canvas
        self.MainCanvas=Canvas(self.root,bg="#000064",highlightthickness=0)
        self.MainCanvas.grid(row=0,column=0,padx=0,pady=0,sticky="nswe")
        # sidebar
        self.SideBar=Frame(self.root,highlightthickness=1,highlightbackground="yellow",highlightcolor="yellow",bg="#000064")
        Button(self.SideBar,text="OPEN",command=self.Open_FUNC,bg="#00002d",fg="white",font=("arial",12),cursor="hand2",activebackground="#000064",activeforeground="white",relief=SOLID).grid(row=0,column=0,padx=2,pady=2,sticky="nswe")
        Button(self.SideBar,text="FULLSCREEN",command=self.FullScreen_FUNC,bg="#00002d",fg="white",font=("arial",12),cursor="hand2",activebackground="#000064",activeforeground="white",relief=SOLID).grid(row=0,column=1,padx=2,pady=2,sticky="nswe")
        Button(self.SideBar,text="RESET",command=self.Reset_FUNC,bg="#00002d",fg="white",font=("arial",12),cursor="hand2",activebackground="#000064",activeforeground="white",relief=SOLID).grid(row=0,column=2,padx=2,pady=2,sticky="nswe")
        Button(self.SideBar,text="◀ Previous",command=self.Previous_FUNC,bg="#00002d",fg="white",font=("arial",12),cursor="hand2",activebackground="#000064",activeforeground="white",relief=SOLID).grid(row=0,column=3,padx=2,pady=2,sticky="nswe")
        Button(self.SideBar,text="Next ▶",command=self.Next_FUNC,bg="#00002d",fg="white",font=("arial",12),cursor="hand2",activebackground="#000064",activeforeground="white",relief=SOLID).grid(row=0,column=4,padx=2,pady=2,sticky="nswe")

        self.L1=Label(self.SideBar,bg="#000064",fg="yellow",font=("arial",12))
        self.L1.grid(row=0,column=5,padx=2,pady=2,sticky="nsew")
        self.SideBar.grid(row=1,column=0,padx=0,pady=0,sticky="nswe")

        self.MainCanvas.bind("<ButtonPress-1>",self.SCAN_MARKING)
        self.MainCanvas.bind("<B1-Motion>",self.SCAN_DRAGING)
        self.MainCanvas.bind("<MouseWheel>",self.ScrollBars)
        self.MainCanvas.bind("<Control MouseWheel>",self.Change_Ratio)
        self.root.bind("<Right>",self.Next_FUNC)
        self.root.bind("<Left>",self.Previous_FUNC)
        self.root.bind("<Up>",self.UP_KEY)
        self.root.bind("<Down>",self.DOWN_KEY)
        self.root.bind("<Control-o>",self.Open_FUNC)
        self.root.mainloop()
        pass

    def SCAN_MARKING(self,e):
        self.MainCanvas.scan_mark(e.x,e.y)

    def SCAN_DRAGING(self,e):
        self.MainCanvas.scan_dragto(e.x,e.y,gain=1)

    def ScrollBars(self,e):
        self.MainCanvas.yview_scroll(int(-1/e.delta*120),UNITS)

    def Change_Ratio(self,e):
        try:
            if self.FileURL!="":
                if e.delta==120:
                    self.Ratio+=0.05
                elif e.delta==-120:
                    sizes=self.Ratio-0.05
                    if sizes>=0:
                        self.Ratio-=0.05
                    else:
                        self.Ratio=0.5
                doc=fitz.open(self.FileURL)
                page = doc.load_page(self.Pointer)
                mat=fitz.Matrix(3,3)
                pix = page.get_pixmap(matrix=mat)
                im=Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                H,W=im.size
                im=im.resize((int(H*self.Ratio),int(W*self.Ratio)))
                img=ImageTk.PhotoImage(im)
                self.MainCanvas.delete(ALL)
                self.MainCanvas.create_image((0,0),anchor="nw",image=img)
                self.MainCanvas.image=img
                self.MainCanvas.config(scrollregion=self.MainCanvas.bbox(ALL))
        except:
            pass

    def Open_FUNC(self,*args):
        files=filedialog.askopenfilename(defaultextension=".pdf")
        if files!="":
            doc=fitz.open(files)
            self.total_pdf_pages=int(doc.page_count)
            self.L1.config(text=f"Pages = {self.Pointer+1} / {self.total_pdf_pages}")
            self.FileURL=files
            self.FileName=os.path.basename(self.FileURL)
            self.root.title(self.FileName)

            page = doc.load_page(self.Pointer)
            mat=fitz.Matrix(3,3)
            pix = page.get_pixmap(matrix=mat)
            im=Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            H,W=im.size
            im=im.resize((int(H*self.Ratio),int(W*self.Ratio)))
            img=ImageTk.PhotoImage(im)
            self.MainCanvas.delete(ALL)
            self.MainCanvas.create_image((0,0),anchor="nw",image=img)
            self.MainCanvas.image=img
            self.MainCanvas.config(scrollregion=self.MainCanvas.bbox(ALL))
        pass

    def Next_FUNC(self,*args):
        self.Pointer=self.Pointer+1
        if self.Pointer<self.total_pdf_pages:
            doc=fitz.open(self.FileURL)
            self.total_pdf_pages=int(doc.page_count)
            self.L1.config(text=f"Pages = {self.Pointer+1} / {self.total_pdf_pages}")
            page = doc.load_page(self.Pointer)
            mat=fitz.Matrix(3,3)
            pix = page.get_pixmap(matrix=mat)
            im=Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            H,W=im.size
            im=im.resize((int(H*self.Ratio),int(W*self.Ratio)))
            img=ImageTk.PhotoImage(im)
            self.MainCanvas.delete(ALL)
            self.MainCanvas.create_image((0,0),anchor="nw",image=img)
            self.MainCanvas.image=img
            self.MainCanvas.config(scrollregion=self.MainCanvas.bbox(ALL))
            self.MainCanvas.yview_moveto(0.0)
        else:
            self.Pointer-=1
        pass

    def Previous_FUNC(self,*args):
        self.Pointer=self.Pointer-1
        if self.Pointer>=0:
            doc=fitz.open(self.FileURL)
            self.total_pdf_pages=int(doc.page_count)
            self.L1.config(text=f"Pages = {self.Pointer+1} / {self.total_pdf_pages}")
            page = doc.load_page(self.Pointer)
            mat=fitz.Matrix(3,3)
            pix = page.get_pixmap(matrix=mat)
            im=Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            H,W=im.size
            im=im.resize((int(H*self.Ratio),int(W*self.Ratio)))
            img=ImageTk.PhotoImage(im)
            self.MainCanvas.delete(ALL)
            self.MainCanvas.create_image((0,0),anchor="nw",image=img)
            self.MainCanvas.image=img
            self.MainCanvas.config(scrollregion=self.MainCanvas.bbox(ALL))
            self.MainCanvas.yview_moveto(1.0)
        else:
            self.Pointer+=1
        pass

    def Reset_FUNC(self,*args):
        asks=messagebox.askquestion("Reset","Do you really want to reset")
        if asks=="yes":
            self.FileURL=""
            self.FileName=""
            self.Pointer=0
            self.total_pdf_pages=0
            self.Ratio=0.5
            self.root.title("Untitled")
            self.MainCanvas.delete(ALL)
            self.L1.config(text="")
            self.FullScreen_Active=True
            self.FullScreen_FUNC()

    def FullScreen_FUNC(self,*args):
        if self.FullScreen_Active==False:
            self.FullScreen_Active=True
            self.root.wm_attributes("-fullscreen",True)
        elif self.FullScreen_Active==True:
            self.FullScreen_Active=False
            self.root.wm_attributes("-fullscreen",False)
        pass

    def UP_KEY(self,*args):
        data=self.MainCanvas.yview()
        self.MainCanvas.yview_moveto(float(data[0]-0.02))
        pass

    def DOWN_KEY(self,*args):
        data=self.MainCanvas.yview()
        self.MainCanvas.yview_moveto(float(data[0]+0.02))
        pass
    pass
App=Application()
App.User_Interface()
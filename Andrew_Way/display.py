import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import time
import skills
label_font = ('Arial',18)
text_font=('Arial',16)
small_font=('Arial',12)
pad = 10
skill_list=skills.skills


class MHWBuider():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Monster Hunter Wilds Set Finder')
        self.root.geometry("1200x900")
        
        
        #========================================making as a grid
        self.frame= tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH,expand=True)
        

        self.frame.grid_columnconfigure(0,weight=1)
        self.frame.grid_columnconfigure(1,weight=1)
        self.frame.grid_columnconfigure(2,weight=1)
        self.frame.grid_rowconfigure(0,weight=1)


        #============================================================left column stuff
        self.left_column = tk.Frame(self.frame,bd=pad)
        self.left_column.grid(row=0,column=0,sticky="nsew")
        self.left_column.grid_propagate(False)

        #splitting top and bottom of left column
        self.left_column.grid_rowconfigure(0,weight=1)
        self.left_column.grid_rowconfigure(1,weight=1)
        self.left_column.grid_columnconfigure(0,weight=1)

        #===========================================Left top
        self.__create_left_top__()
        



        #Left Bottom
        self.left_bottom = tk.Frame(self.left_column)
        self.left_bottom.grid(row=1,column=0,sticky='nsew')
        self.left_bottom.grid_propagate(False)

        self.label2 = tk.Label(self.left_bottom,text="Choose Skill Level",font=label_font)
        self.label2.pack(padx=pad,pady=pad)
        #============================================================middle column stuff
        self.middle_column = tk.Frame(self.frame,bg="gray",bd=pad)
        self.middle_column.grid(row=0,column=1,sticky="nsew")
        self.middle_column.grid_propagate(False)
        #progress bar for build gen (CAUSING NOTHING ELSE TO WORK AT THE MOMENT)
        #self.build_progress = Progressbar(self.middle_column,orient=HORIZONTAL,length=300)
        #self.build_progress.pack(pady=pad)
        #self.button = Button(self.middle_column,text="Generate Builds",command = self.__progress_bar__).pack()
        #tabs for builds should go in the middle column
        self.notebook = ttk.Notebook(self.middle_column)
        build_1=Frame(self.notebook)
        build_2=Frame(self.notebook)
        build_3=Frame(self.notebook)
        build_4=Frame(self.notebook)
        build_5=Frame(self.notebook)
        self.notebook.add(build_1,text="Build 1")
        self.notebook.add(build_2,text="Build 2")
        self.notebook.add(build_3,text="Build 3")
        self.notebook.add(build_4,text="Build 4")
        self.notebook.add(build_5,text="Build 5")
        self.notebook.pack()

        
        
        
        #==============================================================right column stuff
        self.right_column = tk.Frame(self.frame,bd=pad)
        self.right_column.grid(row=0,column=2,sticky="nsew")
        self.right_column.grid_propagate(False)

        self.r_label = tk.Label(self.right_column,text="Final Skills",font=label_font)
        self.r_label.pack(padx=pad,pady=pad)
        
        
        
        #self.button=tk.Button(self.root,text="Show Message",font=label_font)
        #self.button.pack(padx=pad,pady=pad)

        self.root.mainloop()
    
    

        
   
    def __create_left_top__(self):
        self.left_top = tk.Frame(self.left_column)
        self.left_top.grid(row=0,column=0,sticky='nsew')
        #self.left_top.grid_propagate(False)
        
        #title label
        self.label = tk.Label(self.left_top,text='Choose Skills',font=label_font)
        self.label.pack(padx=pad,pady=pad,anchor='n')
        
        #searchbar
        self.search_frame = tk.Frame(self.left_top)
        self.search_frame.pack(side='top',fill='x',padx=(0,10))
        self.search_var=tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame,textvariable=self.search_var,font=small_font,width=30)
        self.search_entry.pack(side='left',fill='x',expand=True)

        self.search_entry.insert(0,"Search skills...")

        def on_focus_in(event):
            if self.search_entry.get()=="Search skills...":
                self.search_entry.delete(0,tk.END)
                self.search_entry.config(fg='black')
        
        def on_focus_out(event):
            if not self.search_entry.get():
                self.search_entry.insert(0,"Search skills...")
                self.search_entry.config(fg='gray')
        
        self.search_entry.bind('<FocusIn>',on_focus_in)
        self.search_entry.bind('<FocusOut>',on_focus_out)
        self.search_entry.config(fg='gray')
        
        self.first_filter_done = False

        def on_search_change(*args):
            self.__filter_skills__()
        
        self.search_var.trace_add('write', on_search_change)

        #=============making  a scrollbar
        self.scrollable_container = tk.Frame(self.left_top)
        self.scrollable_container.pack(fill=tk.BOTH,expand=True)

        # have to use canvas since frames are not scrollable
        self.canvas = tk.Canvas(self.scrollable_container)
        self.canvas.pack(side='left',fill='both',expand=True)

        #scrollbar
        self.scrollbar = ttk.Scrollbar(self.scrollable_container,orient='vertical',command=self.canvas.yview)
        self.scrollbar.pack(side='right',fill='y')

        #connect bar to canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.skills_btn_frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0,0),window=self.skills_btn_frame
                                                       ,anchor='nw')
        
        # update sizing when stuff changes size
        def on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        
        self.skills_btn_frame.bind('<Configure>',on_frame_configure)

        def on_canvas_configure(event):
            self.canvas.itemconfig(self.canvas_window,width=event.width)
        
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)

        self.canvas.bind("<Configure>",on_canvas_configure)

        self.__create_skill_buttons__()
        
        self.root.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    
    
    def __create_skill_buttons__(self):
        self.all_skill_buttons = {}
        
        for i, skill in enumerate(skill_list):
            self.btn=tk.Button(self.skills_btn_frame,text=skill,font=small_font,anchor='w',width=25,command=lambda s=skill: self.__on_skill_click__(s))
            self.btn.pack(fill='x',padx=pad,pady=2)
            self.all_skill_buttons[skill]=self.btn
            
    
    def __filter_skills__(self):
        search_text = self.search_entry.get()
        if search_text=="search skills...":
            search_text=''
        else:
            search_text = search_text.lower().strip()
        for skill, btn in self.all_skill_buttons.items():
            btn.pack_forget()
        for skill,btn in self.all_skill_buttons.items():
            skill_lower = skill.lower()
            if search_text==""or skill_lower.startswith(search_text):
                btn.pack(fill='x',padx=pad,pady=2)
        
        self.skills_btn_frame.update_idletasks()
    
    # Reconfigure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        self.canvas.itemconfig(self.canvas_window,window=self.skills_btn_frame)

    def __on_skill_click__(self,skill):
        print(f"Skill clicked:{skill}")

    
        
    def __progress_bar__(self):
        total_builds = len(skills)
        x=0
        while x<total_builds:
            time.sleep(1)
            self.build_progress['value']+=10
            self.root.update_idletasks()
            x+=1
    

MHWBuider()
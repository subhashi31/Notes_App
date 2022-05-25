# notes app/ journal
import calendar
import random
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from time import strftime
import datetime as dt
from PIL import ImageDraw
from fuzzywuzzy import process
import os
import pymysql

import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)


class Notes:

    def __init__(self, root):
        self.root = root
        self.root.title("Notes")
        self.root.geometry("1800x930+50+20")
        self.root.configure(background="white")
        self.root.maxsize(1800, 930)

        title=Label(text="",font=("MingLiU-ExtB 20 bold"),bg="#A7C7D9",bd=5,relief=RIDGE)
        title.pack(side=TOP,fill=X)

        def Resize_Image(image, maxsize):
            r1 = image.size[0] / maxsize[0]  # width ratio
            r2 = image.size[1] / maxsize[1]  # height ratio
            ratio = max(r1, r2)
            newsize = (int(image.size[0] / ratio), int(image.size[1] / ratio))
            image = image.resize(newsize, Image.ANTIALIAS)
            return image

        ####  Reminder Frame f1
        f1=Frame(self.root, bd=4 , bg="black")
        f1.place(x=15 ,y=50 ,width=400 ,height=273)

        ####  main frame  f2
        f2 = Frame(self.root)
        f2.place(x=430, y=50, width=1355, height=367)

        ##### recent frame f3
        f3 = Frame(self.root, bd=4, bg="black")
        f3.place(x=430, y=430, width=1355, height=490)

        ##### calendar frame f4
        f4 = Frame(self.root, bd=4, bg="black")
        f4.place(x=15, y=600, width=400, height=320)

        cimage = Image.open("cal2.jpg")
        cphoto = ImageTk.PhotoImage(cimage)

        canvasc = Canvas(f4, width=320, height=270)
        canvasc.pack(fill="both", expand=True)

        canvasc.create_image(0, 0, image=cphoto, anchor=NW)
        canvasc.photo = cphoto

        year = int(dt.date.today().strftime("%Y"))  # year
        month = int(dt.date.today().strftime("%m"))  # month number

        c = calendar.TextCalendar(calendar.SUNDAY)

        canvasc.create_text(190, 150, text=c.formatmonth(year,month), font=("Courier 16 bold"), fill="black")

        ##### picture frame f5
        f5 = Frame(self.root, bd=4, bg="black")
        f5.place(x=15, y=337, width=400, height=250)

        canvasp = Canvas(f5, width=400, height=250)
        canvasp.pack(fill="both", expand=True)

        #### Reminder frame
        f1_rf=Frame(f1, bg="#F7C5A3" , bd=3, relief=RIDGE)
        f1_rf.place(x=0,y=0,width=392,height=66)

        r1=Label(f1_rf, text="Reminder", font=("MingLiU-ExtB 15 bold"), bg="#F7C5A3")
        r1.pack(side=LEFT,padx=5)

        br = Button(f1_rf, text="~", font=("MingLiU-ExtB 11 bold"), bg="white", command=self.rem_listbox_win)
        br.pack(side=RIGHT,padx=10)

        #### Reminder entry frame
        f1_ref = Frame(f1, bg="white")
        f1_ref.place(x=0, y=66, width=391, height=66)

        # reminder entry variable
        self.reminder_entry_var = StringVar()
        self.reminder_entry_var = Entry(f1_ref, textvariable=self.reminder_entry_var, width=20, font=("MingLiU-ExtB 15 bold"),highlightbackground="black",highlightthickness=2)
        self.reminder_entry_var.pack(side=LEFT,padx=5)

        bre = Button(f1_ref, text="+", font=("MingLiU-ExtB 11 bold"), bg="#F7C5A3", command=self.add_reminder)
        bre.pack(side=RIGHT,padx=14)

        #### To do
        f1_tf = Frame(f1, bg="#F7C5A3", bd=3, relief=RIDGE)
        f1_tf.place(x=0, y=132, width=392, height=66)

        t1 = Label(f1_tf, text="To-do", font=("MingLiU-ExtB 15 bold"), bg="#F7C5A3")
        t1.pack(side=LEFT,padx=5)

        btd = Button(f1_tf, text="~", font=("MingLiU-ExtB 11 bold"), bg="white", command=self.list_box_win)
        btd.pack(side=RIGHT,padx=10)

        #### To-do entry frame
        f1_tdef = Frame(f1, bg="white")
        f1_tdef.place(x=0, y=198, width=391, height=66)

        # to-do entry variable
        self.to_do_entry_var = StringVar()
        self.to_do_entry_var = Entry(f1_tdef, textvariable=self.to_do_entry_var, width=20, font=("MingLiU-ExtB 15 bold"),highlightbackground="black",highlightthickness=2)
        self.to_do_entry_var.pack(side=LEFT,padx=5)

        btde = Button(f1_tdef, text="+", font=("MingLiU-ExtB 11 bold"), bg="#F7C5A3", command=self.get_task)
        btde.pack(side=RIGHT,padx=14)

        ##### Recent
        f3_tf = Frame(f3, bg="#F7C5A3", bd=3, relief=RIDGE)
        f3_tf.place(x=0,y=0,width=1346,height=40)

        t3 = Label(f3_tf, text="Recent", font=("MingLiU-ExtB 15 bold"), bg="#F7C5A3")
        t3.pack(side=LEFT)

        brf = Button(f3_tf, text="R", font=("MingLiU-ExtB 11 bold"), bg="white",command=self.show_recent)
        brf.pack(side=LEFT)

        b3 = Button(f3_tf, text="Q",font=("MingLiU-ExtB 11 bold"), bg="white", command=self.search_by_title)
        b3.pack(side=RIGHT)

        #  search_entry var
        self.search_entry_var=StringVar()

        self.search_entry = Entry(f3_tf,textvariable=self.search_entry_var, width=20, font=("MingLiU-ExtB 12 bold"))
        self.search_entry.pack(side=RIGHT)

        binimage = Image.open("bin.jpg")
        binimage = Resize_Image(binimage, (15, 25))
        binphoto = ImageTk.PhotoImage(binimage)
        label = Label(image=binphoto)
        label.image = binphoto

        b4 = Button(f3_tf, font=("MingLiU-ExtB 11 bold"), image=binphoto,height=25,width=15,bg='white', command=self.delete)
        b4.pack(side=RIGHT,padx=15)

        ####  recent table   ######
        table_frame=Frame(f3,bd=3,bg="white")
        table_frame.place(x=0,y=42,width=1346,height=440)

        scroll_y=Scrollbar(table_frame,orient=VERTICAL)
        self.view_recent=ttk.Treeview(table_frame,columns=("Date","Title","Notes"),yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_y.config(command=self.view_recent.yview)

        self.view_recent.heading("Date",text="Date")
        self.view_recent.heading("Title", text="Title")
        self.view_recent.heading("Notes", text="Description")

        self.view_recent.column("Date",width=100)
        self.view_recent.column("Title", width=300)
        self.view_recent.column("Notes", width=600)

        self.view_recent['show']='headings'
        self.view_recent.pack(fill=BOTH,expand=1)

        self.view_recent.bind("<Double-Button-1>", self.OnDoubleClick)


        #####  bg picture for f2
        image = Image.open("weed.jpg")
        photo = ImageTk.PhotoImage(image)

        canvas1 = Canvas(f2, width=1355, height=367)
        canvas1.pack(fill="both", expand=True)

        canvas1.create_image(0, 0, image=photo, anchor=NW)
        canvas1.photo=photo
        canvas1.create_rectangle(520,160,810,220, outline="white", width=4)
        canvas1.create_text(660, 190, text="Hi Subhashi!",font=("MingLiU-ExtB 20 bold"),fill="white")
        binimage = Image.open("bin.jpg")
        binphoto = ImageTk.PhotoImage(binimage)
        #img_label = Label(image=binphoto)

        scribble_notes_bt = Button(canvas1, font=("MingLiU-ExtB 13 bold"), text='Doodle',bg='white', command=self.scribble)
        scribble_notes_bt.place(x=1249,y=250)



        ##########################     newwin      #####################
        ##########################     Add Notes      #####################

        #add notes function
        def addnotes():

            class newnotewin:
                def __init__(self,newwin):
                    self.newwin=newwin
                    self.newwin.title("Notes")
                    self.newwin.geometry("957x927+480+20")


                    image = Image.open("add_notes.jpg")
                    photo = ImageTk.PhotoImage(image)

                    canvas2 = Canvas(self.newwin, width=957, height=927)
                    canvas2.pack()

                    canvas2.create_image(0, 0, image=photo, anchor=NW)
                    canvas2.photo = photo

                    nw_bt1 = Button(newwin, text="save", font=("MingLiU-ExtB 13 bold"),bg='#CD8B5B', command=self.save)
                    nw_bt1.place(x=30, y=30)

                    nw_bt2 = Button(newwin, text="cancel", font=("MingLiU-ExtB 13 bold"),bg='#CD8B5B', command=self.cancel)
                    nw_bt2.place(y=30, x=840)


                    self.date_txt = Text(newwin, height=1, width=10, font=("MingLiU-ExtB 15 bold"),highlightbackground="black",highlightthickness=2)
                    self.date_txt.place(x=380, y=30)

                    self.title_txt = Text(newwin, height=2, width=61, font=("MingLiU-ExtB 15 bold"))
                    self.title_txt.place(x=50, y=80)

                    self.note_txt = Text(newwin, height=32, width=71, font=("MingLiU-ExtB 13 bold"))
                    self.note_txt.place(x=52, y=150)

                    self.date_txt.insert('1.0', f"{dt.datetime.now():%d-%m-%Y}")


                #notesdb
                #keepnotes

                ######### save function

                def save(self):
                    con=pymysql.connect(host="localhost",user="root",passwd="",database="notesdb")
                    mycursor=con.cursor()
                    mycursor.execute("insert into keepnotes values(%s,%s,%s)",(f"{dt.datetime.now():%d-%m-%Y}",
                                                                               self.title_txt.get('1.0',END),
                                                                               self.note_txt.get('1.0',END)
                                                                               ))

                    con.commit()
                    con.close()

                def cancel(self):
                    self.title_txt.delete('1.0', END)
                    self.note_txt.delete('1.0', END)




            newwin=Toplevel()
            newwin_ob=newnotewin(newwin)
            newwin.mainloop()


        ######## back to root  #########

        # button to add notes in f2
        add_bt = Button(canvas1, text="Add notes", font=("MingLiU-ExtB 13 bold"), bg="white",command=addnotes)
        add_bt.place(x=1213,y=300)


        ##########  show function  #########

        self.show_recent()

        ######### digital clock & date in f2  ##########
        def time():
            string = strftime('%H:%M:%S')
            timelbl.config(text=string,fg="white")
            timelbl.after(1000, time)

        timelbl=Label(canvas1,font=("MingLiU-ExtB 18 bold"),bg="#52685B")
        timelbl.pack(anchor=NE, padx=40,pady=10)
        time()

        #date
        canvas1.create_text(1320, 49, anchor=NE, text=f"{dt.datetime.now():%a, %d %b %Y}",fill="white",
                                           font=("MingLiU-ExtB 12 bold"))
        #ends here

        ########## picture frame ############

        def photo_frame():
            pic_list = ['p9.jpg', 'p10.jpg','p11.jpg', 'p12.jpg','p5.jpg', 'p13.jpg', 'p7.jpg', 'p8.jpg', 'p2.jpg', 'p3.jpg', 'p4.jpg','p6.jpg']
            pic = random.choice(pic_list)
            pimage = Image.open(pic)
            pphoto = ImageTk.PhotoImage(pimage)

            canvasp.create_image(0, 0, image=pphoto, anchor=NW)
            canvasp.photo = pphoto

            canvasp.after(2000, photo_frame)



        photo_frame()

        def sort():
            rows = [(self.view_recent.set(item, 'Date'), item) for item in self.view_recent.get_children('')]
            rows.sort(key=lambda date: dt.datetime.strptime(date[0], "%d-%m-%Y"),reverse=True)

            '''col=[]
            for i in rows:
                col.append(i[0])
            print(rows)
            print(col)
            col.sort(key=lambda date: dt.datetime.strptime(date, "%d-%m-%Y"))'''

            for index, (values, item) in enumerate(rows):
                self.view_recent.move(item, '', index)

            self.view_recent.after(100,sort)

        sort()


    def scribble(self):
        class ImageGenerator:
            def __init__(self, root):
                self.root = root
                self.b1 = "up"
                self.xold = None
                self.yold = None

                fr1 = Frame(root, width=957, height=80)
                fr1.grid(row=0, column=0, )

                frame = Frame(self.root)
                frame.grid(row=1, column=0, pady=10, sticky=(N, W, E, S))

                v = ttk.Scrollbar(frame, orient=VERTICAL)

                self.drawing_area = Canvas(frame, height=820, width=932, bg='white', scrollregion=(0, 0, 932, 1200),
                                           yscrollcommand=v.set)
                self.drawing_area.grid(column=0, row=0, sticky=(N, W, E, S))

                v.grid(column=1, row=0, sticky=(N, S))
                v['command'] = self.drawing_area.yview

                self.drawing_area.bind("<Motion>", self.motion)
                self.drawing_area.bind("<ButtonPress-1>", self.b1down)
                self.drawing_area.bind("<ButtonRelease-1>", self.b1up)

                self.button = Button(fr1, text="Save", width=10, height=2, bg='white', command=self.save)
                self.button.place(x=40, y=15)
                self.button1 = Button(fr1, text="Clear", width=10, height=2, bg='white', command=self.clear)
                self.button1.place(x=810, y=15)

                self.doodle_name = StringVar()
                self.doodle_name_ent = Entry(fr1, width=35, textvariable=self.doodle_name).place(x=350, y=5, height=25)
                self.doodle_name.set('Untitled')

                self.blackbt = Button(fr1, width=2, height=1, bg='black', relief=SUNKEN,
                                      command=lambda: self.setcolor('black'))
                self.blackbt.place(x=360, y=40)
                self.redbt = Button(fr1, width=2, height=1, bg='red', relief=SUNKEN,
                                    command=lambda: self.setcolor('red'))
                self.redbt.place(x=400, y=40)
                self.bluebt = Button(fr1, width=2, height=1, bg='blue', relief=SUNKEN,
                                     command=lambda: self.setcolor('blue'))
                self.bluebt.place(x=440, y=40)
                self.pinkbt = Button(fr1, width=2, height=1, bg='pink', relief=SUNKEN,
                                     command=lambda: self.setcolor('pink'))
                self.pinkbt.place(x=480, y=40)
                self.yellowbt = Button(fr1, width=2, height=1, bg='yellow', relief=SUNKEN,
                                       command=lambda: self.setcolor('yellow'))
                self.yellowbt.place(x=520, y=40)
                self.greenbt = Button(fr1, width=2, height=1, bg='green', relief=SUNKEN,
                                      command=lambda: self.setcolor('green'))
                self.greenbt.place(x=560, y=40)
                self.purplebt = Button(fr1, width=2, height=1, bg='purple', relief=SUNKEN,
                                       command=lambda: self.setcolor('purple'))
                self.purplebt.place(x=600, y=40)
                self.whitebt = Button(fr1, width=5, height=2, bg='white', relief=SUNKEN,
                                      command=lambda: self.setcolor('white'))
                self.whitebt.place(x=660, y=23)



                self.setcolor('black')

                self.image = Image.new("RGB", (932, 1200), (255, 255, 255))
                self.draw = ImageDraw.Draw(self.image)

            def save(self):
                filename = self.doodle_name.get()+'.jpg'
                self.image.save(f'C:/Users/hp/PycharmProjects/finalcodenotesapp/doodle/{filename}','JPEG')

            def clear(self):
                self.drawing_area.delete("all")
                self.image = Image.new("RGB", (1200, 1200), (255, 255, 255))
                self.draw = ImageDraw.Draw(self.image)


            def setcolor(self, newcolor):

                global color
                color = newcolor
                self.stroke_thickness = 3
                if color == 'black':
                    self.r = 0
                    self.g = 0
                    self.b = 0
                elif color == 'red':
                    self.r = 255
                    self.g = 0
                    self.b = 0
                elif color == 'blue':
                    self.r = 0
                    self.g = 0
                    self.b = 255
                elif color == 'pink':
                    self.r = 237
                    self.g = 131
                    self.b = 177
                elif color == 'yellow':
                    self.r = 253
                    self.g = 255
                    self.b = 22
                elif color == 'green':
                    self.r = 0
                    self.g = 146
                    self.b = 0
                elif color == 'purple':
                    self.r = 195
                    self.g = 65
                    self.b = 199
                elif color == 'white':
                    self.stroke_thickness = 10
                    self.r = 255
                    self.g = 255
                    self.b = 255

            def b1down(self, event):
                self.b1 = "down"

            def b1up(self, event):
                self.b1 = "up"
                self.xold = None
                self.yold = None

            def motion(self, event):
                if self.b1 == "down":
                    if self.xold is not None and self.yold is not None:
                        event.widget.create_line(self.xold, self.yold, event.x, event.y, smooth='true',
                                                 width=self.stroke_thickness, fill=color)
                        self.draw.line(((self.xold, self.yold), (event.x, event.y)), (self.r, self.g, self.b),
                                       width=self.stroke_thickness)

                self.xold = event.x
                self.yold = event.y


        root = Toplevel()
        root.geometry("%dx%d+%d+%d" % (957, 927, 480, 20))
        root.config(bg='white')
        ImageGenerator(root)
        root.mainloop()



    def show_recent(self):  #completed


        con = pymysql.connect(host="localhost", user="root", passwd="", database="notesdb")
        mycursor = con.cursor()
        mycursor.execute("select * from keepnotes")

        rows = mycursor.fetchall()
        if len(rows) != 0:
            self.view_recent.delete(*self.view_recent.get_children())
            for row in rows:
                self.view_recent.insert('',END,values=row)
                con.commit()

        con.close()

        path = "C:/Users/hp/PycharmProjects/finalcodenotesapp/doodle"
        list_img = []
        for d in os.listdir(path):
            file = d
            p = path+'/'+d
            filedate = dt.datetime.fromtimestamp(os.stat(p).st_mtime).strftime('%d-%m-%Y')
            descript = "Doodle Note"
            tup = (filedate,file[:-4],descript)
            list_img.append(tup)


        for row in list_img:
            self.view_recent.insert('', END, values=row)



    def search_by_title(self):

        title_searched = self.search_entry_var.get()
        search=[]
        matches=[]
        fuzzy_sort=[]

        con = pymysql.connect(host="localhost", user="root", passwd="", database="notesdb")
        mycursor = con.cursor()
        mycursor.execute("SELECT Title FROM keepnotes")
        searchtup = mycursor.fetchall()
        for s in searchtup:
            search.append(s[0])

        con.commit()
        con.close()

        fuzzy_sort = process.extract(title_searched, search)
        for i in fuzzy_sort:
            matches.append(i[0])


        else:

            rows=[]
            con = pymysql.connect(host="localhost", user="root", passwd="", database="notesdb")
            mycursor = con.cursor()
            for i in matches:
                mycursor.execute("select * from keepnotes where Title=%s",(i))
                rows.append(mycursor.fetchone())

            if len(rows) != 0:
                self.view_recent.delete(*self.view_recent.get_children())
                for row in rows:
                    self.view_recent.insert('', END, values=row)
                    con.commit()

            con.close()





    def delete(self):  #completed

        selected_items = self.view_recent.selection()
        rows_to_del = []
        doodle_to_del = []

        for row in selected_items:
            if self.view_recent.item(row,'values')[2] != 'Doodle Note':
                rows_to_del.append(self.view_recent.item(row,'values')[1])
            else:
                doodle_to_del.append(self.view_recent.item(row,'values')[1])

        rows_to_del_str = ','.join(rows_to_del)

        for row in selected_items:
            self.view_recent.delete(row)

        for note in doodle_to_del:
            filename = note + '.jpg'
            os.remove(f'C:/Users/hp/PycharmProjects/finalcodenotesapp/doodle/{filename}')

        con = pymysql.connect(host="localhost", user="root", passwd="", database="notesdb")
        mycursor = con.cursor()
        mycursor.execute("DELETE from keepnotes where Title in ('"+rows_to_del_str+"')")

        con.commit()
        con.close()

        rows_to_del = []

    def add_reminder(self):

        class rmwinclass:
            def __init__(self, rmwin, rm_lb):
                self.rmwin = rmwin
                self.rmwin.geometry("380x280+950+290")
                self.rmwin.title("Reminder")
                self.rmwin.configure(background="white")
                self.rmwin.resizable(width=False, height=False)

                self.rm_lb = rm_lb
                rem_lable = Label(self.rmwin, text=self.rm_lb)
                rem_lable.place(x=25, y=10, height=30, width=330)

                choose_date = Label(self.rmwin, text="Date")
                choose_date.place(x=55, y=60, height=30, width=55)

                choose_time = Label(self.rmwin, text="Time")
                choose_time.place(x=55, y=100, height=30, width=55)

                self.day = StringVar()
                self.day_ent = Entry(self.rmwin, width=5, textvariable=self.day,highlightbackground='black',highlightthickness=2).place(x=170, y=65)


                self.month = StringVar()
                self.month_ent = Entry(self.rmwin, width=5, textvariable=self.month,highlightbackground='black',highlightthickness=2).place(x=220, y=65)



                self.year = StringVar()
                self.year_ent = Entry(self.rmwin, width=5, textvariable=self.year,highlightbackground='black',highlightthickness=2).place(x=270, y=65)

                self.hour = StringVar()
                self.hour_sp = Spinbox(self.rmwin, width=8, from_=0, to=23, textvariable=self.hour, format="%02.0f",highlightbackground='black',highlightthickness=2).place(x=170,
                                                                                                             y=105)

                self.minutes = StringVar()
                self.minutes_sp = Spinbox(self.rmwin, width=8, from_=0, to=59, textvariable=self.minutes, format="%02.0f",highlightbackground='black',highlightthickness=2).place(
                    x=240, y=105)

                confirm = Button(self.rmwin, text="Set Reminder", width=12, command=self.alarm_time)
                confirm.place(x=140, y=170)

                exit = Button(self.rmwin, text="Quit", width=10, command=self.rmwin.destroy)
                exit.place(x=150, y=220)

            def alarm_time(self):

                '''s=f"{dt.date.today():%d %m %Y}"
                print("hi",s)
                l=['15-05-2021','14-11-2021','01-03-2021']
                l.sort(key=lambda date: dt.datetime.strptime(date, "%d-%m-%Y"))
                print(l)'''
                D = self.day.get()
                M = self.month.get()
                Y = self.year.get()
                h = self.hour.get()
                m = self.minutes.get()


                set_alarm = f"{h}:{m}:00"
                set_date = f"{D}-{M}-{Y}"

                con = pymysql.connect(host="localhost", user="root", passwd="", database="notesdb")
                mycursor = con.cursor()
                mycursor.execute("insert into reminder_table values(%s,%s,%s)", (self.rm_lb,
                                                                                 set_date,
                                                                                 set_alarm
                                                                                 ))

                con.commit()
                con.close()




        rmwin = Toplevel()
        rm_lb = self.reminder_entry_var.get()
        self.reminder_entry_var.delete(0,END)
        rmwin_ob = rmwinclass(rmwin,rm_lb)
        #rmwin.mainloop()

    def rem_listbox_win(self):

        def delete_Task():

            selected_items = self.view_rem.selection()
            rows_to_del = []

            for row in selected_items:
                rows_to_del.append(self.view_rem.item(row, 'values')[0])

            rows_to_del_str = ','.join(rows_to_del)

            for row in selected_items:
                self.view_rem.delete(row)

            con = pymysql.connect(host="localhost", user="root", passwd="", database="notesdb")
            mycursor = con.cursor()
            mycursor.execute("DELETE from reminder_table where Event in ('" + rows_to_del_str + "')")

            con.commit()
            con.close()

            rows_to_del = []


        self.rem = Toplevel()
        self.rem.title("Reminders")
        self.rem.geometry("390x300+70+177")
        self.rem.resizable(width=False, height=False)

        lb_fr=Frame(self.rem)
        lb_fr.place(x=0,y=0,width=390,height=240)


        scroll = Scrollbar(lb_fr, orient=VERTICAL)
        self.view_rem = ttk.Treeview(lb_fr, columns=("L", "D", "T"), yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)
        scroll.config(command=self.view_rem.yview)

        self.view_rem.heading("L", text="Label")
        self.view_rem.heading("D", text="Date")
        self.view_rem.heading("T", text="Time")

        self.view_rem.column("L", width=100)
        self.view_rem.column("D", width=50)
        self.view_rem.column("T", width=60)

        self.view_rem['show'] = 'headings'
        self.view_rem.pack(fill=BOTH, expand=1)

        con = pymysql.connect(host="localhost", user="root", passwd="", database="notesdb")
        mycursor = con.cursor()
        mycursor.execute("select * from reminder_table")

        rows = mycursor.fetchall()


        if len(rows) != 0:
            self.view_rem.delete(*self.view_rem.get_children())
            for row in rows:
                self.view_rem.insert('',END,values=row)
                con.commit()

        con.close()


        del_bt = Button(self.rem, text='Delete', font=('Times, 10'), command=delete_Task)
        del_bt.place(x=143, y=250)


    def get_task(self):
        task = self.to_do_entry_var.get()

        sql = """INSERT INTO `to-do_table` VALUES (%s)"""

        con = pymysql.connect(host="localhost", user="root", passwd="", database="notesdb")
        mycursor = con.cursor()
        mycursor.execute(sql,(task,))

        con.commit()
        con.close()

        self.to_do_entry_var.delete(0,END)


    def list_box_win(self):

        def delete_Task():

            sel_items = lb.curselection()

            for i in lb.curselection():

                del_task=lb.get(i)
                l=','.join(del_task)
                con = pymysql.connect(host="localhost", user="root", passwd="", database="notesdb")
                mycursor = con.cursor()
                mycursor.execute("DELETE from `to-do_table` where Task in ('" + l + "')")

                con.commit()
                con.close()

            for item in sel_items[::-1]:
                lb.delete(item)



        self.todo = Toplevel()
        self.todo.title("To-do")
        self.todo.geometry("390x450+70+309")
        self.todo.resizable(width=False, height=False)

        lb_fr=Frame(self.todo)
        lb_fr.place(x=0,y=0,width=390,height=370)

        lb = Listbox(lb_fr, width=33, height=15, font=('Times', 14), bd=0, selectmode=MULTIPLE)
        lb.pack(side=LEFT, fill=BOTH)

        scroll=Scrollbar(lb_fr)
        scroll.pack(side=RIGHT, fill=BOTH)

        lb.config(yscrollcommand=scroll.set)
        scroll.config(command=lb.yview)

        con = pymysql.connect(host="localhost", user="root", passwd="", database="notesdb")
        mycursor = con.cursor()
        mycursor.execute("select * from `to-do_table`")

        Tasks = []

        rows = mycursor.fetchall()
        for row in rows:
            Tasks.append(row)

        con.commit()
        con.close()

        for task in Tasks:
            lb.insert(END,task)

        del_bt = Button(self.todo, text='Delete', font=('Times, 10'), command=delete_Task)
        del_bt.place(x=150, y=395)


    ####  opening existing note  #######
    def OnDoubleClick(self, event):

        class doodle_win:
            def __init__(self, root, title_selected):
                self.root = root
                root.geometry("%dx%d+%d+%d" % (957, 927, 480, 20))
                root.config(bg='white')
                self.b1 = "up"
                self.xold = None
                self.yold = None

                fr1 = Frame(root, width=957, height=80)
                fr1.grid(row=0, column=0, )

                frame = Frame(self.root)
                frame.grid(row=1, column=0, pady=10, sticky=(N, W, E, S))

                v = ttk.Scrollbar(frame, orient=VERTICAL)

                self.drawing_area = Canvas(frame, height=820, width=932, bg='white', scrollregion=(0, 0, 932, 1200),
                                           yscrollcommand=v.set)
                self.drawing_area.grid(column=0, row=0, sticky=(N, W, E, S))

                v.grid(column=1, row=0, sticky=(N, S))
                v['command'] = self.drawing_area.yview


                filename = title_selected + '.jpg'
                self.filepath = f'C:/Users/hp/PycharmProjects/finalcodenotesapp/doodle/{filename}'

                doodleimage = Image.open(self.filepath)
                doodlephoto = ImageTk.PhotoImage(doodleimage)

                self.drawing_area.create_image(0, 0, image=doodlephoto, anchor=NW)
                self.drawing_area.photo = doodlephoto


                self.drawing_area.bind("<Motion>", self.motion)
                self.drawing_area.bind("<ButtonPress-1>", self.b1down)
                self.drawing_area.bind("<ButtonRelease-1>", self.b1up)

                self.button = Button(fr1, text="Save", width=10, height=2, bg='white', command=self.save)
                self.button.place(x=40, y=15)
                self.button1 = Button(fr1, text="Clear", width=10, height=2, bg='white', command=self.clear)
                self.button1.place(x=810, y=15)

                self.doodle_name = StringVar()
                self.doodle_name_ent = Entry(fr1, width=35, textvariable=self.doodle_name).place(x=350, y=5, height=25)
                self.doodle_name.set(title_selected)

                self.blackbt = Button(fr1, width=2, height=1, bg='black', relief=SUNKEN,
                                      command=lambda: self.setcolor('black'))
                self.blackbt.place(x=360, y=40)
                self.redbt = Button(fr1, width=2, height=1, bg='red', relief=SUNKEN,
                                    command=lambda: self.setcolor('red'))
                self.redbt.place(x=400, y=40)
                self.bluebt = Button(fr1, width=2, height=1, bg='blue', relief=SUNKEN,
                                     command=lambda: self.setcolor('blue'))
                self.bluebt.place(x=440, y=40)
                self.pinkbt = Button(fr1, width=2, height=1, bg='pink', relief=SUNKEN,
                                     command=lambda: self.setcolor('pink'))
                self.pinkbt.place(x=480, y=40)
                self.yellowbt = Button(fr1, width=2, height=1, bg='yellow', relief=SUNKEN,
                                       command=lambda: self.setcolor('yellow'))
                self.yellowbt.place(x=520, y=40)
                self.greenbt = Button(fr1, width=2, height=1, bg='green', relief=SUNKEN,
                                      command=lambda: self.setcolor('green'))
                self.greenbt.place(x=560, y=40)
                self.purplebt = Button(fr1, width=2, height=1, bg='purple', relief=SUNKEN,
                                       command=lambda: self.setcolor('purple'))
                self.purplebt.place(x=600, y=40)
                self.whitebt = Button(fr1, width=5, height=2, bg='white', relief=SUNKEN,
                                      command=lambda: self.setcolor('white'))
                self.whitebt.place(x=660, y=23)



                self.setcolor('black')

                self.image = Image.open(self.filepath)
                self.draw = ImageDraw.Draw(self.image)

            def save(self):
                filename = self.doodle_name.get()+'.jpg'
                self.image.save(f'C:/Users/hp/PycharmProjects/finalcodenotesapp/doodle/{filename}','JPEG')

            def clear(self):
                self.drawing_area.delete("all")

                doodleimage = Image.open(self.filepath)
                doodlephoto = ImageTk.PhotoImage(doodleimage)
                self.drawing_area.create_image(0, 0, image=doodlephoto, anchor=NW)
                self.drawing_area.photo = doodlephoto

                self.image = Image.open(self.filepath)
                self.draw = ImageDraw.Draw(self.image)


            def setcolor(self, newcolor):

                global color
                color = newcolor
                self.stroke_thickness = 3
                if color == 'black':
                    self.r = 0
                    self.g = 0
                    self.b = 0
                elif color == 'red':
                    self.r = 255
                    self.g = 0
                    self.b = 0
                elif color == 'blue':
                    self.r = 0
                    self.g = 0
                    self.b = 255
                elif color == 'pink':
                    self.r = 237
                    self.g = 131
                    self.b = 177
                elif color == 'yellow':
                    self.r = 253
                    self.g = 255
                    self.b = 22
                elif color == 'green':
                    self.r = 0
                    self.g = 146
                    self.b = 0
                elif color == 'purple':
                    self.r = 195
                    self.g = 65
                    self.b = 199
                elif color == 'white':
                    self.stroke_thickness = 10
                    self.r = 255
                    self.g = 255
                    self.b = 255

            def b1down(self, event):
                self.b1 = "down"

            def b1up(self, event):
                self.b1 = "up"
                self.xold = None
                self.yold = None

            def motion(self, event):
                if self.b1 == "down":
                    if self.xold is not None and self.yold is not None:
                        event.widget.create_line(self.xold, self.yold, event.x, event.y, smooth='true',
                                                 width=self.stroke_thickness, fill=color)
                        self.draw.line(((self.xold, self.yold), (event.x, event.y)), (self.r, self.g, self.b),
                                       width=self.stroke_thickness)

                self.xold = event.x
                self.yold = event.y


        class newnotewin:

            def __init__(self, newwin, title_selected):
                self.newwin = newwin
                self.newwin.title("Notes")
                self.newwin.geometry("957x927+480+20")

                image = Image.open("add_notes.jpg")
                photo = ImageTk.PhotoImage(image)

                canvas2 = Canvas(self.newwin, width=957, height=927)
                canvas2.pack()

                canvas2.create_image(0, 0, image=photo, anchor=NW)
                canvas2.photo = photo

                nw_bt1 = Button(newwin, text="save", font=("MingLiU-ExtB 13 bold"),bg='#CD8B5B', command=self.save)
                nw_bt1.place(x=30, y=30)

                nw_bt2 = Button(newwin, text="cancel", font=("MingLiU-ExtB 13 bold"),bg='#CD8B5B', command=self.cancel)
                nw_bt2.place(y=30, x=840)

                self.date_txt = Text(newwin, height=1, width=10, font=("MingLiU-ExtB 15 bold"),highlightbackground="black",highlightthickness=2)
                self.date_txt.place(x=380, y=30)

                self.title_txt = Text(newwin, height=2, width=61, font=("MingLiU-ExtB 15 bold"))
                self.title_txt.place(x=50, y=80)

                self.note_txt = Text(newwin, height=32, width=71, font=("MingLiU-ExtB 13 bold"))
                self.note_txt.place(x=52, y=150)

                self.title_selected = title_selected


                ## show whats in the note ##

                con = pymysql.connect(host="localhost", user="root", passwd="", database="notesdb")
                mycursor = con.cursor()

                mycursor.execute("select Date from keepnotes where Title=%s",(self.title_selected,))
                self.dateofnote = mycursor.fetchone()

                mycursor.execute("select Title from keepnotes where Title=%s", (self.title_selected,))
                self.titleofnote = mycursor.fetchone()

                mycursor.execute("select Notes from keepnotes where Title=%s", (self.title_selected,))
                self.noteofnote = mycursor.fetchone()

                self.date_txt.insert(END, self.dateofnote)
                self.title_txt.insert(END,"".join(self.titleofnote))
                self.note_txt.insert(END,"".join(self.noteofnote))






            # notesdb
            # keepnotes

            ######### save function

            def save(self):

                con = pymysql.connect(host="localhost", user="root", passwd="", database="notesdb")
                mycursor = con.cursor()
                mycursor.execute("UPDATE keepnotes SET Date=%s, Title=%s, Notes=%s where Title=%s", (f"{dt.datetime.now():%d-%m-%Y}",
                                                                            self.title_txt.get('1.0', END),
                                                                            self.note_txt.get('1.0', END),
                                                                            self.title_selected
                                                                            ))

                con.commit()
                con.close()

            def cancel(self):
                self.date_txt.delete('1.0', END)
                self.title_txt.delete('1.0', END)
                self.note_txt.delete('1.0', END)

                con = pymysql.connect(host="localhost", user="root", passwd="", database="notesdb")
                mycursor = con.cursor()

                mycursor.execute("select Date from keepnotes where Title=%s", (self.title_selected,))
                self.dateofnote = mycursor.fetchone()

                mycursor.execute("select Title from keepnotes where Title=%s", (self.title_selected,))
                self.titleofnote = mycursor.fetchone()

                mycursor.execute("select Notes from keepnotes where Title=%s", (self.title_selected,))
                self.noteofnote = mycursor.fetchone()

                self.date_txt.insert(END, self.dateofnote)
                self.title_txt.insert(END, "".join(self.titleofnote))
                self.note_txt.insert(END, "".join(self.noteofnote))









        newwin = Toplevel()

        # passing title_selected to newwin
        curItem = self.view_recent.item(self.view_recent.focus())
        des_selected = curItem['values'][2]
        if des_selected != 'Doodle Note':
            title_selected = curItem['values'][1]
            newwin_ob = newnotewin(newwin, title_selected)
        else:
            title_selected = curItem['values'][1]
            newwin_ob = doodle_win(newwin,title_selected)
        newwin.mainloop()


def correctpass():
    pwd = password.get()
    passwd = 'pass'

    if passwd == pwd:
        root.destroy()
        mainwin=Tk()
        ob=Notes(mainwin)
        root.mainloop()
    else:
        passEntry.delete(0,END)
        messagebox.showerror("Error", "Incorrect Password")


if __name__ == '__main__':

    root=Tk()
    root.title("Notes")
    root.geometry("800x700+580+95")
    root.resizable(height=False, width=False)

    cimage = Image.open("bg1.jpg")
    cphoto = ImageTk.PhotoImage(cimage)
    canvasc = Canvas(root, width=800, height=700)
    canvasc.pack(fill="both", expand=True)
    canvasc.create_image(0, 0, image=cphoto, anchor=NW)
    canvasc.photo = cphoto

    frame = Frame(root)
    frame.place(x=150, y=70, width=500, height=540)

    title = Label(frame,text="NOTES", font=("MingLiU-ExtB 20 bold"))
    title.place(x=200,y=20)

    title = Label(frame, text="Enter password", font=("MingLiU-ExtB 10 bold"))
    title.place(x=50,y=200)

    password = StringVar()  # Password variable
    passEntry = Entry(frame, textvariable=password, show='*')
    passEntry.place(x=50,y=230,width=400,height=50)



    def switchState():
        if checkvar.get() == 1:
            passEntry.config(show="")

        elif checkvar.get() == 0:
            passEntry.config(show='*')


    checkvar = IntVar()
    chechbutton = Checkbutton(frame, text="Show password",font=("MingLiU-ExtB 10 bold"), variable=checkvar,onvalue=1, offvalue=0,command=switchState)
    chechbutton.place(x=50,y=290)

    button = Button(frame, text="Next", font=("MingLiU-ExtB 11 bold"), bg="grey", command=correctpass)
    button.place(x=220,y=340,height=45, width=80)



    root.mainloop()

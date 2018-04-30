from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pickle
import os.path
import sys
import pymongo
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import os
import shutil
import datetime
from tkinter import messagebox
from myDatabasefile import *
from myDatabasefile import loginCheck
import MachineLearning as m
now=datetime.datetime.now()
import re


class Frame1(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg="grey")
        self.parent = parent



        self.tree = ttk.Treeview(self,selectmode='browse')
        self.tree.bind("<Double-1>", self.link_tree)
        self.username_label = Label(self, text="Username: ")  # USERNAME LABEL
        self.username_label.grid(row=1, column=1)

        self.username = ttk.Entry(self,width=15)  # USERNAME ENTRY BOX
        self.username.grid(column=2, row=1, sticky="nsew")

        self.password_label = Label(self, text="Password: ")  # USERNAME LABEL
        self.password_label.grid(row=2, column=1)
        self.password = Entry(self,show="*",width=15)  # USERNAME ENTRY BOX
        self.password.grid(column=2, row=2, sticky="nsew")
        self.SubmitB = Button(self, text="Submit", command=self.login)
        self.SubmitB.grid(row=3, column=2, padx=5, pady=5)
        self.search = ttk.Entry(self, width=15)
        createTable()

    def link_tree(self, event):
        input_id = self.tree.selection()
        self.input_item = self.tree.item(input_id, "text")
        print(self.input_item)
        # for opening the link in browser
        import webbrowser
        webbrowser.open('{}'.format(self.input_item))

    def login(self):
        usr=self.username.get()
        pwd=self.password.get()
        print(self.username.get(),self.password.get())
        if (usr != '' and pwd != ''):
                                    self.result = loginCheck(usr, pwd)

                                    if self.result == 'Pass':

                                                        self.widgets()

                                    else:
                                        messagebox.showerror("Error", "Invalid credentials, please try again")
        else:
            messagebox.showerror("Error", "Invalid credentials, please try again")








    def widgets(self):
    #    self.winfo_toplevel().title("Web Scraping and Natural Language Processing")
        self.username_label.grid_forget()
        self.username.grid_forget()
        self.password_label.grid_forget()
        self.password.grid_forget()
        self.SubmitB.grid_forget()

        self.btn1=Button(self,text="View Scraped Information", command=self.main_1).grid(row=1, column=0, padx=5, pady=5)
        self.btn2=Button(self,text="Scrape Info", command=self.main_3).grid(row=1, column=1, padx=5, pady=5)
        self.btn3 = Button(self, text="Clear Scraped Info", command=self.main_2).grid(row=1, column=2, padx=5, pady=5)
        self.btn3 = Button(self, text="Knwoledge Extraction",command=self.machine_learning).grid(row=1, column=3, padx=5, pady=5)


        self.search.grid(column=4, row=2, sticky="nsew")
        self.btn3 = Button(self, text="Search Questions", command=self.search_questions).grid(row=1, column=4, padx=5, pady=5)

        #self.tree.resizable(width=0, height=0)


        #tree.place(x=30, y=95)

        vsb = Scrollbar(self, orient="vertical", command=self.tree.yview)
        #vsb.place(x=30 + 200+400, y=35, height=200)
        vsb.grid(column=1,row=0,sticky="nsew")

        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(column=0,row=0,sticky="nsew",padx=5, pady=5)
       # self.tree["columns"] = ("one", "two","three")
        self.tree["columns"] = ("one", "two")
        self.tree.column("one")
        self.tree.column("two")
     #   self.tree.column("three")
        self.tree.heading("one", text="Question")
        self.tree.heading("two", text="Url")
       # self.tree.heading("three", text="Url")
        self.tree['show']=['headings']

        #from wordcloud import WordCloud

        #self.btn4 = Button(self, text="Word Cloud", command=self.main_4).grid(row=1, column=4, padx=5, pady=5)


    def machine_learning(self):
        print(m.ml_task())

    def main_1(self):

        cursor1=connectDB()
        i=0
        for document in cursor1:
            i+=1
            title_p = document["title"]
            # date_p=document["date"]
            date_p = str((document['date']))
            url_p=document['url']
            # self.tree.insert("", 1, "dir2", text="Dir 2")
            self.tree.insert("", 0, values=(title_p,url_p))

    def main_2(self):
        #clearDB()
        self.tree.delete(*self.tree.get_children())
        #text = messagebox.askyesnocancel("Delete", "Are You Sure to delete everything?", icon='warning')
        #if text == 'Yes':


         #   messagebox.showinfo("Success", "Deleted Records Succesfully!")
       # else:
        #    pass


    def main_3(self):
        result = runScrap()
        if result=='Crawling Completed':
            messagebox.showinfo("Success", "Scraping completed")

    def search_questions(self):
        print("In search called")
        srch=self.search.get()
        print()
        cursor1 = searchDB(srch)
        i = 0
        #print(cursor1)
        for document in cursor1:
            i += 1
            title_p = document["title"]
            #print(title_p)
            # date_p=document["date"]
            date_p = str((document['date']))
            url_p = document['url']
            # self.tree.insert("", 1, "dir2", text="Dir 2")
            self.tree.insert("", 0, values=(title_p, url_p))

        pass

class MainW(Tk):

    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.title="Web Scraping and Machine Learning Application"
        self.mainWidgets()


    def mainWidgets(self):
        self.label1 = Label(self, text="Project on Web Scraping in python", bg="red")
        self.label1.grid(row=0, column=0)

        self.window = Frame1(self)
        self.window.grid(row=0, column=10, rowspan=2)



def connectDB():
    from pymongo import MongoClient
    client = MongoClient()
    client = MongoClient('localhost', 27017)
    db = client.stackoverflow
    posts = db.questions
    cursor = posts.find({})
    cursor1=posts.find({}, {"_id": False, "date": True, "title": True, "url": True})
    #print(posts.find({}, {"_id": False, "date": True, "title": True, "url": True}))
    return cursor1

def searchDB(text):
 try:
    from pymongo import MongoClient
    #client = MongoClient()
    client = MongoClient('localhost', 27017)
    db = client.stackoverflow
    posts = db.questions

   # cursor2=db.users.find({"title": {'$regex': '.*' + text + '.*'},{"_id": 1}).limit(1)}})
  #  cursor2=db.collection.find({"title": {'$regex':'^'+text+'$', '$options' : 'i'}}, {"date": True, "title": True, "url": True})
    cursor2 = posts.find({'title':{'$regex':text}},{"_id": False, "date": True, "title": True, "url": True})
    #cursor2=db.users.find({"title":/text/})
    #print(cursor2)

    return cursor2
 except Exception as e:
     print(e)

def clearDB():
    from pymongo import MongoClient
    client = MongoClient()
    client = MongoClient('localhost', 27017)
    db = client.stackoverflow
    db.questions.remove({})




def runScrap():
    curfilePath = os.path.abspath(__file__)
    curDir = os.path.abspath(os.path.join(curfilePath, os.pardir))
    tmpDir = os.path.abspath(os.path.join(curDir, 'tmp/'))
    try:
        shutil.rmtree(tmpDir)
    except:
        pass
    s = get_project_settings()
    process = CrawlerProcess(s)
    process.crawl('stack_spider1')
    process.start()
    return 'Crawling Completed'



if __name__=="__main__":
    app = MainW(None)
    app.mainloop()
    print(now.strftime("%Y-%m-%d %H:%M"))
    print("Programmed by Pratik Tamhankar and Swati Khandalekar");
#root=buildFrame()
#root.mainloop()
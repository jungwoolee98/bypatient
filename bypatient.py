"""
ByPatient 
by Jungwoo Lee and Andy Lu

A smart tool to promote patient self-care. 
Patients do not always follow self-care efforts due to many reasons such as
forgetfulness, lack of understanding, loss of instructions, misinformation, and many other reasons.
Our product helps to solve this issue.
Due to the ubiquitous nature of cellphones, cellphones serve as the best way to solve these issues.
Their prevalence and amount of use (people use their cellphones several hours a day) make them
the perfect solution.
ByPatient allows the health-care provider to put in information into an interactive and 
self-explanatory GUI. It will then send a text message to the patient's phone number with
information such as instructions on taking medication, doctor notes, and quick explanation
of the drug. Compared to just verbal messages or notes written on paper, these text messages
will always be available to the patient.
"""

from twilio.rest import Client
from Tkinter import *
import time
import pandas as pd

# Your Account SID from twilio.com/console
account_sid = "AC5d70d3f0bc928bc33297d7684d78a004"
# Your Auth Token from twilio.com/console
auth_token  = "8c3fcc4f2cbaf15f4ac68d2826c887b0"

client = Client(account_sid, auth_token)

master = Tk()
master.configure(background = '#a1dbcd')
master.title("ByPatient")
master.wm_iconbitmap('Icon.ico')

Patient_INFO  = {}
drug1 = ""
drug2 = ""
Phone_number = ""
frequency = ""
dosage = ''
additional_comment = ''

df1 = pd.read_csv('druginteraction.csv')
drugInteraction = df1.set_index("drugs")
df2 = pd.read_csv('druginfo.csv')
drugInfo = df2.set_index("drugs")

Label(master, text = 'ByPatient', bg = "#a1dbcd")
Label(master,text = 'Phone Number', bg = "#a1dbcd").grid(row= 0)
Label(master,text = 'Drug1', bg = "#a1dbcd").grid(row = 1)
Label(master,text = 'Times/day', bg = "#a1dbcd").grid(row = 2)
Label(master,text = 'Dosage', bg = "#a1dbcd").grid(row = 3)
Label(master,text = 'Drug2', bg = "#a1dbcd").grid(row = 4)
Label(master,text = 'Times/Day', bg = "#a1dbcd").grid(row = 5)
Label(master,text = 'Dosage', bg = "#a1dbcd").grid(row=6)
Label(master,text = 'Additional Comment', bg ="#a1dbcd" ).grid(row = 7)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e4 = Entry(master)
e5 = Entry(master)
e6 = Entry(master)
e7 = Entry(master)
e8 = Entry(master)

e1.grid(row = 0, column = 1)
e2.grid(row = 1, column = 1)
e3.grid(row = 2, column = 1)
e4.grid(row = 3, column = 1)
e5.grid(row = 4, column = 1)
e6.grid(row = 5, column = 1)
e7.grid(row = 6, column = 1)
e8.grid(row = 7, column = 1)

def Enter():
    global drug1, drug2, frequency, Phone_number,dosage, sec
    Phone_number = e1.get()
    drug1 = e2.get()
    frequency1 = e3.get()
    dosage1 = e4.get()
    drug2 = e5.get()
    frequency2 = e6.get()
    dosage2 = e7.get()
    additional_comment = e8.get()
    Patient_INFO[Phone_number] = [drug1, frequency1, dosage1, drug2, frequency2, dosage2, additional_comment]

    if drug1 != "" and drug2 != "":
        message = client.messages.create(
            to="+1" + Phone_number,
            from_= "+15755025023",
            body="You have been prescribed " + drug1 + " and " + drug2 + ". Please take " + drug1 + " " +dosage1 + " pills " + frequency1 +" times/day." \
                  + " Please take " + drug2 + " " + dosage2 + " pills" + frequency2 + " times/day." + " The possible adverse side effects from" \
                  + " taking these two drugs together is: " + drugInteraction.loc[drug1, drug2] + " " + additional_comment
            )
        time.sleep(5)
        message = client.messages.create(
            to="+1" + Phone_number,
            from_= "+15755025023",
            body = "" + drug1 + " is " + drugInfo.loc[drug1, 'info'] + " Please make sure to take your prescribed medication properly. Failure to do so may result in" \
                    + " worsening of symptoms and hospitalization. "
            )
        time.sleep(5)
        message = client.messages.create(
        to="+1" + Phone_number,
        from_= "+15755025023",
        body = "" + drug2 + " is " + drugInfo.loc[drug2,'info'] + " Please make sure to take your prescribed medication properly. Failure to do so may result in" \
               + " worsening of symptoms and hospitalization. ")

    if drug2 == "":
        message = client.messages.create(
            to="+1" + Phone_number,
            from_= "+15755025023",
            body= "You have been prescribed " + drug1 + ". Please take " + dosage1 + " pills" + frequency1 + " times/day. " \
              + additional_comment)
        time.sleep(5)
        message = client.messages.create(
            to="+1" + Phone_number,
            from_= "+15755025023",
            body = drug1 + " is " + drugInfo.loc[drug1, 'info'] + " Please make sure to take your prescribed medication properly." \
                   + " Failure to do so may result in worsening of symptoms and hospitalization."
                   )

def Clear():
    e1.delete(0,END)
    e2.delete(0,END)
    e3.delete(0,END)
    e4.delete(0,END)
    e5.delete(0,END)
    e6.delete(0,END)
    e7.delete(0,END)
    e8.delete(0,END)

def druginteraction():
    toplevel = Toplevel()
    drug1 = e2.get()
    drug2 = e5.get()
    label1 = Label(toplevel, text= drugInteraction.loc[drug1, drug2], height=10, width=65)
    label1.pack()

button1 = Button(master, text= 'Enter', command= Enter, bg = "red" )
button1.grid(row=8, column=0, sticky=W, pady = 4)
button2 = Button(master, text= 'Clear', command= Clear, bg = "#a1dbcd" )
button2.grid(row=8, column =1, sticky=W, pady = 4)
button3 = Button(master, text= 'Check Potential Drug Interaction', command = druginteraction,bg = "#a1dbcd")
button3.grid(row=8,column= 2,sticky=W, pady = 4)


mainloop()
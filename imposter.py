import tkinter
import tkinter.messagebox

window = tkinter.Tk()
window.title("Ditto's Gallery")

window.geometry('800x300') #set size of main window

#message box stuff
def greet():
    tkinter.messagebox.showinfo('Greetings', 'Ditto!')

btn = tkinter.Button(window, text="Ditto?", width=10, height=5, command=greet)
btn.place(x=700, y=30)

canvas = tkinter.Canvas(window, width=500, height=300) #create canvas
oval = canvas.create_oval(100,100,200,180, fill='green') #draw oval
canvas.pack()

window.mainloop() #run the loop that triggers the window
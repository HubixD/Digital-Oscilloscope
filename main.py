import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from tkinter import filedialog

#Window app config
osc = tk.Tk()
osc.wm_title("Digital Oscilloscope")

x1, y1 = 0.0 , 0.0
data = []

#Reading file from the path
def ReadData():
    path = filedialog.askopenfilename()
    with open(path, 'r') as file:
        sample = file.readlines()
        for line in sample:
            data.append(int(line.rstrip("\n"),16))         # conversion from hex
    file.close()
    osc.destroy()

#Marker definition
def Marker(event):
    global x1,y1

    if event.inaxes:                    #If we press on the graph then show the difference
        x2 = round(event.xdata,10)
        y2 = round(event.ydata,10)

        dx = round(abs(x2 - x1),10)
        dy = round(abs(y2 - y1),10)

        fig.suptitle("Marker 1("+str(x1)+ ","+str(y1)+ ")"+
                        "\n Marker 2("+str(x2)+ ","+str(y2)+ ")"+
                        "\n Delta x:"+str(dx)+"\t Delta y:" +str(dy))
        x1 = x2
        y1 = y2

    else:                               # If we press outside the graph
        fig.suptitle("\n Incorrect press, please click within the graph")

# Labels and window enhancement
Title = tk.Label(osc, text="Digital Oscilloscope", font="Arial 20 bold")
Title.pack()
Path = tk.Label(osc, text="\n Specify the file path", font="Arial 20")
Path.pack()
Path_box = tk.Entry(osc)
Path_box.pack()
Button = tk.Button(osc, text ="Search for Path", command = ReadData)
Button.pack()

osc.mainloop()

# Configuration of the plots
timebase = np.linspace(0,1/900, len(data))
data = np.array(data)*5/1024
fig,(ax2,ax) = plt.subplots(2)
fig.suptitle("Time Domain - Oscilloscope , Freq Domain - FFT")
ax.plot(timebase, data, 'm')
ax.set(xlabel = "Time[s]", ylabel = "Amplitude[V]")

#Markers for time and freq domain
marker1 = Cursor(ax, color="blue", linewidth = 2)
fig.canvas.mpl_connect('button_press_event',Marker)
marker2 = Cursor(ax2, color="blue", linewidth = 2)
fig.canvas.mpl_connect('button_press_event',Marker)

# Fast Fourier Transform
x_fft = np.fft.fftshift(np.fft.fft(data))
x_fft = 1/len(x_fft) * np.abs(x_fft)
f = np.linspace(-1/(2*(timebase[1]-timebase[0])),1/(2*(timebase[1]-timebase[0])),len(x_fft))
ax2.plot(f,x_fft, 'c-', linewidth="2")
ax2.set(xlabel = "Frequency[Hz]", ylabel = "Amplitude[V]")

plt.show()

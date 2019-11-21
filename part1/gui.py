from tkinter import *
root = Tk()


Label(text="Energy (keV)").grid(row=0, column=1)
Label(text="Inensity (1/s)").grid(row=0, column=2)
Label(text="FWHM (keV)").grid(row=0, column=3)

Label(text="Line:").grid(row=1, column=0)
energy = Entry(width=20)
energy.insert(0, 0)
energy.grid(row=1, column=1)
intensity = Entry(width=20)
intensity.insert(0, 0)
intensity.grid(row=1, column=2)
FWHM = Entry(width=20)
FWHM.grid(row=1, column=3)
FWHM.insert(0, 0)
addLine = Button(text="Add")
addLine.grid(row=1, column=4)

Label(text="a1 (number) *  ").grid(row=2, column=1)
Label(text="exp(a2 (1/keV) * x) + ").grid(row=2, column=2)
Label(text="a3 (number) + ").grid(row=2, column=3)
Label(text="a4 (number/keV) * x").grid(row=2, column=4)

Label(text="Background parameters:").grid(row=3, column=0)
a1 = Entry(width=20)
a1.grid(row=3, column=1)
a1.insert(0, 0)
a2 = Entry(width=20)
a2.grid(row=3, column=2)
a2.insert(0, 0)
a3 = Entry(width=20)
a3.grid(row=3, column=3)
a3.insert(0, 0)
a4 = Entry(width=20)
a4.grid(row=3, column=4)
a4.insert(0, 0)

Label(text="Time (s):").grid(row=5, column=0)
time = Entry(width=10)
time.grid(row=5, column=1)
time.insert(0, 1)
Label(text="E0 (keV):").grid(row=5, column=2)
E0 = Entry(width=10)
E0.grid(row=5, column=3)
E0.insert(0, 0)
Label(text="Channels number: ").grid(row=5, column=4)
channelsNum = Entry(width=10)
channelsNum.grid(row=5, column=5)
channelsNum.insert(0, 1000)
Label(text="Background intensity: ").grid(row=5, column=6)
backgroudIntensity = Entry(width=10)
backgroudIntensity.grid(row=5, column=7)
Label(text="Max energy (keV): ").grid(row=5, column=8)
maxEnergy = Entry(width=10)
maxEnergy.grid(row=5, column=9)


runButton = Button(width=80, text='RUN', bg='red')
runButton.grid(row=7, column=0, columnspan=10)


var = IntVar()
var.set(0)
clear = Radiobutton(text="Clear", variable=var, value=0)
clearBck = Radiobutton(text="Clear + Background", variable=var, value=1)
statBck = Radiobutton(text="Statistic + Background", variable=var, value=2)
statBckBlured = Radiobutton(text="Statistic + Background + Blurred", variable=var, value=3)

Label(text="Select build mode: ").grid(row=0, column=7)
clear.grid(row=1, column=7)
clearBck.grid(row=2, column=7)
statBck.grid(row=3, column=7)
statBckBlured.grid(row=4, column=7)

table_name = Button(text='Help')
table_name.grid(row=0, column=9)
 


logFile = open('logFile.txt', 'w+')

def GetLine(event):
	# --line 1 2 0.03
	s = '--line '
	s += intensity.get() + ' '
	s += energy.get() + ' '
	s += FWHM.get()
	logFile.write(s + '\n')

def GetBackground():
	# background parameters: par[0] * exp( par[1] * x) + par[2] + par[3] * x
	s = '--background '
	s += a1.get() + ' '
	s += a2.get() + ' '
	s += a3.get() + ' '
	s += a4.get()
	logFile.write(s + '\n')

def MakeRun(event):
	GetBackground()
	s = '--time '
	s += time.get()
	logFile.write(s + '\n')
	s = '--E_max '
	s += maxEnergy.get()
	logFile.write(s + '\n')
	s = '--background_intensity '
	s += backgroudIntensity.get()
	logFile.write(s + '\n')
	s = '--chanels '
	s += channelsNum.get()
	logFile.write(s + '\n')
	s = '--E0 '
	s += E0.get()
	logFile.write(s + '\n')
	# Add spectrum_build.py runner

addLine.bind('<Button-1>', GetLine)
runButton.bind('<Button-1>', MakeRun)

root.mainloop()

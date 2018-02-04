#MAITRI SHASTRI 2014B2A70220P#####################################################

from Tkinter import *

global can
global matrix


#this module was created in order to change the matrix on clicking and display coins on the board
#this module could not be integrated with the main module

def gameboarddisp():
	#displays the gameboard
	w=can.winfo_width()
	h=can.winfo_height()
	cellwidth=w/10
	cellheight=h/10
	can.create_rectangle(0,0,cellwidth*4,10,fill="red")
	for row in xrange(4):
		for col in xrange(4):
			if(matrix[row][col]==1):
				
				can.create_rectangle(col*cellwidth,row*cellheight,(col+1)*cellwidth,(row+1)*cellheight)
				can.create_oval(col*cellwidth,row*cellheight,(col+1)*cellwidth,(row+1)*cellheight,fill="blue")

			elif(matrix[row][col]==2):
				can.create_rectangle(col*cellwidth,row*cellheight,(col+1)*cellwidth,(row+1)*cellheight)
				can.create_oval(col*cellwidth,row*cellheight,(col+1)*cellwidth,(row+1)*cellheight,fill="green")
			elif(matrix[row][col]==0):
				can.create_rectangle(col*cellwidth,row*cellheight,(col+1)*cellwidth,(row+1)*cellheight,fill="white")
				can.create_oval(col*cellwidth,row*cellheight,(col+1)*cellwidth,(row+1)*cellheight,fill="white")

	can.create_rectangle(0,0,cellwidth*4,10,fill="red")


def gameboardclick(xclick,yclick):
	#make changes to the matrix and places coins on the gameboard
	w=can.winfo_width()
	h=can.winfo_height()
	cellwidth=100
	cellheight=100
	yindex=int(xclick/100)
	xindex=int(yclick/100)
	if(xindex<=4 and xindex>=0 and yindex<=4 and yindex>=0 ):
		matrix[xindex][yindex]=1
		print(cellwidth,cellheight)
		#display coins
		can.create_rectangle(yindex*cellwidth,xindex*cellheight,(yindex+1)*cellwidth,(xindex+1)*cellheight,fill="white")
		can.create_oval(yindex*cellwidth,xindex*cellheight,(yindex+1)*cellwidth,(xindex+1)*cellheight,fill="blue")
		can.create_rectangle(0,0,cellwidth*4,10,fill="red")	

def callback(event):
	#callback function 
	
	#print'clicked at',event.x,event.y
	gameboardclick (event.x,event.y)





window=Tk()
can=Canvas(window,width=1000,height=1000)	
can.grid(row=0,column=0)

window.update_idletasks()

matrix=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

gameboarddisp()




can.bind("<Button-1>",callback)

can.pack()





window.mainloop()	

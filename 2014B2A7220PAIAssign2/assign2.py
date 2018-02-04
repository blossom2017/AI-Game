############MAITRI SHASTRI ###########################
#############2014B2A70220P ###########################

import random
import copy
import time
from Tkinter import * 
import sys





global window
global can
global analysisobj
global analysisobjalpha



def initialmatrixgenerator():
	#generates the first random start position
	arr=[[0]*4 for i in xrange(4)]
	starty=random.randint(0,3)
	arr[0][starty]=2
	return arr


def islegal(ls):
	#checks whether the x and y index is within bounds[0,3]
	for item in ls:
		x=item[0]
		y=item[1]
		if(x<0 or x>=4 or y<0 or y>=4):
			return False
	return True		


class State:
	#state object containing matrix of 0s,1s(human),2s(agent) and to_play=min for human and max for agent
	def __init__(self):
		
		self.matrix=initialmatrixgenerator()
		self.to_play='min'

def gameboard(state):
	#displays the game board using Tkinter grpahics module
	matrix=state.matrix
	w=can.winfo_width()
	h=can.winfo_height()
	cellwidth=w/10
	cellheight=h/10

	#display coins
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

	#display baseline
	can.create_rectangle(0,0,cellwidth*4,10,fill="red")

	
				


def printState(state):
	#printing matrix state on the terminal
	for i in xrange(0,4):
		print(state.matrix[i])
		
	

def getTerminalValue(state):
	#utility function that gives utility value for terminal states +1 for agent win
	#-1 for human win
	#0 for others
	matrix=state.matrix
	flagm=False

	for x in xrange(0,4):
		for y in xrange(0,4):
			if(matrix[x][y]!=0):
				#horizontal win 
				#print('Entering if')
				#print(x,y)

				value=matrix[x][y]
				#print('value is',value)
				flagh=False
				flagv=False
				flagd=False
				flagd2=False
				lshorizontal=[[x,y],[x,y+1],[x,y+2]]
				lsvertical=[[x,y],[x+1,y],[x+2,y]]
				lsdiagonal=[[x,y],[x+1,y+1],[x+2,y+2]]
				lsdiagonal2=[[x,y],[x+1,y-1],[x+2,y-2]]
				if(islegal(lshorizontal)==True ):
					#print('entering islegal if hori')
					for(xval,yval) in lshorizontal:
						if(matrix[xval][yval]!=value):
							flagh=False
							break
						else:
							flagh=True	

				if(islegal(lsvertical)==True ):
					#print('entering islegal if vert')
					for(xval,yval) in lsvertical:
						if(matrix[xval][yval]!=value):
							flagv=False	
							break
						else:
							flagv=True		
				if(islegal(lsdiagonal)==True):
					#print('entering islegal if diag')
					for (xval,yval) in lsdiagonal:
						if(matrix[xval][yval]!=value):
							flagd=False
							break
						else:
							flagd=True	
				if(islegal(lsdiagonal2)==True):
					#print('entering islegal if diag')
					for (xval,yval) in lsdiagonal2:
						if(matrix[xval][yval]!=value):
							flagd2=False
							break
						else:
							flagd2=True				
				

				flagm=flagd or flagv or flagh or flagd2	
				if(flagm==True):
					break
		if(flagm==True):
			break				

	
	if(flagm==False):
		return 0
	elif(flagm==True and value==1):
		return -1
	elif(flagm==True and value==2):
		#print(xval,yval)
		return 1


def isDraw(state):
	#checks if there is a draw by counting coins
	count=0
	for i in xrange(0,4):
		for j in xrange(0,4):
			if(state.matrix[i][j]==1 or state.matrix[i][j]==2):
				count=count+1
	if(count==16):
		return True
	return False

	
def TerminalTest(state):
	#return True if state is terminal state else returns false
	termutil=getTerminalValue(state)
	if(termutil==-1 or termutil==1):
		return True
	elif(termutil==0):
		count=0
		for i in xrange(0,4):
			for j in xrange(0,4):
				if(state.matrix[i][j]==1 or state.matrix[i][j]==2):
					count=count+1
		if(count==16):
			return True
		return False



def getMoves(state):
	#returns a list of valid moves
	moves=[]
	for y in xrange(0,4):
		for x in xrange(0,4):
			if(state.matrix[x][y]==0):
				moves.append([x,y])
				break
	#print('in getMoves')
	#print(moves)			
	return moves

def getsucessors(state):
	#returns tuples of form (move,succstate) for given state
	succ=[]
	moves=getMoves(state)
	for move in moves:
		succ.append((move,result(state,move)))
	return succ	




def result(state,move):
	#returns a new state corresponding to the move
	if move not in getMoves(state):
		#illegal moves have no effect
		return state
	
	xval=move[0]
	yval=move[1]
	newstate=copy.deepcopy(state)
	
	if(state.to_play=='max'):
		newstate.matrix[xval][yval]=2
		newstate.to_play='min'
	elif(state.to_play=='min'):
		newstate.matrix[xval][yval]=1
		newstate.to_play='max'	
	return newstate
	

def playGame(state,option):
	while(True):
		if(TerminalTest(state) and getTerminalValue(state)==-1):
			if(option==2):
				analysisobj.whowon ='human'
			elif(option==3):
				analysisobjalpha.whowon='human'
			print'Agent Lost and human player won'
			print'Final state'
			printState(state)
			gameboard(state)
			
			break
		elif(TerminalTest(state) and getTerminalValue(state)==1):
			print'Agent won and human player lost'
			if(option==2):
				analysisobj.whowon ='agent'
			elif(option==3):
				analysisobjalpha.whowon='agent'	
			print'Final state'
			printState(state)
			gameboard(state)
			#time.sleep(3)
			break
		elif(TerminalTest(state) and isDraw(state)):
			print'Draw'	
			if(option==2):
				analysisobj.whowon ='draw'
			elif(option==3):
				analysisobjalpha.whowon='draw'	
			gameboard(state)
			#time.sleep(3)
			break
		else:
			gameboard(state)
			state=human_player(state)
			gameboard(state)
			printState(state)

			
			
			if not (TerminalTest(state)):
				if(option==2):
					#state.to_play='min'
					t1=time.time()
					
					move=minimaxdecision(state)

					t2=time.time()
					analysisobj.time_taken=analysisobj.time_taken+(t2-t1)

					state=result(state,move)


					printState(state)
					gameboard(state)
				elif(option==3):
					t1=time.time()
					move=alphabetasearch(state)	
					t2=time.time()
					analysisobjalpha.time_taken_alpha=analysisobjalpha.time_taken_alpha+(t2-t1)
					state=result(state,move)
					printState(state)
					gameboard(state)

#MINMAX ALGORITHM	
def minimaxdecision(state):
	(v,i)=maxval(state)
	analysisobj.implicit_stack=analysisobj.implicit_stack+1
	return getMoves(state)[i]

def maxval(state):

	indextrack=[]
	analysisobj.implicit_stack=analysisobj.implicit_stack+1
	if(TerminalTest(state)):
		
		return (getTerminalValue(state),1)
	v=-100#negative infinity
	succ=getsucessors(state)
	#print(succ)
	for t in succ:
		analysisobj.numnodesminimax=analysisobj.numnodesminimax+1
		#print(t[1].matrix)
		
		(a,i)=minval(t[1])
		v=max(v,a)
		indextrack.append(v)

	return 	(v,indextrack.index(max(indextrack)))

def minval(state):
	indextrack=[]
	analysisobj.implicit_stack=analysisobj.implicit_stack+1
	if(TerminalTest(state)):
		return (getTerminalValue(state),1)
	v=100#positive infinity
	succ=getsucessors(state)
	for t in succ:
		analysisobj.numnodesminimax=analysisobj.numnodesminimax+1
		
		#print(t[1].matrix)
		(a,i)=maxval(t[1])
		v=min(v,a)
		indextrack.append(v)
	return (v,indextrack.index(min(indextrack)))
				
			


		
def human_player(state):
	#takes user input 
	move=[]
	print 'Current state'
	printState(state)
	movesvalid=getMoves(state)
	print(movesvalid)
	move_numberx=input('Enter your move-x')
	move.append(move_numberx)
	move_numbery=input('Enter you move-y')
	move.append(move_numbery)
	if(move in movesvalid):
		state.matrix[move_numberx][move_numbery]=1
		state.to_play='max'
		return state
	else:
		print'Invalid move'
		return human_player(state)	


#ALPHA BETA PRUNING
def alphabetasearch(state):
	v,i=alphabetamaxval(state,-100,+100)
	analysisobjalpha.implicit_stackalpha=analysisobjalpha.implicit_stackalpha+1
	return getMoves(state)[i]


def alphabetamaxval(state,a,b):
	indextrack=[]
	analysisobjalpha.implicit_stackalpha=analysisobjalpha.implicit_stackalpha+1
	if(TerminalTest(state)):
		return (getTerminalValue(state),1)
	v=-100#negative infinity
	succ=getsucessors(state)
	for t in succ:
		
		analysisobjalpha.numnodesalphabeta=analysisobjalpha.numnodesalphabeta+1
		temp,i=alphabetaminval(t[1],a,b)
		v=max(v,temp)
		indextrack.append(v)	
		if(v>=b):
			return v,indextrack.index(v)
		#v=max(indextrack)	
		a=max(a,v)
	return v,indextrack.index(v)

def alphabetaminval(state,a,b):
	indextrack=[]

	analysisobjalpha.implicit_stackalpha=analysisobjalpha.implicit_stackalpha+1
		
	if(TerminalTest(state)):
		return (getTerminalValue(state),1)
	v=100#positive infinity
	succ=getsucessors(state)
	for t in succ:
		analysisobjalpha.numnodesalphabeta=analysisobjalpha.numnodesalphabeta+1
		temp,i=alphabetamaxval(t[1],a,b)
		v=min(v,temp)
		indextrack.append(v)
		if(v<=a):
			return v,indextrack.index(v)
		#v=min(indextrack)	
		b=min(b,v)
	return v,indextrack.index(v)

#ANALYSIS MODULE CLASSES

class analysis:
	#FOR MINMAX
	def __init__(self):
		self.numnodesminimax=0
		self.implicit_stack=0
		
		self.time_taken=0
		self.whowon='None'

class analysisalphabeta:
	#FOR ALPHA BETA PRUNING
	def __init__(self):
		self.numnodesalphabeta=0
		self.implicit_stackalpha=0
		self.time_taken_alpha=0		
		self.whowon='None'


if __name__ == '__main__':
	

	
	


	
	window=Tk()
	can=Canvas(window,width=1000,height=1000)	
	can.grid(row=0,column=0)
	window.update_idletasks()
	ch=1
	while(ch!=0):
		print'entering'
		option=input('Enter option 1-display gameboard/2-minmax/3-alphabeta/4-analysis')
		st=State()
		stalpha=copy.deepcopy(st)

		if(option==1):
			gameboard(st)
			ch=input('Press 1 to continue and 0 to end the game ')	
			
		elif(option==2):	
		
		#numnodesminimax=0
			gameboard(st)
			analysisobj=analysis()
			#print(st.matrix)
			#printState(st)
			playGame(st,2)
			ch=input('Press 1 to continue and 0 to end the game ')		
			
		elif(option==3):
			gameboard(st)
			analysisobjalpha =analysisalphabeta()
			#print(st.matrix)
			#printState(st)
			playGame(st,3)
			print'R6:Number of nodes generated till problem is solved',analysisobjalpha.numnodesalphabeta
			ch=input('Press 1 to continue and 0 to end the game ')	
			
		elif(option==4):	
			
			gameboard(st)
			analysisobj=analysis()	
			playGame(st,2)
			analysisobjalpha=analysisalphabeta()
			gameboard(stalpha)
			print'Play again using alpha beta pruning'
			playGame(stalpha,3)

			print'MINMAX ALGORTIHM BASED ANALYSIS'
			print('R1:Number of nodes generated till the problem is solved',analysisobj.numnodesminimax)
			memnode=sys.getsizeof(st)
			print('R2:Memory allocated to one node is',memnode)
			print'R3:Maximum Growth of implicit stack in search tree',analysisobj.implicit_stack
			print'R4:Total time to play the game using minmax',analysisobj.time_taken
			numnodesms=int(analysisobj.numnodesminimax/analysisobj.time_taken)
			print'R5:Number of nodes created in 1 sec',numnodesms

			print'ALPHA BETA PRUNING BASED ANALYSIS'
			print'R6:Number of nodes generated till problem is solved',analysisobjalpha.numnodesalphabeta
			print'R7:Saving using pruning',((analysisobj.numnodesminimax- analysisobjalpha.numnodesalphabeta)/analysisobj.numnodesminimax)
			print'R8:Total time to play a game',analysisobjalpha.time_taken_alpha

			print'COMPARATIVE ANALYSIS'
			print'Memory used in minmax technique',memnode*analysisobj.numnodesminimax+analysisobj.implicit_stack*memnode
			print'Memory used in alpha beta technique',memnode*(analysisobjalpha.numnodesalphabeta+ analysisobjalpha.implicit_stackalpha)
			print'Comparing R4 and R8'
			print'R4:Total time to play the game using minmax',analysisobj.time_taken
			print'R8:Total time to play a game',analysisobjalpha.time_taken_alpha

		
			summinmax=0
			sumalpha=0
			countwinmin=0
			countwinalpha=0
			
			for x in xrange(0,10):
				st=State()
				stalpha=copy.deepcopy(st)
				gameboard(st)
				analysisobj=analysis()	
				playGame(st,2)
				if(analysisobj.whowon=='agent'):
					countwinmin=countwinmin+1
				analysisobjalpha=analysisalphabeta()
				gameboard(stalpha)
				playGame(stalpha,3)
				if(analysisobjalpha.whowon=='agent'):
					countwinalpha=countwinalpha+1


				summinmax=summinmax+analysisobj.time_taken
				sumalpha=sumalpha+analysisobjalpha.time_taken_alpha

			print'R10:Average time to play game using minmax ',summinmax/10
			print'R10:Average time to play game using alpha beta pruning',sumalpha/10
			print'R11:Number of times M wins using minmax',countwinmin
			print'R11:Number of times M wins using alpha beta pruning',countwinalpha

			for i in range(0,200):
				st=State()
				gameboard(st)
				analysisobj=analysis()	
				playGame(st,2)
				if(analysisobj.whowon=='agent'):
					countwinmin=countwinmin+1

			print'R12:Average number of times agent wins in 10 games is ',countwinmin/20	
			ch=input('Press 1 to continue and 0 to end the game ')		
		




	time.sleep(5)
	window.mainloop()
	window.quit()


#PENDING-CALLIBRATION INTEGRATION AND IMPLICIT STACK CORRECT CALCULATION

				

N = 6
g=[["7FEQT",-50],["19EGQ",10],["6WF",20],["7FEQ",-10],["7FE",-10],["7",40]]
l1=[]
l2=[]
graph=[]
final={}
f={}
j=0
for i in g:
	final[i[0]]=j
	f[j]=final[i[0]]
	j=j+1
for i in range(N):
	l3=[]
	for j in range(N):
		l3=l3+[0]
	graph=graph+[l3]
for i in g:
	if(i[1] == 0):
		continue
	elif(i[1] > 0):
		l1=l1+[i]
	else:
		l2=l2+[i]
def f(l1,l2):
	global graph
	simplify(l1,l2,graph)
def simplify(li1,li2,graph):
	if(len(li1) == 0 or len(li2) == 0):
		return
	else:
		y=li1[0]
		if(y[1] + li2[0][1] == 0):
			graph[final[y[0]]][final[li2[0][0]]] = graph[final[y[0]]][final[li2[0][0]]] + y[1]
			simplify(li1[1:],li2[1:],graph)
		elif(y[1] + li2[0][1] > 0):
			graph[final[y[0]]][final[li2[0][0]]] = graph[final[y[0]]][final[li2[0][0]]] - li2[0][1]
			y[1] = y[1]+li2[0][1]
			simplify(li1,li2[1:],graph)
		else:
			graph[final[y[0]]][final[li2[0][0]]] = graph[final[y[0]]][final[li2[0][0]]] + y[1]
			li2[0][1]=y[1]+li2[0][1]
			simplify(li1[1:],li2,graph)

f(l1,l2)
l11=[]
print(graph)
def getMin(arr): 	
	minInd = 0
	for i in range(1, N): 
		if (arr[i] < arr[minInd]): 
			minInd = i 
	return minInd 
def getMax(arr): 
	maxInd = 0
	for i in range(1, N): 
		if (arr[i] > arr[maxInd]): 
			maxInd = i 
	return maxInd 
def minOf2(x, y): 
	return x if x < y else y 
def minCashFlowRec(amount): 
	mxCredit = getMax(amount)
	global l11
	mxDebit = getMin(amount) 
	if (amount[mxCredit] == 0 and amount[mxDebit] == 0): 
		return 0
	min = minOf2(-amount[mxDebit], amount[mxCredit]) 
	amount[mxCredit] -=min
	amount[mxDebit] += min
	l11=l11+[[mxDebit,min,mxCredit]]
	minCashFlowRec(amount) 
def minCashFlow(graph): 
	amount = [0 for i in range(N)] 
	for p in range(N): 
		for i in range(N): 
			amount[p] += (graph[i][p] - graph[p][i]) 
	minCashFlowRec(amount)
minCashFlow(graph)
need = []
for i in range(N):
	l3=[]
	for j in range(N):
		l3=l3+[0]
	need = need + [l3]
for i in l11:
	need[i[0]][i[2]] = i[1]
print(need)
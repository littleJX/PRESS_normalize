import re
import numpy as np
# if you don't need distance image, below 3 header(matplotlib) can be deleted.
import matplotlib.pyplot as plt 
from matplotlib.ticker import FuncFormatter
import matplotlib

#[Parameter setting]###################################

filename = "data4.txt"

sep_thd=30 #mm, grouping threshold, minimum distance between groups

parser_x = "0\]\s+(\d+),\s+\d+,\s+\d+,"
parser_y = "0\]\s+\d+,\s+(\d+),\s+\d+,"
parser_s = "0\]\s+\d+,\s+\d+,\s+(\d+),"

x_grid_num =10
y_grid_num =19

#######################################################

def distance(x1,y1,x2,y2):
	return np.sqrt(pow(x1-x2,2)+pow(y1-y2,2))

def parsing(filename,parser_x,parser_y,parser_s):
	fin = open(filename, 'r')
	f = fin.read()
	fin.close()

	x=[]
	y=[]
	s=[]
	x_str = re.findall(parser_x, f)
	y_str = re.findall(parser_y, f)
	s_str = re.findall(parser_s, f)

	num=len(x_str)

	for i in range(num):
	    x.append(int(x_str[i]))
	    y.append(int(y_str[i]))
	    s.append(int(s_str[i]))

	return x,y,s

def gruping(x,y):
	groupnum=1
	group = []
	num=len(x)
	group.append(groupnum)
	for i in range(num-1):
		if (np.absolute(x[i+1]-x[i])>sep_thd)|(np.absolute(y[i+1]-y[i])>sep_thd):
			groupnum=groupnum+1
		group.append(groupnum)

	# print 'groupnum :', groupnum
	# print group
	return groupnum,group

def find_MaxPress(x,y,s,groupnum,group):
	max_s=[]
	max_x=[]
	max_y=[]

	for i in range(1,groupnum):
		tmp_max = np.max(s[group.index(i):group.index(i+1)])
		max_s.append(tmp_max)

		idx=s[group.index(i):group.index(i+1)].index(tmp_max)
		max_x.append(x[group.index(i)+idx])
		max_y.append(y[group.index(i)+idx])

	tmp_max = np.max(s[group.index(groupnum):len(group)-1])
	max_s.append(tmp_max)

	idx=s[group.index(groupnum):len(group)-1].index(tmp_max)
	max_x.append(x[group.index(groupnum)+idx])
	max_y.append(y[group.index(groupnum)+idx])
	
	return max_x, max_y, max_s

def print_table(name, table):
	print "["+name+"]"
	for j in range(y_grid_num):
		str_tmp=""
		for i in range(x_grid_num):
			str_tmp = str_tmp + str(table[i+j*x_grid_num])+"," 
		print str_tmp
	print ''

def make_normal_table(table,target):
	normal_table=[]
	for i in range(len(table)):
		val=64*target/table[i]
		normal_table.append(val)
	return normal_table

#[MAIN]##############################

(x,y,s)=parsing(filename,parser_x,parser_y,parser_s)
(groupnum,group)=gruping(x,y)
(max_x, max_y, max_s)=find_MaxPress(x,y,s,groupnum,group)

print_table("Max Intensity Table", max_s)

normal_table = make_normal_table(max_s,40)

print_table("Normalizing Table", normal_table)

##################################################################
avg_x=[]
avg_y=[]
for i in range(1,groupnum):
	avg_x.append(np.mean(x[group.index(i):group.index(i+1)]))
	avg_y.append(np.mean(y[group.index(i):group.index(i+1)]))
avg_x.append(np.mean(x[group.index(groupnum):len(group)-1]))
avg_y.append(np.mean(y[group.index(groupnum):len(group)-1]))

avg_x = max_x
avg_y = max_y

for i in range(len(avg_x)):
	if avg_y[i+1]-avg_y[i] > sep_thd:
		nCol = i+1
		nRow=groupnum/nCol
		break

print "X_NUM: ",nCol
print "Y_NUM: ",nRow

x_mat = np.array(avg_x).reshape((nRow, nCol))
y_mat = np.array(avg_y).reshape((nRow, nCol))

x_tic=[]
y_tic=[]

for i in range(nCol):
	x_tic.append(int(np.mean([row[i] for row in x_mat])))

for i in range(nRow):
	y_tic.append(int(np.mean(y_mat[i])))

print "x_tic: ",x_tic
print "y_tic: ", y_tic

#[PLOT]#############################################
plt.subplot(1, 2, 1)
plt.scatter(x,y,s,edgecolors='none')
plt.title('scattering')
plt.gca().invert_yaxis()
plt.grid()

plt.subplot(1, 2, 2)
m =  np.array(max_s).reshape((y_grid_num, x_grid_num))
plt.imshow(m,interpolation='nearest')
plt.tight_layout()
plt.title("max image")
plt.colorbar()
plt.show()
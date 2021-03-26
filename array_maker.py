import pickle

##############################################################################
####################### FILE/LEVEl TO EDIT HERE ##############################
level = 0
##############################################################################
##############################################################################

height=450
width_original = 780
##########length of level
width = width_original*3

block=30
no_of_row=int(width/block)
no_of_column=int(height/block)

no_of_tile=width_original//block
middle = no_of_tile//2
##for me lists are in [[20 elements
#],......]
print(f'no_of_column : {no_of_column}')
print(f'no_of_row : {no_of_row}')
print(f'screen width : {width_original/block}')
array=[]
temp_array=[]

#making a empty array
for row in range(0,no_of_row):

	for column in range(0,no_of_column):
		temp_array.append(0)
	array.append(temp_array)
	temp_array=[]
#
j=0
for row in array:
	i=0
	for column in row:
		
		#making the useless block dirt
		if j <= middle:
			row[i]=1
		#making last 2 dirt vertical ( BOTTOM ONE)
		elif i>no_of_column - 3 :
			row[i]=1
		#making last 8 dirt horizontal (last in level)
		elif j>no_of_row-16:
			row[i]=1

		i+=1
		
	j+=1
#print(middle)
with open(f"data{level}.ani","wb") as f:
	pickle.dump(array,f)


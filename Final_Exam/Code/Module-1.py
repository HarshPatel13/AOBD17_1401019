import pandas as pd
import os
import numpy as n
from random import randint
import time

folder = os.listdir("CSV")
skillBreakUp = []

goal = randint(0,len(folder)-1)
str = folder[goal].replace('.csv','')
print('\n----------------------------------------------------------------------------------------------------------------------')
print('Career')
print(str)
print('----------------------------------------------------------------------------------------------------------------------')

reviews = pd.read_csv("CSV/"+folder[goal])

users = randint(0,reviews.shape[0]-1)
userDetails = reviews.iloc[0,1:13]

print('\n----------------------------------------------------------------------------------------------------------------------')
print('User Details')
print(userDetails)
print('----------------------------------------------------------------------------------------------------------------------')


skills = reviews.loc[:,'Skills']

t = time.clock()
for i in skills:
	temp = i.replace('(','')
	temp = temp.replace(')','')
	temp = temp.replace('&&',',')
	temp = temp.replace('. ',',')
	
	temp = temp.split(',')
	
	for m in temp:
		if 'year' not in m:
			if 'years' not in m:
				if m not in skillBreakUp:
					if len(m)>0:
						skillBreakUp.append(m.strip())
					
numOfSkills = len(skillBreakUp)
users = len(reviews)
skillMatrix = n.zeros((users,numOfSkills))

for i in range(0,users):
	for j in range(0,numOfSkills):
		if skillBreakUp[j] in skills[i]: # Checking if the current user has a particular skill or not
			skillMatrix[i,j] = 1
			
freq = skillMatrix.sum(axis=0)

temp = n.unique(freq)[::-1] # Sorting in descending order of frequency

temp = temp[0:3] # Top 3 skills

# Suggesting skills to the user

print('\n----------------------------------------------------------------------------------------------------------------------')
print('Suggested Skills for the user for the Career Goal of',str,'\n----------------------------------------------------------------------------------------------------------------------')

for i in temp:
	k = n.where(freq==i)
	k = k[0].tolist()
	for j in k:
		print(skillBreakUp[j])
		
print('\n\nTime taken:',time.clock()-t)
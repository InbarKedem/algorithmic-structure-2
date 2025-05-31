# ~~~ This is a template for question 2  ~~~

#Imports:
import numpy as np
import pandas as pd
from lief import type_error


###Part A###
#~~~  implementation of heap class  ~~~
class Heap():
    def __init__(self, A):
        #Initialize the Heap with a list A for t as the heap list and size as len(A)
        self.t=A.tolist()
        if len(A)>200:
            raise TypeError("A exceeds heap limit")
        else:
            self.size = len(self.t)
        for i in range(self.size,-1,-1):
            self.heapify(i)

    def insert(self, x):
        #Add x to the end and increase size and heapify the new member
        self.t.append(x)
        self.size+=1
        self.heapify(self.size-1)

    def delete_min(self):
        #Remove the value in the first index and put the value in the end of the heap and heapify 0 to remain a heap
        min=self.t[0]
        self.t[0]=self.t[self.size-1]
        self.size-=1
        self.t.pop(self.size)
        self.heapify(0)
        return min

    def heapify(self,i):
        #this function is a recursive function that checks if the children of the input index
        #are smaller than the current index then they swap and we heapify the index that we swapped into until it gets to the right place.
        l = 2 * i + 1
        r = 2 * i + 2
        min=i
        if l<self.size and self.t[l]<self.t[i]:
            min=l
        if r<self.size and self.t[r]<self.t[min]:
            min=r
        if min!=i:
            holder=self.t[i]
            self.t[i]=self.t[min]
            self.t[min]=holder
            self.heapify(min)




###Part B###
def optimal_value_merge_problem(prices):
    """
    :param prices:Array
    In this function firstly we heapify the given array and then we combine the two minimal
    companies and insert them back into the array. Thus creating a Huffman optimal sum heap
    :return: the sum of the optimal tax Float/int
    """
    h=Heap(prices)
    min1=0
    min2=0
    total_cost=0
    while h.size>1:
        min1=h.delete_min()
        min2=h.delete_min()
        total_cost+=(min1+min2)
        h.insert(min1+min2)
    return total_cost

df=pd.read_excel("data_2.xlsx")
A=df.iloc[:,0]
print(A)
print(optimal_value_merge_problem(A))


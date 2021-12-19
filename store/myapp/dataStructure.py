from datetime import date, timedelta
class LinkedList:
    class Node :
        def __init__(self,data,next = None) :
            self.data = data
            if next is None :
                self.next = None
            else :
                self.next = next
                
        def __str__(self) :
            return str(self.data)

    def __init__(self,head = None):
        if head == None:
                self.head = self.tail = None
                self.size = 0
        else:
            self.head = head
            t = self.head        
            self.size = 1
            while t.next != None :
                t = t.next
                self.size += 1
            self.tail = t
            
    def __str__(self) :
        s = 'Linked data : '
        p = self.head
        while p != None :
            s += str(p.data)+' '
            p = p.next
        return s

    def __len__(self) :
        return self.size
    
    def append(self, data):
        p = self.Node(data)
        if self.head == None:
            self.head = self.tail = p
        else:
            t = self.tail
            t.next = p   
            self.tail =p  
        self.size += 1

    def removeHead(self) :
        if self.head == None : return
        if self.head.next == None :
            p = self.head
            self.head = None
        else :
            p = self.head
            self.head = self.head.next
        self.size -= 1
        return p.data
    
    def isEmpty(self) :
        return self.size == 0
    
    def nodeAt(self,i) :
        p = self.head
        for j in range(i) :
            p = p.next
        return p
    def reverse(self):
        prev = None
        current = self.head
        while(current is not None):
            next = current.next
            current.next = prev
            prev = current
            current = next
        self.head = prev
    def convertToArr(self):
        #len1 = findlength(head)
        arr = []
        index = 0
        curr = self.head
        while (curr != None):
            arr.append( curr.data)
            curr = curr.next
        #printArr(arr, len1)
        return arr
    def sortList(self,asc=True):  
        #Node current will point to head  
        current = self.head;  
        index = None;  
        
        if(self.head == None):  
            return;  
        else:  
            while(current != None):  
                #Node index will point to node next to current  
                index = current.next;  
                
                while(index != None):  
                    if asc:
                        #change year
                        if(current.data.get('created').year > index.data.get('created').year):  
                            temp = current.data;  
                            current.data = index.data;  
                            index.data = temp;  
                        if(current.data.get('created').year == index.data.get('created').year):
                            #change month
                            if(current.data.get('created').month > index.data.get('created').month):  
                                temp = current.data;  
                                current.data = index.data;  
                                index.data = temp;  
                                #change day
                            if(current.data.get('created').month == index.data.get('created').month):
                                if(current.data.get('created').day > index.data.get('created').day):  
                                    temp = current.data;  
                                    current.data = index.data;  
                                    index.data = temp;  
                    else:
                        #change year
                        if(current.data.get('created').year< index.data.get('created').year):  
                            temp = current.data;  
                            current.data = index.data;  
                            index.data = temp;  
                        if(current.data.get('created').year == index.data.get('created').year):
                            #change month
                            if(current.data.get('created').month < index.data.get('created').month):  
                                temp = current.data;  
                                current.data = index.data;  
                                index.data = temp;  
                                #change day
                            if(current.data.get('created').month == index.data.get('created').month):
                                if(current.data.get('created').day < index.data.get('created').day):  
                                    temp = current.data;  
                                    current.data = index.data;  
                                    index.data = temp;  
                    index = index.next;  
                current = current.next;  


class Queue:
    def __init__(self,list=None):
        if list==None:
            self.items=[]
        else:
            self.items=list
    def enQueue(self,i):
        self.items.append(i)
    def deQueue(self):
        return self.items.pop(0)
    def deQueueleft(self):
        return self.items.pop(-1)
    def isEmpty(self):
        return len(self.items)==0
    def size(self):
        return len(self.items)
    def peek(self):
        return self.items[len(self.items)-1]    
    def __str__(self):
        return "".join(str(self.items))

def merge_sort(lst):
    #global count
    if len(lst)<=1:
        return lst
    mid = len(lst)//2 #แบ่งครั้ง
    left=lst[:mid]
    right=lst[mid:]
    left=merge_sort(left)
    right = merge_sort(right)
    #count+=1
    return list(sort_list(left,right))

def sort_list(left,right):
    #global count
    lst =[]
    while len(left)!=0 and len(right)!=0:
        if left[0].get('price')<right[0].get('price'):
            lst.append(left[0])
            left.pop(0)
        else:
            lst.append(right[0])
            right.pop(0)
        #count+=1
    if len(left)==0:
        lst = lst + right
        #count+=1
    else:
        lst = lst +left
        #count+=1
    return lst

def sort_by_price(q):
    #lst_of_data#get dict
    lst_of_data=[]
    for list_index in range(q.size()):#list
        dicts=q.deQueue() 
        for dictt in dicts:#dict
            #print(dictt.get('price'))
            lst_of_data.append(dictt)
            for y in dictt:#key
                pass
    lst_sorted = merge_sort(lst_of_data)
    #print('lst sorted',lst_sorted)
    new_q = Queue()
    for x in lst_sorted:
        new_q.enQueue(x)
    return lst_sorted

#Sort price
def radixSort(lst):
    q=Queue(lst)
    max_digit=getMaxDigit(lst)
    q10=[Queue(),Queue(),Queue(),Queue(),Queue(),Queue(),Queue(),Queue(),Queue(),Queue()]
    for i in range(1,max_digit+1):
        while not q.isEmpty():
            num=q.dequeue()
            indexDigit=getDigit(num,i)
            q10[indexDigit].enqueue(num)
        print('\nQQ:',end=' ')
        for i in range(10):
            print(q10[i],end=' ')
        for j in range(10):
            
            while not q10[j].isEmpty():
                q.enqueue(q10[j].dequeue())
    return q.list
def getDigit(n,d):
    for i in range(d-1):
        n//=10
    return n%10
def getMaxDigit(lst):
    n=max(lst)
    i=0
    while n>0:
        n//=10
        i+=1
    return i

def build_Linkedlist(q_Products):
    l1=LinkedList()
    for i in q_Products:
        #print(i.get('created'))
        #print(i.get('created').year,i.get('created').month,i.get('created').day)
        l1.append(i)
    return l1
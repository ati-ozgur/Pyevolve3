class Node:
    def __init__(self, data = None):
        self.data = data
        self.previous = self
        self.next = self

class DCLL:
    def __init__(self):
        self.head = None
        self.count = 0

    def __repr__(self):
        string = ""

        if (self.head == None):
            string += "Doubly Circular Linked List Empty"
            return string

        string += f"Doubly Circular Linked List:\n{self.head.data}"
        temp = self.head.next
        while (temp != self.head):
            string += f" -> {temp.data}"
            temp = temp.next
        return string

    def append(self, data):
        self.insert(data, self.count)
        return

    def insert(self, data, index):
        if (index > self.count) | (index < 0):
            raise ValueError(f"Index out of range: {index}, size: {self.count}")

        if self.head == None:
            self.head = Node(data)
            self.count = 1
            return

        temp = self.head
        if (index == 0):
            temp = temp.previous
        else:
            for _ in range(index - 1):
                temp = temp.next

        temp.next.previous = Node(data)
        temp.next.previous.next, temp.next.previous.previous = temp.next, temp
        temp.next = temp.next.previous
        if (index == 0):
            self.head = self.head.previous
        self.count += 1
        return

    def remove(self, index):
        if (index >= self.count) | (index < 0):
            raise ValueError(f"Index out of range: {index}, size: {self.count}")

        if self.count == 1:
            self.head = None
            self.count = 0
            return

        target = self.head
        for _ in range(index):
            target = target.next

        if target is self.head:
            self.head = self.head.next

        target.previous.next, target.next.previous = target.next, target.previous
        self.count -= 1

    def index(self, data):
        temp = self.head
        for i in range(self.count):
            if (temp.data == data):
                return i
            temp = temp.next
        return None

    def get(self, index):
        if (index >= self.count) | (index < 0):
            raise ValueError(f"Index out of range: {index}, size: {self.count}")

        temp = self.head
        for _ in range(index):
            temp = temp.next
        return temp.data

    def size(self):
        return self.count

    def display(self):
        print(self)

#Methods prepared for the project
# get prev i next
    def getp(self, index):
        if (index >= self.count) | (index < 0):
            raise ValueError(f"Index out of range: {index}, size: {self.count}")

        temp = self.head
        for _ in range(index):
            temp = temp.next
        print("liczba: "+str(temp.data))
        print("prev: " + str(temp.previous.data))
        print("next: " + str(temp.next.data))

# get index
    def getindex(self, rangelist,value):

        for index in range(0,rangelist):

            if (index >= self.count) | (index < 0):
                raise ValueError(f"Index out of range: {index}, size: {self.count}")

            temp = self.head
            for _ in range(index):
                temp = temp.next
            if(temp.data==value):
                return index

#Get neighbours of element for IGX crossover.
    def getleftright(self, rangelist, value):
        list = []
        for index in range(0, rangelist):

            if (index >= self.count) | (index < 0):
                raise ValueError(f"Index out of range: {index}, size: {self.count}")

            temp = self.head
            for _ in range(index):
                temp = temp.next
            if (temp.data == value):
                list.append(temp.previous.data)
                list.append(temp.next.data)
                return list
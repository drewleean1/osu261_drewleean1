# Name: Andrew Lee
# OSU Email: leea6@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 2
# Due Date: 10/24/2022
# Description: An implementation of a DynamicArray data structure using a StaticArray as it's underlying framework.
#Student implemented methods: resize, append, insert_at_index, remove_at_index, slice, merge, map, filter, reduce,
#and the outside of class function find_mode


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        '''method that will create a new StaticArray with capacity equal to the given new_capacity, copy data
        from the current StaticArray over, and then assign self._data to the new array.'''
        if new_capacity <= 0 or new_capacity < self._size:
            return
        new_array = StaticArray(new_capacity)
        lesser_of_two = None                                      #assign to new var whichever is smaller, new_capacity
        if new_capacity < self.length():                          #or self._data.length() to avoid an IndexBoundError
            lesser_of_two = new_capacity
        else:
            lesser_of_two = self.length()
        for x in range(lesser_of_two):                              #for loop to copy values from old to new array
            new_array[x] = self._data[x]
        self._data = new_array
        self._capacity = new_capacity

    def append(self, value: object) -> None:
        '''method that appends the given value to the end of our array and doubles the array by calling resize if there
        is not enough capacity'''
        if self.get_capacity() == self.length():
            self.resize(self.get_capacity() * 2)
        self._data[self.length()] = value
        self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        '''method that inserts given value at the given index, moving all elements down one spot. Method will also double
        size of the array if necessary by calling resize and will raise an exception if the given index is invalid'''
        if index < 0 or index > self.length():
            raise DynamicArrayException
        if self.get_capacity() == self.length():
            self.resize(self.get_capacity() * 2)
        end_of_array = self.length() - 1                            #two pointers to the end of array and its new index
        new_end_of_array = self.length()
        while end_of_array >= index:                                #while loop continues til reach given index, copies
                                                                    #values up one spot
            self._data[new_end_of_array] = self._data[end_of_array]
            end_of_array -= 1
            new_end_of_array -= 1
        self._data[index] = value
        self._size += 1


    def remove_at_index(self, index: int) -> None:
        '''method that removes the value at given index and moves all the values down 1 spot'''
        if self.length() < self.get_capacity()*.25:
            if self.get_capacity() > 10 or self.length()*2 > 10:
                larger = None
                if self.length()*2 > 10:                              #when shrinking, cannot shrink array below 10
                    larger = self.length()*2
                else: larger = 10
                self.resize(larger)
        if index < 0 or index > (self.length() - 1):
            raise DynamicArrayException
        start = index
        end = index + 1
        while end != self.length():                                   #while loop to move everything down 1
            self._data[start] = self._data[end]
            start += 1
            end += 1
        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        '''method that returns a new DynamicArray that is all values in a given range'''
        if start_index < 0 or start_index >= self.length() or start_index+size > self.length() or size < 0:
            raise DynamicArrayException
        new_array = DynamicArray()
        for x in range (size):                          #for loop to append given slice to new_array
            new_array.append(self._data[start_index])
            start_index += 1
        return new_array


    def merge(self, second_da: "DynamicArray") -> None:
        '''method takes as input a DynamicArray and append all its elements to self'''
        for x in range(second_da.length()):
            self.append(second_da[x])

    def map(self, map_func) -> "DynamicArray":
        '''method takes a map_function and returns a new DynamicArray where every self's elements have the map function
        applied to it'''
        new_array = DynamicArray()
        for x in range(self.length()):
            new_array.append(map_func(self._data[x]))
        return new_array

    def filter(self, filter_func) -> "DynamicArray":
        '''method takes a filter function and returns a new DynamicArray with all of self's elements that pass the filter
        function'''
        new_array = DynamicArray()
        for x in range(self.length()):
            if filter_func(self._data[x]):                  #if statement to check if filter applies
                new_array.append(self._data[x])
        return new_array

    def reduce(self, reduce_func, initializer=None) -> object:
        '''method takes a reduce function, applies it to the Dynamic array, and returns the value'''
        if self.length() == 0:                              #if DynamicArray empty, return None/initializer
            return initializer
        if initializer == None:                             #if no initializer, the stored_value will be index[0] and
                                                            #we will start iterating through DA from index[1]
            stored_value = self._data[0]
            index = 1
        else:                                               #if there is an initializer, then we will begin iterating
                                                            #from DA[0]
            stored_value = initializer
            index = 0
        while index != self.length():
            stored_value = reduce_func(stored_value, self._data[index])
            index += 1
        return stored_value

def find_mode(arr: DynamicArray) -> (DynamicArray, int):
    '''function that takes a DynamicArray and returns a tuple of 1) a DynamicArray with all the modes, and 2) what
    the mode is aka the frequency'''
    output_array = DynamicArray()
    if arr.length() == 1:
        output_array.append(arr[0])
        return (output_array, 1)
    mode = 0
    new_mode = 0                                #var to keep track of the new mode when we are counting each new element
    index = 0
    current = arr[index]                        #var to keep track of what element we are currently counting
    while index <= arr.length() - 1:
        if arr[index] == current:               #if the element at index == current, then we +1 new_mode and continue
            new_mode += 1                       #iterating
            index += 1
        else:                                   #if it's not, then we know bc its sorted, then we check if it's the mode
            if new_mode > mode:                 #we have a higher mode, so we have to create a new output_array
                output_array = DynamicArray()
                output_array.append(current)
                mode = new_mode
                new_mode = 0
                current = arr[index]
            elif new_mode == mode:              #this case, we just append current to output_array
                output_array.append(current)
                new_mode = 0
                current = arr[index]
            else:                               #if it's not a mode, then we continue iterating
                current = arr[index]
                new_mode = 0
    if arr[arr.length()-1] == current:          #with the way above code is worded, we have to check the last element
        if new_mode > mode:                     #in the array and see if it is a mode
            output_array = DynamicArray()
            output_array.append(current)
            mode = new_mode
        elif new_mode == mode:
            output_array.append(current)
            new_mode = 0
    return (output_array, mode)





# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    print(da)
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# merge example 1")
    da = DynamicArray([1, 2, 3, 4, 5])
    da2 = DynamicArray([10, 11, 12, 13])
    print(da)
    da.merge(da2)
    print(da)

    print("\n# merge example 2")
    da = DynamicArray([1, 2, 3])
    da2 = DynamicArray()
    da3 = DynamicArray()
    da.merge(da2)
    print(da)
    da2.merge(da3)
    print(da2)
    da3.merge(da)
    print(da3)

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")

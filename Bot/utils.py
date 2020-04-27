import heapq


class DataStructure:

	def __init__(self):
		self.container = list()


	def __repr__(self): return str(self.container)


	def put(self, item):
		self.container.append(item)


	def empty(self):
		return len(self.container) == 0


class Queue(DataStructure):
	"""
	FIFO Policy Queue
	"""
	def get(self):
		item = self.container.pop(0)
		return item


class Stack(DataStructure):
	"""
	Stack LIFO Policy
	"""
	def get(self):
		item = self.container.pop()
		return item


class PriorityQueue(DataStructure):
	"""
	MinHeap:
	Each inserted item has a priority associated with it and the client 
	is usually interested in quick retrieval of the lowest-priority item 
	in the queue. This data structure allows O(1) access to the lowest-priority item.
	"""
	def __init__(self, priority_function):
		super(PriorityQueue, self).__init__()
		self.priority_function = priority_function
		self.count = 0


	def put(self, item):
		if not hasattr(item, 'pos'):
			raise ValueError('pos attribute not found for the item instance that you try to push')
		priority = self.priority_function(item.pos)
		item_heap = (priority, self.count, item)
		heapq.heappush(self.container, item_heap)
		self.count += 1


	def get(self):
		_, _, item = heapq.heappop(self.container)
		return item
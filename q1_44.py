# ~~~ This is a template for question 1  ~~~

#Imports:

###Part A###
#~~~  implementation of queue class  ~~~
class Node:
    def __init__(self, value):
        """
        A node in the linked list implementation of the queue.
        """
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        """
        Initialize an empty queue with head, tail, and size attributes.
        """
        self.head = None
        self.tail = None
        self.q_size = 0

    def front(self):
        """
        Return the value at the front of the queue without removing it.
        Raises IndexError if the queue is empty.
        """
        if self.empty():
            raise IndexError("front from empty queue")
        return self.head.value

    def empty(self):
        """
        Return True if the queue is empty, False otherwise.
        """
        return self.q_size == 0

    def enqueue(self, x):
        """
        Add a new element x to the end of the queue.
        """
        new_node = Node(x)
        if self.empty():
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.q_size += 1

    def dequeue(self):
        """
        Remove and return the element at the front of the queue.
        Raises IndexError if the queue is empty.
        """
        if self.empty():
            raise IndexError("dequeue from empty queue")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.q_size -= 1
        return value

###Part B###
def Was_an_attack(A, n, t):
    """
    Detects an "attack" in the sequence A.

    Parameters:
      - A: list of [type:str, timestamp:float] entries (unsorted).
      - n: int, minimum number of same-type requests in any window of length t.
      - t: float, size of the time window in seconds.

    First of all we check if A can have an attack by checking it's length.
    Then we sort A and the algorithm starts.
    We create an empty dictionary, then we loop through A, making each unique word a key in the dictionary, and the value a queue of all the requests.
    If a key already exist, we add the request to the queue.
    If the queue size is bigger than n, we check the front and tail to see if their difference is smaller than t.
    Otherwise, returning 0 if there's no attack.


    Returns:
      - [message:str, first_timestamp:float, first_type:str] on detection,
      - None if no attack is found.
    """

    # If fewer entries than required, no possible attack

    if len(A) < n:
        return 0

    # 1) Sort A by timestamp (O(N log N))
    A.sort(key=lambda x: x[1])

    windows = {}            # maps req_type.lower() → Queue of (ts, original_type)
    attacks = []            # will collect each time a new attack “starts”

    for req_type, ts in A:
        key = req_type.lower()
        if key not in windows:
            windows[key] = Queue()
        q = windows[key]

        # Remember how many were in the queue *before* enqueuing the new event:
        old_size = q.q_size

        # 2) enqueue the new event:
        q.enqueue((ts, req_type))

        # 3) Evict anything with timestamp < (ts - t):
        while (not q.empty()) and (q.front()[0] < ts - t):
            q.dequeue()

        # 4) If we have just gone from <n to ≥n, record it as a new attack:
        if old_size < n <= q.q_size:
            first_ts, first_type = q.front()
            msg = f"There was an attack on second {first_ts}"
            attacks.append([msg, first_ts, first_type])

    # 5) Return all detections, or 0 if none were found:
    return attacks if attacks else 0

A=[['Shelf',1.1], ['Shelf',10],  ['NEW USER',2.5],['sheLf',10], ['sheLf',10], ['SHeLF',10], ['Rating',5.9]]
result1 = Was_an_attack(A, 4, 5)
print(result1)

A=[['shelf',10],['shelf',5],['flower',1.76]]
result2 = Was_an_attack(A, 5, 5)
print(result2)
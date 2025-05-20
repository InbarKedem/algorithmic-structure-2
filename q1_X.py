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

    Returns:
      - [message:str, first_timestamp:float, first_type:str] on detection,
      - None if no attack is found.

    Raises:
      - TypeError or ValueError on invalid inputs.
    """
    # Validate inputs
    if not isinstance(A, list):
        raise TypeError("A must be a list of [type, timestamp] entries")
    if not A:
        raise ValueError("A must not be empty")
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n <= 0:
        raise ValueError("n must be positive")
    try:
        t = float(t)
    except (TypeError, ValueError):
        raise TypeError("t must be a number")
    if t <= 0:
        raise ValueError("t must be positive")

    # If fewer entries than required, no possible attack
    if len(A) < n:
        return 0

    # Parse and validate each entry
    events = []
    for entry in A:
        if not (isinstance(entry, (list, tuple)) and len(entry) == 2):
            raise ValueError("Each entry in A must be a list or tuple of length 2")
        req_type, ts = entry
        if not isinstance(req_type, str) or not req_type:
            raise ValueError("Request type must be a non-empty string")
        try:
            ts = float(ts)
        except (TypeError, ValueError):
            raise TypeError("Timestamp must be a number")
        events.append((req_type, ts))

    # Sort by timestamp (O(N log N))
    events.sort(key=lambda x: x[1])

    # Sliding windows per request type
    windows = {}
    for req_type, ts in events:
        key = req_type.lower()
        if key not in windows:
            windows[key] = Queue()
        q = windows[key]

        # Enqueue new event
        q.enqueue((ts, req_type))
        # Evict old events outside [ts - t, ts]
        while not q.empty() and q.front()[0] < ts - t:
            q.dequeue()
        # Check attack condition
        if q.q_size >= n:
            first_ts, first_type = q.front()
            msg = f"There was an attack on second {first_ts}"
            return [msg, first_ts, first_type]

    # No attack detected
    return 0


A=[['Shelf',1.1], ['Shelf',1.2], ['sheLf',1.3], ['sheLf',1.5], ['SHeLF',0.01], ['NEW USER',2.5], ['Rating',5.9]]
result1 = Was_an_attack(A, 5, 5)
print(result1)

A=[['shelf',10],['shelf',5],['flower',1.76]]
result2 = Was_an_attack(A, 5, 5)
print(result2)
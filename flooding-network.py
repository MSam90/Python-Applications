import copy
import threading


class Packet:
    """ This class represents the Packet to be transmitted in the network, while have the attributes of ttl, source, source_list,
     next_destination, final destination and execution time"""
    def __init__(self):     # Packet constructor which is initialized every time the object is created
        self.ttl = 11       # TTL value is always +1 due to the initialization of the network is done by receiving a packet at the source node
        self.source = 0     # Used to mark where the packet came from so the nodes dont transfer the packet back through the same path
        self.source_list = []   # Used for the solution so the nodes dont receive the packet twice and avoid repeating duplication
        self.final_destination = 14     # Notes the final node destination in the network
        self.next_destination = 0       # User to identify the next destination the packet will travel
        self.exec_time = 0              # Used to implement discrete time, while only using the link once every iteration

    def increment_exec_time(self):      # Used to change the execution time of the transfer in case the link is busy
        self.exec_time += 1

    def dec_ttl(self):                  # Decrements the ttl
        self.ttl -= 1

    def get_ttl(self):                  # Returns the ttl value of any packet object
        return self.ttl

    def get_source(self):               # Returns the node which the packet last travelled through
        return self.source

    def get_sources(self):              # Returns the identifier list of all the nodes the packet has travelled through
        return self.source_list

    def set_source(self, e):            # Used to change the source when travelling through a node
        self.source = e

    def reg_source(self, a):            # Used to add an identifier when travelling through a node in the solution
        self.source_list.append(a)

    def get_destination(self):          # Used to return the final destination
        return self.final_destination

    def set_destination(self, f):       # Used to set the final destination
        self.final_destination = f

    def set_next(self, a):              # Used to set the next hop in the network
        self.next_destination = a

    def get_next(self):                 # Used to find the next hop in the network
        return self.next_destination

    def set_exec_time(self, a):         # Used to change the execution time of the packet transmission
        self.exec_time = a

    def get_exec_time(self):            # Used to find the execution time of the packet transfer
        return self.exec_time


class Link:
    """ This class represents the Link between nodes and holds values of the status, Id and the connection """
    def __init__(self):
        self.status = False             # Used to identify whether the link is being used or not
        self.link_id = 0                # Used to identify the link being used
        self.linked_between = [] * 2    # Used to identify the nodes on both ends of the link
        self.packets_received = 0       # Used to identify how many packets have been received in the solution

    def set_status(self, d):            # Used to change the link status
        self.status = d

    def get_status(self):               # Returns the link status
        return self.status

    def set_link_id(self, e):           # Used to change or set the link id
        self.link_id = e

    def get_link_id(self):              # Returns the link id
        return self.link_id

    def set_connection(self, a):        # sets the connection on both ends of the node
        self.linked_between = a

    def get_target(self):               # Used to identify the receiving end of the link
        return self.linked_between[1]

    def get_source(self):               # Used to identify the sending end of the link
        return self.linked_between[0]

    def get_connection(self):           # Returns both ends of the link
        return self.linked_between


class Node:
    """ The class represent a node which is used to transmit and receive packets, with the attributes of Id, Packet queue
        links, a queue of duplicates, transmission completed (Done) and in case of the final_node destination (Packets received)"""
    def __init__(self):
        self.node_id = 0                # Used to identify a specific node
        self.nodeQueue = []             # Holds the packets waiting to be sent
        self.node_links = [] * 10       # Holds the links linked to other nodes
        self.duplicates = [] * 100      # Used for the duplication process
        self.done = False               # Used to check if all transmission are completed
        self.packets_received = 0       # Used to check how many packets the destination has received

    def set_node_id(self, a):           # Used to change a node id
        self.node_id = a

    def get_node_id(self):              # Returns the Id of the node
        return self.node_id

    def set_node_links(self, a):        # Used to add links to the node
        self.node_links.append(a)

    def get_node_links(self):           # Used to find the links of the node
        return self.node_links

    def get_node_link(self, a):         # Used to find a single link of the node
        return self.node_links[a]

    def print_queue(self):              # Used to print the queues at the node
        print('Queue at Node: ' + str(self.node_id) + ' = ' + str(len(self.nodeQueue)) + '\n')

    def add_queue(self, a):             # Used to add a packet to the node queue
        self.nodeQueue.append(a)

    def get_queue(self, a):             # Used to get a index specific packet from the queue
        return self.nodeQueue[a]

    def remove_queue(self, a):          # Used to remove a packet from the queue after transmission
        del self.nodeQueue[a]

    def get_all_queue(self):            # Used to return all of the queue, usually as size
        return self.nodeQueue

    def copy_packet(self, b, c):        # Used to duplicate a packet
        self.nodeQueue.append(copy.deepcopy(b))
        self.nodeQueue[-1].set_next(c)

    def increment_exec_time(self):      # Used to increment the execution time of a packet
        for x in range(len(self.nodeQueue)):
            self.nodeQueue[x].increment_exec_time()


class Network:
    """Used as a overall network to implement all objects functions with ease, the class attributes are, nodes, links,
        , destination_finder, internal_timer and total_packets"""
    def __init__(self):
        self.nodes = [Node()] * 15      # A list which holds all the nodes of the network used for iterative purposes
        self.links = [Link()] * 28      # A list which holds all the links of the network used for iterative purposes
        self.destination = 0            # A integer used to find the destination of the other link end
        self.internal_timer = 0         # Timer used to identify when a packet transmission is due
        self.total_packets = 0          # Used for a counter to identify how many packets are in the network

    def increment_time(self):                   # Used to increment the internal network timer
        self.internal_timer = self.internal_timer + 1

    def get_time(self):                         # Used to return the internal_timer
        return self.internal_timer

    def make_nodes(self):                       # Generates all the nodes in the network topology
        for mns in range(15):
            self.nodes[mns] = Node()            # Creates an Node object
            self.nodes[mns].set_node_id(mns)    # Sets the Node object Id

    def make_links(self):                       # Generates all the links used in the network topology
        for x in range(28):
            self.links[x] = Link()              # Creates a Link object
            self.links[x].set_link_id(x)        # Sets the Link object Id

    def make_connection(self, a, b, c):         # Used to define the link connection of the network topology
        self.links[a].linked_between = [b, c]   # Sets the connection of both ends of the link
        self.nodes[b].set_node_links(a)         # Adds the link to one side of the node
        self.nodes[c].set_node_links(a)         # Adds the link to the other side of the node

    def find_destination(self, a, x):           # Used to identify the sending and receiving side of the link
        if self.nodes[a].get_node_id() == self.links[self.nodes[a].get_node_link(x)].get_target():
            self.destination = self.links[self.nodes[a].get_node_link(x)].get_source()
        else:
            self.destination = self.links[self.nodes[a].get_node_link(x)].get_target()

        return self.destination

    def find_link(self, a, b):                  # Used to find the link that holds a specific connection between nodes
        for y in range(len(self.links)):
            if a in self.links[y].get_connection() and b in self.links[y].get_connection():
                z = self.links[y].get_link_id()
                return z

    def emtpy_queue_problem(self, a):           # Used to empty the queue in the problem part of the flooding network
        j = 0                                   # Used to iterate through the queue elements
        self.nodes[a].done = False              # Used to check if transmission is complete
        while len(self.nodes[a].get_all_queue()) > 0 and not self.nodes[a].done:    # While loop to execute while elements still in the queue
            try:                                                                    # Try catch statement to send packets if possible
                if self.nodes[a].get_queue(j).get_exec_time() == self.internal_timer:
                    confirm = self.send_problem(a, self.nodes[a].get_queue(j))      # Sends a packet and returns a confirmation
                    if confirm:                                                     # Removes the packet from the queue if confirmed
                        self.nodes[a].remove_queue(j)
                else:                                                               # Goes to the next packet in queue in case confirmation is false
                    j += 1

            except IndexError:                                                      # Avoids the index error when all elements have been checked
                self.nodes[a].done = True
                pass

    def emtpy_queue_solution(self, a):          # Used to empty the queue with the implemented solution of the network
        j = 0                                   # Works similar to the above function though the sending function is different
        self.nodes[a].done = False
        while len(self.nodes[a].get_all_queue()) > 0 and not self.nodes[a].done:
            try:
                if self.nodes[a].get_queue(j).get_exec_time() == self.internal_timer:
                    confirm = self.send_solution(a, self.nodes[a].get_queue(j))
                    if confirm:
                        self.nodes[a].remove_queue(j)
                else:
                    j += 1

            except IndexError:
                self.nodes[a].done = True
                pass

    def send_problem(self, a, b):           # Used to send the packets with the problem part of the flooding network
        if not b.get_next == b.get_source():    # Used to check if the next hop is the source based on the links of the node
            b.set_source(a)                     # Sets the source of the sending node
            c = self.find_link(self.nodes[a].get_node_id(), b.get_next())   # Finds the link for transmission
            if not self.links[c].get_status():                              # Checks if link is busy
                self.links[c].set_status(True)                              # Makes the link busy
                self.receive_problem(b.get_next(), b)                       # Receives at the other end of the link
                return True                                                 # Confirms that transmission was succesful
            elif self.links[c].get_status():                                # When the link is busy
                b.set_exec_time(self.internal_timer + 1)                    # Send packet next iteration
                return False                                                # Confirmation is false

    def send_solution(self, a, b):              # Works similar to above function with a minor difference
        if b.get_next not in b.get_sources():   # Checks through a list of nodes instead of a single node
            b.reg_source(a)
            c = self.find_link(self.nodes[a].get_node_id(), b.get_next())
            if not self.links[c].get_status():
                self.links[c].set_status(True)
                self.receive_solution(b.get_next(), b)      # The receiving function is different as well
                return True
            elif self.links[c].get_status():
                b.set_exec_time(self.internal_timer + 1)
                return False

    def receive_problem(self, a, b):                        # Used to receive packets at the other end of a link
        b.dec_ttl()                                         # Decrements the ttl upon receival
        if b.get_ttl() <= 0 and a == b.get_destination():   # Checks if packet has reached its life or destination
            self.nodes[a].packets_received += 1             # Increments the packets received
            del b                                           # Deletes the packet from the network
        elif b.get_ttl() <= 0:                              # Checks if the packet has reached its ttl
            del b                                           # Deletes the packet from the network

        elif self.nodes[a].get_node_id() == b.get_destination():    # Checks if packet has reached its destination
            self.nodes[a].packets_received += 1                     # Increments the received packets counter
            del b                                                   # Deletes the packet from the network

        else:
            if b.get_exec_time() == self.internal_timer:            # Checks if the packet has a current execution time
                b.set_exec_time(self.internal_timer + 1)            # Makes the packet time of execution the next iteration
                for x in range(len(self.nodes[a].get_node_links())):    # a for loop for all the links of the node
                    if not self.find_destination(self.nodes[a].get_node_id(), x) == b.get_source():     # Checks the packet last node place
                        self.nodes[a].copy_packet(b, self.find_destination(self.nodes[a].get_node_id(), x))     # Copies the packet for all the valid links

    def receive_solution(self, a, b):       # Similar to the above function with a minor change in conditions
        self.nodes[a].packets_received += 1
        b.dec_ttl()
        if b.get_ttl() <= 0 and a == b.get_destination():
            self.nodes[a].packets_received += 1
            del b
        elif b.get_ttl() <= 0:
            del b

        elif self.nodes[a].get_node_id() == b.get_destination():
            self.nodes[a].packets_received += 1
            del b

        else:
            if b.get_exec_time() == self.internal_timer:
                b.set_exec_time(self.internal_timer + 1)
                for x in range(len(self.nodes[a].get_node_links())):
                    if not self.find_destination(self.nodes[a].get_node_id(), x) in b.get_sources():    # Checks all the nodes the packet has travelled through
                        self.nodes[a].copy_packet(b, self.find_destination(self.nodes[a].get_node_id(), x))

    def init_network(self, a, b):   # Used to initialize the network at the desired source
        b.set_exec_time(self.internal_timer + 1)    # Sets the time of sending at the next iteration
        for x in range(len(self.nodes[a].get_node_links())):        # Applied to all the connected node links
            self.nodes[a].copy_packet(b, self.find_destination(self.nodes[a].get_node_id(), x))     # Queues a packet to be sent to the other link end

    def print_output(self):     # Used to print the Queues and the packets received at each iteration of time
        self.total_packets = 0
        for y in range(14):
            if y < 10:
                if len(self.nodes[y].get_all_queue()) < 10:
                    print('Node  ' + str(self.nodes[y].get_node_id()) + ' - Queue-Size:  ' +
                          str(len(self.nodes[y].get_all_queue())))
                    self.total_packets += len(self.nodes[y].get_all_queue())
                else:
                    print('Node  ' + str(self.nodes[y].get_node_id()) + ' - Queue-Size: ' +
                          str(len(self.nodes[y].get_all_queue())))
                    self.total_packets += len(self.nodes[y].get_all_queue())
            else:
                if len(self.nodes[y].get_all_queue()) < 10:
                    print('Node ' + str(self.nodes[y].get_node_id()) + ' - Queue-Size:  ' +
                          str(len(self.nodes[y].get_all_queue())))
                    self.total_packets += len(self.nodes[y].get_all_queue())
                else:
                    print('Node ' + str(self.nodes[y].get_node_id()) + ' - Queue-Size: ' +
                          str(len(self.nodes[y].get_all_queue())))
                    self.total_packets += len(self.nodes[y].get_all_queue())

        print('Node ' + str(Net.nodes[14].get_node_id()) + ' - Packets Received: ' + str(
            Net.nodes[14].packets_received))
        print('Total Packets in the Network: ' + str(self.total_packets))

    def clear_all(self):        # Used to clear all the queues of all nodes
        for n in range(len(self.nodes)):
            self.nodes[n].nodeQueue.clear()
        self.nodes[14].packets_received = 0
        self.internal_timer = 0

    def print_topology(self):
        print("***************   Topology    **************")
        for pn in range(len(self.nodes)):
            print("Node: " + str(self.nodes[pn].get_node_id()) + " Links" + str(self.nodes[pn].get_node_links()))

        print("************   End of Topology  ************\n")
        print("NOTE!!!: Two runs will occur one simulating the problem the second the solution \n")


""" Creates the network topology and makes all the connections of the network"""
Net = Network()
Net.make_nodes()
Net.make_links()
Net.make_connection(0, 0, 1)
Net.make_connection(1, 0, 4)
Net.make_connection(2, 0, 2)
Net.make_connection(3, 1, 3)
Net.make_connection(4, 1, 4)
Net.make_connection(5, 2, 4)
Net.make_connection(6, 2, 5)
Net.make_connection(7, 3, 4)
Net.make_connection(8, 4, 5)
Net.make_connection(9, 3, 6)
Net.make_connection(10, 4, 6)
Net.make_connection(11, 4, 8)
Net.make_connection(12, 4, 7)
Net.make_connection(13, 5, 7)
Net.make_connection(14, 6, 9)
Net.make_connection(15, 6, 8)
Net.make_connection(16, 7, 8)
Net.make_connection(17, 7, 10)
Net.make_connection(18, 8, 11)
Net.make_connection(19, 9, 12)
Net.make_connection(20, 9, 11)
Net.make_connection(21, 10, 11)
Net.make_connection(22, 10, 13)
Net.make_connection(23, 11, 12)
Net.make_connection(24, 11, 14)
Net.make_connection(25, 11, 13)
Net.make_connection(26, 12, 14)
Net.make_connection(27, 13, 14)

Net.print_topology()

pct_problem = Packet()                  # Makes a new packet to be transmitted
Net.init_network(0, pct_problem)     # Puts a packet in the Source node which at once decrements the ttl hence +1

threads = []                            # A list which holds all the threads executed

print('\n**********   Network No  Solution    **********\n')
for run in range(12):                # Runs from 0 - 11 which is the discrete time

    Net.internal_timer = run
    print('\n**********       Time:  ' + str(Net.internal_timer) + '            **********\n')
    if run % 2 == 0:                                        # Gives the nodes from 0 - 14 the priority in incrementing order
        for i in range(15):
            if len(Net.nodes[i].get_all_queue()) > 0:        # Executes if packets in the queue
                try:
                    t = threading.Thread(target=Net.emtpy_queue_problem, args=(i,))     # Defines the thread
                    threads.append(t)                                                   # Adds the thread to the Threads list
                    t.start()                                                           # Starts the thread
                except threading:
                    print('Threading Error')

        Net.print_output()

    elif run % 2 == 1:                                       # Gives the nodes from 14 - 0 the priority in decrementing order
        for i in reversed(range(15)):
            if len(Net.nodes[i].get_all_queue()) > 0:        # Executes if packets in the queue
                try:
                    t = threading.Thread(target=Net.emtpy_queue_problem, args=(i,))     # Defines the thread
                    threads.append(t)                                                   # Adds the thread to the Threads list
                    t.start()                                                           # Starts the thread
                except threading:
                    print('Threading Error')

        Net.print_output()

    for z in range(len(Net.links)):                         # Reinitialize the links to false after the iteration
        Net.links[z].set_status(False)

print('\n\n**********       End  Of  Run        **********\n\n')

Net.clear_all()     # Clears all the network
threads.clear()     # Clears all the threads
print('\n**********   Network Run  Solution   **********\n')
pct_solution = Packet()     # Creates a new packet object
pct_solution.ttl = 4        # Sets the packet objects ttl 4, the network diameter based on the topology
Net.init_network(0, pct_solution)   # Puts the packet in the node 0 for initialization of the network

for run in range(12):       # Runs from 0 - 11 which is the discrete time

    Net.internal_timer = run
    print('\n**********       Time:  ' + str(Net.internal_timer) + '            **********\n')
    if run % 2 == 0:                                    # Gives the nodes from 0 - 14 the priority in incrementing order
        for i in range(15):
            if len(Net.nodes[i].get_all_queue()) > 0:   # Executes if packets in the queue
                try:
                    t = threading.Thread(target=Net.emtpy_queue_solution, args=(i,))    # Defines the thread
                    threads.append(t)                                                   # Adds the thread to the Threads list
                    t.start()                                                           # Starts the thread
                except threading:
                    print('Threading Error')

        Net.print_output()

    elif run % 2 == 1:                                  # Gives the nodes from 14 - 0 the priority in the decrementing order
        for i in reversed(range(15)):
            if len(Net.nodes[i].get_all_queue()) > 0:   # Executes if packets in the queue
                try:
                    t = threading.Thread(target=Net.emtpy_queue_solution, args=(i,))    # Defines the thread
                    threads.append(t)                                                   # Adds the thread to the Threads list
                    t.start()                                                           # Starts the thread
                except threading:
                    print('Threading Error')

        Net.print_output()

    for z in range(len(Net.links)):                     # Reinitialize the links to false after the iteration
        Net.links[z].set_status(False)


print('\n\n**********       End  Of  Run        **********\n\n')


# Used to identify that packet have been received at all of networks nodes
for pr in range(1, len(Net.nodes)):
    print("Node: " + str(Net.nodes[pr].get_node_id()) + " Received: " + str(Net.nodes[pr].packets_received) + " Packets")
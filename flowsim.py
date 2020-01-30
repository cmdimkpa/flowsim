# Control Algorithm Simulation

from __future__ import division
import datetime
from random import random

def now():
    return datetime.datetime.today()

def elapsed(t):
    return (now() - t).seconds

def average(array):
    if array:
        if len(array) > 0:
            return sum(array)/len(array)
        else:
            return 0
    else:
        return 0

# Constants
maxCars = 1000
maxSimulations = 2
simulationSeconds = 60
Thresholds = {
    "CR":0.6
}

class FlowQueue:
    def __init__(self):
        self.cars = []
        self.last_closed = None
        self.isOpen = False
        self.total_inflow = 0
        self.total_outflow = 0
        self.data = {
            "cr":[],
            "opened":0,
            "closed":0
        }
    def size(self):
        return len(self.cars)
    def cr(self):
        # store and return Congestion Ratio
        if self.size() > 0:
            _cr = self.size() / maxCars
        else:
            _cr = 0
        self.data["cr"].append(_cr)
        return average(self.data["cr"])
    def inflow(self):
        # cannot inflow more than capacity of queue
        if self.size() < maxCars:
            # add new car
            self.cars.append(self.size()+1)
            # increment total inflow
            self.total_inflow+=1
    def outflow(self):
        # outflow is only possible if flow queue is open
        if self.isOpen and self.size()>0:
            # pop car from queue
            self.cars.pop()
            # increment total outflow
            self.total_outflow+=1
    def open(self):
        if not self.isOpen:
            self.data["opened"]+=1
        # open flow queue
        self.isOpen = True
    def close(self):
        if self.isOpen:
            self.data["closed"]+=1
        # close flow queue
        self.isOpen = False
        # log last closed
        self.last_closed = now()

# Simulation Relay
for sim in range(maxSimulations):
    # 1. create Flow Queues
    Flow1 = FlowQueue()
    Flow2 = FlowQueue(); Flow2.open()  # Open Flow2 at the start (principal flow)
    Flow3 = FlowQueue()
    # 2. start global relay
    relayStarted = now()
    while elapsed(relayStarted) < simulationSeconds:

        # probabilistic inflow
        if random() > 0.5:
            Flow1.inflow()
        if random() > 0.5:
            Flow2.inflow()
        if random() > 0.5:
            Flow3.inflow()

        # probabilistic outflow
        if random() > 0.5:
            Flow1.outflow()
        if random() > 0.5:
            Flow2.outflow()
        if random() > 0.5:
            Flow3.outflow()

        # Apply Flow Rules: Conditional CLOSE of Flow2 / OPEN Flow1 & Flow3
        if Flow1.cr() > Thresholds["CR"] or Flow3.cr() > Thresholds["CR"]:
            Flow2.close()
            Flow1.open()
            Flow3.open()
        else:
            Flow2.open()
            Flow1.close()
            Flow3.close()

        # update Flow2
        Flow2.cr()

    # report findings
    print("")
    print("SIM %s of %s: Flow1 total inflow = %s" % (sim+1, maxSimulations, Flow1.total_inflow))
    print("SIM %s of %s: Flow1 total outflow = %s" % (sim+1, maxSimulations, Flow1.total_outflow))
    print("SIM %s of %s: Flow1 left on queue = %s" % (sim+1, maxSimulations, Flow1.total_inflow - Flow1.total_outflow))
    print("SIM %s of %s: Flow1 average CR = %s" % (sim+1, maxSimulations, average(Flow1.data["cr"])))
    print("SIM %s of %s: Flow1 times opened = %s" % (sim+1, maxSimulations, Flow1.data["opened"]))
    print("SIM %s of %s: Flow1 times closed = %s" % (sim+1, maxSimulations, Flow1.data["closed"]))
    print("")
    print("SIM %s of %s: Flow2 total inflow = %s" % (sim+1, maxSimulations, Flow2.total_inflow))
    print("SIM %s of %s: Flow2 total outflow = %s" % (sim+1, maxSimulations, Flow2.total_outflow))
    print("SIM %s of %s: Flow2 left on queue = %s" % (sim+1, maxSimulations, Flow2.total_inflow - Flow2.total_outflow))
    print("SIM %s of %s: Flow2 average CR = %s" % (sim+1, maxSimulations, average(Flow2.data["cr"])))
    print("SIM %s of %s: Flow2 times opened = %s" % (sim+1, maxSimulations, Flow2.data["opened"]))
    print("SIM %s of %s: Flow2 times closed = %s" % (sim+1, maxSimulations, Flow2.data["closed"]))
    print("")
    print("SIM %s of %s: Flow3 total inflow = %s" % (sim+1, maxSimulations, Flow3.total_inflow))
    print("SIM %s of %s: Flow3 total outflow = %s" % (sim+1, maxSimulations, Flow3.total_outflow))
    print("SIM %s of %s: Flow3 left on queue = %s" % (sim+1, maxSimulations, Flow3.total_inflow - Flow3.total_outflow))
    print("SIM %s of %s: Flow3 average CR = %s" % (sim+1, maxSimulations, average(Flow3.data["cr"])))
    print("SIM %s of %s: Flow3 times opened = %s" % (sim+1, maxSimulations, Flow3.data["opened"]))
    print("SIM %s of %s: Flow3 times closed = %s" % (sim+1, maxSimulations, Flow3.data["closed"]))

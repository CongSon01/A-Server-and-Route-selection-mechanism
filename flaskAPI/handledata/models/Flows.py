class Flows(object):
    """ Flows array holds each Flow object"""

    def __init__(self):
        self.flows = []

    def set_flows(self, flow_object):
        self.flows.append( flow_object)

    def get_flows(self):
        return self.flows


    


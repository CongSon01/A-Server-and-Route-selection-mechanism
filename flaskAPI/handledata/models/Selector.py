class Selector(object):
    """Selector array holds each Criteria object"""

    def __init__(self):
        self.criterias = []

    def set_criterias(self, criteria_object):
        self.criterias.append( criteria_object)

    def get_criterias(self):
        return self.criterias



class Flow(object):

    def __init__(self, priority, timeout, isPermanent, deviceId):
        '''
        priority, timeout: int
        isPermanent: boolean
        deviceId: string
        treament: Treatment object
        selector: Selector object
        '''
        self.priority = priority
        self.timeout = timeout
        self.isPermanent = isPermanent
        self.deviceId = deviceId
        self.treatment = ""
        self.selector = ""

    def set_treatment(self, treatment_object):
        self.treatment = treatment_object

    def set_selector(self, selector_object):
        self.selector = selector_object

    def get_priority(self):
        return self.priority
    
    def get_timeout(self):
        return self.timeout

    def get_isPermanent(self):
        return self.isPermanent

    def get_deviceId(self):
        return self.deviceId

    def get_treatment(self):
        return self.treatment

    def get_selector(self):
        return self.selector

    

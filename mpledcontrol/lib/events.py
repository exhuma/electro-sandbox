class Event(object):
    pass


class StateChange(Event):

    def __init__(self, new_value):
        self.new_value = new_value

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self.new_value)


class MonitorStateChange(StateChange):
    pass


class ButtonStateChange(StateChange):
    pass

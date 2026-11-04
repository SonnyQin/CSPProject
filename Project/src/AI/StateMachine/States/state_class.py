class State:
    def __init__(self):
        pass
    #virtual
    def Enter(self, owner):
        if not owner:
            return
    def Execute(self, owner):
        if not owner:
            return
    def Exit(self, owner):
        if not owner:
            return
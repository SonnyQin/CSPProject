from AI.StateMachine.States.state_class import State

class EnemyGlobalState(State):
    def __init__(self):
        super().__init__()
    def Enter(self, owner):
        super().Enter(owner)
    def Execute(self, owner):
        super().Execute(owner)
    def Exit(self, owner):
        super().Exit(owner)

    @staticmethod
    def get_instance():
        if EnemyGlobalState._Instance is None:
            EnemyGlobalState._Instance = EnemyGlobalState()
        return EnemyGlobalState._Instance
    _Instance = None

#default
class EnemyWanderState(State):
    def __init__(self):
        super().__init__()
    def Enter(self, owner):
        super().Enter(owner)
        #owner.mSteeringBehaviors.WanderOn()
        owner.mSteeringBehaviors.SeekOn()
        #owner.mSteeringBehaviors.PursuitOn()
    def Execute(self, owner):
        super().Execute(owner)
    def Exit(self, owner):
        super().Exit(owner)
        #owner.mSteeringBehaviors.WanderOff()
        owner.mSteeringBehaviors.SeekOff()
        #owner.mSteeringBehaviors.PursuitOff()

    @staticmethod
    def get_instance():
        if EnemyWanderState._Instance is None:
            EnemyWanderState._Instance = EnemyWanderState()
        return EnemyWanderState._Instance
    _Instance = None

#Chase Player
class EnemyChaseState(State):
    def __init__(self):
        super().__init__()
    def Enter(self, owner):
        super().Enter(owner)
        owner.mSteeringBehaviors.PursuitOn()
    def Execute(self, owner):
        super().Execute(owner)
    def Exit(self, owner):
        super().Exit(owner)
        owner.mSteeringBehaviors.PursuitOff()

    @staticmethod
    def get_instance():
        if EnemyChaseState._Instance is None:
            EnemyChaseState._Instance = EnemyChaseState()
        return EnemyChaseState._Instance
    _Instance = None

#Received Attack from player, flee away from  the Rocket
class EnemyEvadeState(State):
    def __init__(self):
        super().__init__()
    def Enter(self, owner):
        super().Enter(owner)
        owner.mSteeringBehaviors.EvadeOn()
    def Execute(self, owner):
        super().Execute(owner)
    def Exit(self, owner):
        super().Exit(owner)
        owner.mSteeringBehaviors.EvadeOff()

    @staticmethod
    def get_instance():
        if EnemyEvadeState._Instance is None:
            EnemyEvadeState._Instance = EnemyEvadeState()
        return EnemyEvadeState._Instance
    _Instance = None
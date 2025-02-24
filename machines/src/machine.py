from dataclasses import dataclass
from enum import StrEnum
import random
import time

class MachineState(StrEnum):
    IDLE = "idle"
    WASHING = "washing"
    FINISHED = "finished"
    RESERVED = "reserved"

# constants for machine type
class MachineType(StrEnum):
    WASHER = "washer"
    DRYER = "dryer"

@dataclass
class Machine:
    id: int
    state: MachineState
    type: MachineType
    will_reserve: bool
    state_init_time: int

def unixTime():
    return int(time.time())

def randomEnum(enum):
    return random.choice(list(enum))

def create_random_machine(id: int, type: MachineType) -> Machine:
    return Machine(
        id=id,
        state=randomEnum(MachineState),
        type=type,
        will_reserve=False,
        state_init_time=unixTime()
    )

def create_default_machine(id: int) -> Machine:
    return Machine(
        id=id,
        state=MachineState.IDLE,
        type=MachineType.WASHER,
        will_reserve=False,
        state_init_time=unixTime()
    )

def createId():
    return random.randint(0, 1000) 

def update(m: Machine):
    if m.state == MachineState.WASHING:
        if unixTime() - m.state_init_time > (30 * 60): #30 minutes in seconds
            m.state = MachineState.FINISHED
            m.state_init_time = unixTime()
    elif m.state == MachineState.FINISHED:
        if unixTime() - m.state_init_time > (5 * 60) and random.randint(0, 1) == 1: #random unload time
            if m.will_reserve:
                m.state = MachineState.RESERVED
                m.will_reserve = False
            else:
                m.state = MachineState.IDLE
            m.state_init_time = unixTime()
    elif m.state == MachineState.RESERVED:
        if unixTime() - m.state_init_time > (10 * 60):
            m.state = MachineState.IDLE
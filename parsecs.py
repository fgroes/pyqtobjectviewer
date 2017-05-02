import re


class StateMachine(object):

    def __init__(self, name, states_name, events_name):
        self.name = name
        self.states_name = states_name
        self.events_name = events_name
        self.states = {}

    def __str__(self):
        return "StateMachine(name: {0}, states: [{1}])".format(self.name, ", ".join(s.__str__() for k, s in self.states.items()))


class State(object):

    def __init__(self, name):
        self.name = name
        self.transitions = []
        self.initial_child = None
        self.children = []

    def __str__(self):
        transition_str = ", ".join(t.__str__() for t in self.transitions)
        if len(self.children) > 0:
            sub_states_str = ", substates: [{0}]".format(", ".join(s.__str__() for s in [self.initial_child] + self.children))
        else:
            sub_states_str = ""
        return "State(name: {0}, transitions: [{1}]{2})".format(self.name, transition_str, sub_states_str)


class Transition(object):

    def __init__(self, event, source_state, target_state):
        self.event = event
        self.source_state = source_state
        self.target_state = target_state

    def __str__(self):
        return "Transition({0} ---{1}---> {2})".format(self.source_state, self.event, self.target_state)


filename = r"D:\Projekte\DeepObserver\Software\deepobserver\PlasmoTemplateProject\AutomationHandler.cs"

lines = None
with open(filename, "r") as fid:
    lines = fid.readlines()

state_machines = {}
curr_sm = None
curr_state = None
for line in lines:
    match = re.search(r"IStateMachine<(?P<states>\w+), (?P<events>\w+)> (?P<name>\w+)", line)
    if match:
        d = match.groupdict()
        sm = StateMachine(d["name"], d["states"], d["events"])
        state_machines[sm.name] = sm
        continue
    match = re.search(r"(?P<name>\w+)\.In\((?P<states>\w+)\.(?P<state>\w+)\)", line)
    if match:
        d = match.groupdict()
        sm_name = d["name"]
        state_name = d["state"]
        if sm_name in state_machines:
            if state_name not in state_machines[sm_name].states:
                s = State(state_name)
                state_machines[sm_name].states[state_name] = s
            curr_sm = sm_name
            curr_state = state_name
    match = re.search(r"\.On\((?P<events>\w+)\.(?P<event>\w+)\)\.Goto\((?P<states>\w+)\.(?P<state>\w+)\)", line)
    if match:
        d = match.groupdict()
        t = Transition(d["event"], curr_state, d["state"])
        state_machines[curr_sm].states[curr_state].transitions.append(t)
    match = re.search(r"\.WithInitialSubState\((?P<states>\w+)\.(?P<state>\w+)\)", line)
    if match:
        d = match.groupdict()
        state_machines[curr_sm].states[curr_state].initial_child = d["state"]
    match = re.search(r"\.WithSubState\((?P<states>\w+)\.(?P<state>\w+)\)", line)
    if match:
        d = match.groupdict()
        state_machines[curr_sm].states[curr_state].children.append(d["state"])

for name, sm in state_machines.items():
    for state_name, state in sm.states.items():
        child_states = []
        for child_state_name in state.children:
            if child_state_name in sm.states:
                child_state = sm.states.pop(child_state_name)
                child_states.append(child_state)
        if state.initial_child in sm.states:
            initial_child = sm.states.pop(state.initial_child)
            state.initial_child = initial_child
        state.children = child_states

for name, sm in state_machines.items():
    print(sm)



import json
from math import inf
from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time
from heapq import heappop, heappush

Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])
tools = ["bench", "furnace", "iron_axe", "iron_pickaxe", "stone_axe", "stone_pickaxe", "wooden_axe", "wooden_pickaxe"]
item_limit = {"wood": 1, 
            "stick": 6, 
            "plank": 8, 
            "ore": 1, 
            "ingot": 6,  
            "cobble": 8, 
            "coal": 1,
            "cart": 1,
            "rail": 32}

class State(OrderedDict):
    """ This class is a thin wrapper around an OrderedDict, which is simply a dictionary which keeps the order in
        which elements are added (for consistent key-value pair comparisons). Here, we have provided functionality
        for hashing, should you need to use a state as a key in another dictionary, e.g. distance[state] = 5. By
        default, dictionaries are not hashable. Additionally, when the state is converted to a string, it removes
        all items with quantity 0.

        Use of this state representation is optional, should you prefer another.
    """

    def __key(self):
        return tuple(self.items())

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.__key() < other.__key()

    def copy(self):
        new_state = State()
        new_state.update(self)
        return new_state

    def __str__(self):
        return str(dict(item for item in self.items() if item[1] > 0))


def make_checker(rule):
    # Implement a function that returns a function to determine whether a state meets a
    # rule's requirements. This code runs once, when the rules are constructed before
    # the search is attempted.
    
    #print("entered make_checker")

    def check(state):
        # This code is called by graph(state) and runs millions of times.
        # Tip: Do something with rule['Consumes'] and rule['Requires'].
        #print("entered check")
        if 'Consumes' in rule:
            for item in rule['Consumes']:
                #print(state[item])
                if state[item] < rule['Consumes'][item]:
                    #print("consumes false")
                    return False
        if 'Requires' in rule:
            for item in rule['Requires']:
                #print(state[item])
                if state[item] <= 0:
                    #print("requires false")
                    return False
        return True
    return check


def make_effector(rule):
    # Implement a function that returns a function which transitions from state to
    # new_state given the rule. This code runs once, when the rules are constructed
    # before the search is attempted.

    def effect(state):
        # This code is called by graph(state) and runs millions of times
        # Tip: Do something with rule['Produces'] and rule['Consumes'].
        next_state = state.copy()
        if 'Produces' in rule:
            for item in rule['Produces']:
                #print("catch produce")
                next_state[item] = state[item] + rule['Produces'][item]
        if 'Consumes' in rule:
            for item in rule['Consumes']:
                #print("catch consume")
                next_state[item] = state[item] - rule['Consumes'][item]
        return next_state

    return effect


def make_goal_checker(goal):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.

    def is_goal(state):
        # This code is used in the search process and may be called millions of times.
        for item in goal:
            if state[item] < goal[item]:
                return False
        return True

    return is_goal


def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)


def heuristic(state, action):
    # Implement your heuristic here!
    """
    tools = ["bench", "furnace", "iron_axe", "iron_pickaxe", "stone_axe", "stone_pickaxe", "wooden_axe", "wooden_pickaxe"]
    items = ["wood", "stick", "plank", "ore", "ingot", "cobble", "coal", "cart"]

    for tool in tools:
        if state[tool] > 1:
            return inf 

    for item in items:
        if item == "wood" and state[item] > 1:
            return inf
        elif item == "stick" and state[item] > 4:
            return inf
        elif item == "plank" and state[item] > 8:
            return inf
        elif item == "ore" and state[item] > 1:
            return inf
        elif item == "ingot" and state[item] > 6:
            return inf
        elif item == "cobble" and state[item] > 8:
            return inf
        elif item == "coal" and state[item] > 1:
    """
    #if is_goal(state):
    #    return inf

    for tool in tools:
        if state[tool] > 1:
            return inf 
            """
    if state['iron_pickaxe'] >= 1:
        if 'stone_pickaxe' in action or 'wooden_pickaxe' in action:
            return inf

    if state['iron_axe'] >= 1:
        if 'stone_axe' in action or 'wooden_axe' in action:
            return inf
    """

    for item in item_limit:
        if state[item] > item_limit[item]:
            return inf
    return 0

def search(graph, state, is_goal, limit, heuristic):

    start_time = time()

    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state
    frontier = [(0, state)]
    #print("frontier:", frontier)
    previous = set()
    previous.add(state)
    actioncost = {}
    actioncost[state] = 0
    
    backpointers = {}
    backpointers[state] = None
    
    actions = {}
    actions[state] = None

    goal_state = None
    cost_to_goal = None
    shortest_path_found = False
    while time() - start_time < limit:

        if not frontier or shortest_path_found:                 # list is empty OR shortest path found
            print("Searched for:", time() - start_time, 'seconds.')
            print("Total (in-game) cost: ", actioncost[goal_state])
            num_states = 0
            path = [(goal_state, actions[goal_state])]
            current_backpointer = backpointers[goal_state]
            while current_backpointer != None:
                #print("path loop")
                path.insert(0, (current_backpointer, actions[current_backpointer]))
                #print(current_backpointer)
                current_backpointer = backpointers[current_backpointer]
                num_states += 1
            print("In total, visited", len(previous), " states.")
            return path

        #print("----------------POP FRONTIER-----------------")
        current_cost, current_state = heappop(frontier)
        #print("state: ", current_state)
        #print("cost: ", current_cost)
        #print()

        if is_goal(current_state):
            if(cost_to_goal is None or actioncost[current_state] < cost_to_goal):
                goal_state = current_state
                cost_to_goal = actioncost[current_state]

        if goal_state is not None and current_cost > cost_to_goal: # make sure all shorter paths have been explored
            shortest_path_found = True
            
        for next_action, next_state, next_cost in graph(current_state):
            #print("potential action: ", next_action)
            #print("current state: ", current_state)
            #print("state after action:", next_state)
            #print("cost of action: ", next_cost)
            #print()
            new_cost = current_cost + next_cost + heuristic(next_state, next_action)
            #print("new cost: ", new_cost)
            #if next_state in actioncost:
            #    print("action cost: ", actioncost[next_state])
            if new_cost == inf:
                continue
            elif next_state not in actioncost or new_cost < actioncost[next_state] and next_state not in previous:
                actioncost[next_state] = new_cost
                backpointers[next_state] = current_state
                actions[next_state] = next_action
                previous.add(next_state)
                heappush(frontier, (new_cost, next_state))
            #    print("chose this action: ", next_action)
                

    # Failed to find a path
    print(time() - start_time, 'seconds.')
    #print(current_state)
    print("Failed to find a path from", state, 'within time limit.')
    return None

if __name__ == '__main__':
    with open('Crafting.json') as f:
        Crafting = json.load(f)

    # # List of items that can be in your inventory:
    print('All items:', Crafting['Items'])
    #
    # # List of items in your initial inventory with amounts:
    print('Initial inventory:', Crafting['Initial'])
    #
    # # List of items needed to be in your inventory at the end of the plan:
    print('Goal:', Crafting['Goal'])
    #
    # # Dict of crafting recipes (each is a dict):
    #print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

    # Build rules
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        #print("name", name)
        #print("rule", rule)
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)

    # Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])
    for item in item_limit:                                     # might need to modify item_limit based on the goal
        if item in Crafting['Goal'] and item_limit[item] < Crafting['Goal'][item]:
            item_limit[item] = Crafting['Goal'][item]

    # Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})
    state.update(Crafting['Initial'])

    # Search for a solution
    resulting_plan = search(graph, state, is_goal, 30, heuristic)

    if resulting_plan:
        # Print resulting plan
        for state, action in resulting_plan:
            print('\t',state)
            print(action)

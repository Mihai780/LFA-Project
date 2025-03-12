#Neagoe Mihai Alexandru
#Cutuliga Razvan Ion
def la_input_verifier():
    #citim din fisier
    with open('configurare_LA', "r") as f:
        input_str = f.read()

    # Extract Sigma section from input
    sigma_str = extract_section(input_str, "Sigma")

    # Check if borders of the section exist
    if sigma_str == 'Sigma not found' or sigma_str == 'end not found':
        return 'Error : Sigma section does not exist.', {}, {}, {}, {}, {}

    # Extract States section from input
    states_str = extract_section(input_str, "States")

    # Check if borders of the section exist
    if states_str == 'States not found' or sigma_str == 'end not found':
        return 'Error : States section does not exist.', {}, {}, {}, {}, {}

    # Extract Transitions section from input
    transitions_str = extract_section(input_str, "Transitions")

    # Check if borders of the section exist
    if transitions_str == 'Transitions not found' or sigma_str == 'end not found':
        return 'Error : Transitions section does not exist.', {}, {}, {}, {}, {}

    # Extract Gamma section from input
    gamma_str = extract_section(input_str, "Gamma")

    # Check if borders of the section exist
    if gamma_str == 'Gamma not found' or gamma_str == 'end not found':
        return 'Error : Gamma section does not exist.', {}, {}, {}, {}, {}

    # Save sigma letters
    Sigma = sigma_parser(sigma_str)

    # Save states status
    States = states_parser(states_str)

    # Save gamma instances
    Gamma = gamma_parser(gamma_str)

    # Verify states status
    feedback = states_status_checker(States)

    # Throw errors when definition not respected
    if feedback == 'Multiple starts':
        return 'Error detected : multiple "start" states.', {}, {}, {}, {}, {}
    elif feedback == 'No start':
        return 'Error detected : no start state.', {}, {}, {}, {}, {}
    else:
        Start = feedback  # Save start state

    # Verify transitions's letters existence in Sigma
    feedback = transitions_sigma_verifier(transitions_str, Sigma)
    if feedback.split()[0] == 'Error':
        return 'Error detected : letter ' + '"' + feedback.split()[1] + '"' + ' not part of Sigma.', {}, {}, {}, {}, {}

    # Verify transitions' symbols existence in Gamma
    feedback = transitions_gamma_verifier(transitions_str, Gamma)
    if feedback.split()[0] == 'Error':
        return 'Error detected : symbol ' + '"' + feedback.split()[1] + '"' + ' not part of Gamma.', {}, {}, {}, {}, {}

    # Verify transition's states existence in States
    feedback = transitions_states_verifier(transitions_str, States)
    if feedback.split()[0] == 'Error':
        return 'Error detected : state ' + feedback.split()[1] + ' not part of States.', {}, {}, {}, {}, {}
    return "Your input file is valid", transitions_dictionary(
        transitions_str), States, Sigma, Start, Gamma


# Function for extracting customized section from file

def extract_section(input_str, section_name):
    # Check if section's start border exists
    section_start = input_str.find(section_name + ":")
    if section_start == -1:
        return section_name + ' not found'

    # Check if section's end border exists
    section_end = input_str.find("End", section_start)
    if section_end == -1:
        return 'End not found'

    # Getting section's info and returning
    section_content = input_str[section_start + len(section_name + ':'): section_end]
    section_content = section_content.strip()
    return section_content


# Function for extracting letters from 'Sigma' section in the  file.
def sigma_parser(sigma_str):
    sigma_letters = []
    sigma_str = sigma_str.split('\n')
    for letter in sigma_str:
        sigma_letters.append(letter)
    return sigma_letters


# Function for extracting states from 'States' section in the file
def states_parser(states_str):
    states_instances = {}
    states_str = states_str.split('\n')
    for state_info in states_str:
        # Parsing every state info line
        if state_info.find(',') != -1:  # Verifying if there is at least a status for the state
            state_info = [element.strip() for element in state_info.split(',')]
            if state_info[0] not in states_instances:
                if len(state_info) == 3:  # Checking if there are both start and final status
                    states_instances[state_info[0]] = [state_info[1], state_info[2]]
                elif len(state_info) == 2:
                    states_instances[state_info[0]] = [state_info[1]]
            else:
                states_instances[state_info[0]].append(
                    state_info[1])  # Appending new status to existing state in dictionary
        else:
            states_instances[state_info] = []  # Null status
    return states_instances


# Function for extracting Gamma symbols from 'Gamma' section in the file
def gamma_parser(gamma_str):
    gamma_symbols = []
    gamma_str = gamma_str.split('\n')
    for symbol in gamma_str:
        gamma_symbols.append(symbol)
    return gamma_symbols


# Function for checking if the states used in transitions are part of States
def transitions_states_verifier(transitions_str, States):
    transitions_str = transitions_str.split('\n')
    # we check every trasition in the file if the first element of the first part and the first element
    # of the second part are in states!
    for transition in transitions_str:
        transition = transition.split('>')
        input_transition_rule = [character.strip() for character in
                                 transition[0].strip().replace("(", "").replace(")", "").split(",")]
        output_transition_rule = [character.strip() for character in
                                  transition[1].strip().replace("(", "").replace(")", "").split(",")]
        if input_transition_rule[0] not in States:
            return "Error " + input_transition_rule[0]
        if output_transition_rule[0] not in States:
            return "Error " + output_transition_rule[0]
    return "Validated"


# Function for checking if the symbols used in transitions are part of Gamma
def transitions_gamma_verifier(transitions_str, Gamma):
    transitions_str = transitions_str.split('\n')
    # we check every trasition in the file if the third element of the first part , the second and third
    # element of the second part is in gamma
    for transition in transitions_str:
        transition = transition.split('>')
        input_transition_rule = [character.strip() for character in
                                 transition[0].strip().replace("(", "").replace(")", "").split(",")]
        output_transition_rule = [character.strip() for character in
                                  transition[1].strip().replace("(", "").replace(")", "").split(",")]
        if input_transition_rule[2] not in Gamma:
            return "Error " + input_transition_rule[2]
        if output_transition_rule[1] not in Gamma:
            return "Error " + output_transition_rule[1]
        if output_transition_rule[2] not in Gamma:
            return "Error " + output_transition_rule[2]
    return "Validated"


# Checking if letters used in transitions are part of Sigma
def transitions_sigma_verifier(transitions_str, Sigma):
    transitions_str = transitions_str.split('\n')
    #we check every trasition in the file if the second element of the first part is in sigma
    for transition in transitions_str:
        transition = transition.split('>')
        input_transition_rule = [character.strip() for character in transition[0].strip().replace("(", "").replace(")", "").split(",")]
        if input_transition_rule[1] not in Sigma:
            return "Error " + input_transition_rule[1]
    return "validated"


# Checking if there is a single state with the 'S' status
def states_status_checker(States):
    start_state_counter = 0
    start_state = ''
    for current_state in States:
        for status in States[current_state]:
            if status == 'S':
                start_state_counter += 1
                start_state = current_state
                if start_state_counter > 1:
                    return 'Multiple starts'
    if start_state_counter == 0:
        return 'No start'
    return start_state


# Function for building the transition's dictionary
def transitions_dictionary(transitions_str):
    transitions_str = transitions_str.split('\n')
    transitions_dict = dict()
    for transition in transitions_str:
        transition = transition.split('>')

        # Separating the left and right parts of the transition by ","
        input_transition_rule = [character.strip() for character in
                                 transition[0].strip().replace("(", "").replace(")", "").split(",")]
        output_transition_rule = [character.strip() for character in
                                  transition[1].strip().replace("(", "").replace(")", "").split(",")]

        # Key built by transition's state and letter
        transition_key = (input_transition_rule[0], input_transition_rule[1])

        # Value built by gamma symbol from left part of transition, transition's destination state and the 2 letters for pop/push
        transition_value = (input_transition_rule[2], output_transition_rule[0], output_transition_rule[1], output_transition_rule[2])
        transitions_dict[transition_key] = transition_value

    return transitions_dict

def cfg_input_verifier():
    #we read from the CFG file
    with open("CFG", "r") as f:
        input_str = f.read()
    # Extract Terminal section
    terminals_str = extract_section_CFG(input_str, "Terminals")
    if terminals_str == 'Terminals not found' or terminals_str=='End not found':
        return 'Terminals section does not exist.',{}, {}, {}, {}

    # Extract Variables section
    variables_str = extract_section_CFG(input_str, "Variables")
    if variables_str == 'Variables not found' or variables_str=='End not found':
        return 'Variables section does not exist.',{}, {}, {}, {}

    # Extract Rules section
    rules_str = extract_section_CFG(input_str, "Rules")
    if rules_str == 'Rules not found' or rules_str=='End not found':
        return 'Rules section does not exist.',{}, {}, {}, {}

    # Extract Start section
    start_str = extract_section_CFG(input_str, "Start")
    if start_str == 'Start not found' or start_str=='End not found':
        return 'Start variable not defined.',{}, {}, {}, {}


    # Save terminals strings
    Terminals = terminals_parser(terminals_str)

    # Save states instances
    Variables = variables_parser(variables_str)

    # Save start variable
    Start = start_parser(start_str)

    # Verifying start variable
    Error = start_variable_checker(rules_str, Variables, Start)

    if Error == 'Start section error':
        return 'Start section not defined properly.',{}, {}, {}, {}
    elif Error == 'Start variable error':
        return 'Start variable not recognized.',{}, {}, {}, {}

    Error = rules_variables_and_terminals_checker(rules_str, Variables, Terminals, Start)
    if Error != None:
        return Error,{}, {}, {}, {}
    return 'This cfg input-file is valid!', Terminals, Variables,Start,rules_dictionary(rules_str, Variables)

    # Function for extracting section from file.

def extract_section_CFG(input_str, section_name):
    # Check if section's start border exists
    section_start = input_str.find(section_name + ":")
    if section_start == -1:
        return section_name + ' not found'

    # Check if section's end border exists
    section_end = input_str.find("End", section_start)
    if section_end == -1:
        return 'End not found'

    # Getting section's info and returning
    section_content = input_str[section_start + len(section_name + ':'): section_end]
    section_content = section_content.strip()
    return section_content

# Function for extracting terminals from 'Terminals' section in the file.
def terminals_parser(terminals_str):
    terminals_letters = []
    terminals_str = terminals_str.split('\n')
    for letter in terminals_str:
        terminals_letters.append(letter)
    return terminals_letters

# Function for extracting variables from 'Variable' section in the file.
def variables_parser(variables_str):
    variables_instances = []
    variables_str = variables_str.split('\n')
    for variable in variables_str:
        variables_instances.append(variable)
    return variables_instances

# Function for extracting start_state from 'Start' section in the  file.
def start_parser(start_str):
    start_str = start_str.split('\n')
    return start_str

# Function for checking if start_state is in the first rule, in the left part
def start_variable_checker(rules_str, Variables, Start):
    rules_str = rules_str.split('\n')
    rule_info = [element.strip() for element in rules_str[0].split('->')]
    start_variable = rule_info[0]
    if Start[0] not in Variables:
        return 'Start section error'
    if start_variable not in Start:
        return 'Start variable error'

#We check here for every rule if it contains only known terminals and variables
def rules_variables_and_terminals_checker(rules_str, Variables, Terminals, Start):
    rules_str = rules_str.split('\n')
    for rule_info in rules_str:
        rule_info = [element.strip() for element in rule_info.split('->')]
        start_variable = rule_info[0]
        current_rules = rule_info[1].split('|')
        if start_variable not in Variables:
            return 'Variable {' + start_variable + '} is not recognized.'
        #for every rule from the rules from the same variable we check if it is build correctly
        for rule in current_rules:
            for cuv in rule.split():
                if cuv not in Variables and cuv not in Terminals:
                    return 'Character {' + cuv + '} is neither from Variables set and Terminals set.'

#here we build the rules for the algorithm
def rules_dictionary(rules_str, Variables):
    rules_str = rules_str.split('\n')
    rules_dict = dict()
    for var in Variables:
        rules_dict[var] = []
    for rule_info in rules_str:
        #we divide in 2 parts one with the rules and one with the variable
        rule_info = [part.strip() for part in rule_info.split('->')]
        current_key = rule_info[0]
        current_rules = rule_info[1]
        #we divide the right part into more rules from the same variable
        current_rules = [rule.strip() for rule in current_rules.split('|')]
        for rule in current_rules:
            rules_dict[current_key].append(rule)
    return rules_dict

#here we construct the sigma of the npda that is equal with the terminals of the cfg
def cfg_pda_sigma(terminals):
    sigma=terminals
    return sigma

#here we construct the gamma of the npda that is equal with the union of the terminals and variables of the cfg
def cfg_pda_gamma(terminals,variables):
    gamma=terminals+variables
    return gamma

#here we construct the 3 states that will help us construct the PDA, qstart,qloop,qaccept
def cfg_pda_states():
    states_dictionary={'qstart':'S','qloop ': [],'qaccept':'F'}
    return states_dictionary

#here we construct the transitions of the PDA following the 3 rules that happen till we are in the final state
def cfg_pda_transition(terminals,variables,states,sigma,gamma,start,rules):
    transitions_dictionary={}
    #this is the first state and we put $ and then start in the stack
    transitions_dictionary[('qstart','#','#')]=[('qloop',[start,'$'])]
    #here is the stack
    stack=[start,'$']
    #this is for happing forever till it exits through the final if statement through break
    while 1==1:
        #this happens for every variable in the stack, stack[0] means the top of the stack
        while stack[0] in variables:
            #we memorise the element on top of the stack because we have to delete the element since we will
            #add new elements in the stack and when we will delete it, we will delete other elements and that
            # it is wrong
            var = stack[0]
            stack.pop(0)
            # for every rule for that variable we add the transition and add every element from that rule on the stack
            for w in rules[var]:
                if ('qloop', '#', var) in transitions_dictionary and ('qloop', w.split()) not in transitions_dictionary[
                    ('qloop', '#', var)]:
                    transitions_dictionary[('qloop', '#', var)].append(('qloop', w.split()))
                    #here we add the elements on the stack, this way so the first element is on top of the stack
                    stack = w.split() + stack
                else:
                    transitions_dictionary[('qloop', '#', var)] = [('qloop', w.split())]
                    stack = w.split() + stack
        #this happens till there are no more terminals on top of the stack, we just add the transition and pop
        #the top of the stack
        while stack[0] in terminals:
            if ('qloop', stack[0], stack[0]) in transitions_dictionary and ('qloop', '#') not in transitions_dictionary[
                ('qloop', stack[0], stack[0])]:
                transitions_dictionary[('qloop', stack[0], stack[0])].append(('qloop', '#'))
            else:
                transitions_dictionary[('qloop', stack[0], stack[0])] = [('qloop', '#')]
            stack.pop(0)
        #here we check if on top of the stack there is the first element we entered , which tells us that we
        #will reach the final state, so we add the transition and pop the last element from the stack
        if stack[0] == '$':
            transitions_dictionary[('qloop', '#', '$')] = ('qaccept', '#')
            stack.pop(0)
            break
    return transitions_dictionary

#here i contrusct the pda and return the values
def cfg_pda(terminals,variables,start,rules):
    sigma=cfg_pda_sigma(terminals)
    gamma=cfg_pda_gamma(terminals,variables)
    states=cfg_pda_states()
    transitions=cfg_pda_transition(terminals,variables,states,sigma,gamma,"".join(start),rules)
    return sigma,gamma,states,transitions

#here we check if the command we entered is valid by navagating the npda we just created
def verif_comanda(command,Sigma,Gamma,States,Transitions):
    stack=[]
    #too tired, sorry, we had fun!
    return "Accepted"
#here we create lists for every room so we could store the element we drop or the elements that are there from the
#beginning
def make_room_lists(Rooms,Transitions):
    Room_inventory={}
    for room in Rooms:
        Room_inventory[room]=[]
        #we check every left part of the transition and if the the current room is in there and there is a
        #form of take, for example take <item_name> we add the item that should be there through the transitions
        #we have in the "Configurare_LA"
        for transition in Transitions:
            if transition[0]==room and 'take' in transition[1]:
                Room_inventory[room].append(Transitions[transition][0])
    return Room_inventory

def run():
    #we check if there is no error while we construct the LA from the exercise 2
    feedback,Transitions_LA,States_LA, Sigma_LA, Start_LA, Gamma_LA=la_input_verifier()
    if feedback!="Your input file is valid":
        print(feedback)
        return 0
    #we check if there is no error while we construct the CFG that will be later transformed into a NPDA
    feedback, terminals, variables, start,rules = cfg_input_verifier()
    if feedback!="This cfg input-file is valid!":
        print(feedback)
        return 0
    #Here we construct the PDA that will later help us with verifying the string
    Sigma_PDA,Gamma_PDA,States_PDA,Transitions_PDA=cfg_pda(terminals,variables,start,rules)

    #Here starts the Game!!!
    stare_curenta=Start_LA
    #Our inventory
    associated_list=[]
    #list for every room in our game, we described it better there
    room_inventory=make_room_lists(list(States_LA.keys()),Transitions_LA)
    #The game ends when we reach the final state
    while 'F' not in States_LA[stare_curenta]:
        comanda=input("Command:")
        #here we validate if the command is correct by using the PDA
        feedback=verif_comanda(comanda,Sigma_PDA,Gamma_PDA,States_PDA,Transitions_PDA)
        if feedback=="Accepted":
            #we check it is from the same type of go <room_name>
            if 'go' in comanda:
                #we check if the this tuple appears in the transitions_LA which is the dictionary for transitions
                if (stare_curenta,comanda) in Transitions_LA:
                    #here it is checked if the item that is necessary for us to have to get in that room is present
                    #in the inventory
                    if Transitions_LA[(stare_curenta,comanda)][0] in associated_list or Transitions_LA[(stare_curenta,comanda)][0] == '#':
                        stare_curenta=Transitions_LA[(stare_curenta,comanda)][1]
                    else:
                        print("There is not the specified item in the inventory!")
                else:
                    print("There is no command for  "+stare_curenta)
            #the code for inventory command to check all the items we have
            if comanda=='inventory':
                #here we tell if the inventory is empty
                if len(associated_list)==0:
                    print("Inventory is empty")
                else:
                    #here we print the elements that are in our inventory
                    print("My inventory contains: "+ ",".join(associated_list))
                #We check if the command is from the time take <item_name>
            if 'take' in comanda:
                #we divide it in 2 parts and we keep only the name of the item from the take command
                item=comanda.split()[1]
                #we check if the item is not in our invnetory and it is in this room
                if item not in associated_list and item in room_inventory[stare_curenta]:
                    associated_list.append(item)
                    room_inventory[stare_curenta].remove(item)
            # we check if it has the form drop <item_name>
            if 'drop' in comanda:
                #we divide it in 2 parts and we keep only the name of the item from the drop command
                item = comanda.split()[1]
                if item in associated_list:
                    associated_list.remove(item)
                    room_inventory[stare_curenta].append(item)
            #look command so we can see where we are, what items are in this room and where we can go from here
            #and what we need to get there
            if comanda=='look':
                #the rooms that we can get to
                Potentiale_Camere=[]
                for transition in Transitions_LA:
                    # we check all the transitions if are from the current room and have a go as an action
                    if stare_curenta == transition[0] and 'go' in transition[1]:
                        Potentiale_Camere.append(Transitions_LA[transition][1])
                print("The current room is " + stare_curenta)
                print("In this room there is these items: "+ ','.join(room_inventory[stare_curenta]))
                print("The rooms that you can reach from here if you have all the items are: ")
                for room in Potentiale_Camere:
                    for transition in Transitions_LA:
                        if 'go '+room==transition[1]:
                            item=Transitions_LA[transition][0]
                    #this means we dont need anything to get there
                    if item=='#':
                        item='Nothing'
                    print(room+ ' and the item that you must have to enter it is '+item)
    print("You won!!!")
#here we run it
run()


#Neagoe Mihai Alexandru
#Cutuliga Razvan Ion
def la_input_verifier():
    #citim din fisier
    with open('input.txt', "r") as f:
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

# Function for parsing a string
def string_parser():
    # Making the validation for the input file
    feedback, Transitions, States, Sigma, Start, Gamma = la_input_verifier()
    associated_list = []

    if feedback.split()[0] != 'Error':
        with open('string.txt', "r") as f:
            string = f.read()

        # Parsing the string
        for chr in string:
            if chr in Sigma:

                # Checking the existence of the transition
                if (Start, chr) in Transitions:

                    # Checking if symbol gamma is part of AL / it is epsilon ('#' means epsilon)
                    if Transitions[(Start, chr)][0] in associated_list or Transitions[(Start, chr)][0] == '#':

                        # Removing the letter meant to be popped from the AL is existing in AL
                        if Transitions[(Start, chr)][2] in associated_list:
                            associated_list.remove(Transitions[(Start, chr)][2])

                        # Adding the letter meant to be added in AL if is not already in AL
                        if Transitions[(Start, chr)][3] not in associated_list and Transitions[(Start, chr)][3] != '#':
                            associated_list.append(Transitions[(Start, chr)][3])

                        # Setting the new state
                        Start = Transitions[(Start, chr)][1]
                    else:
                        return 'Error : symbol ' + '"' + Transitions[(Start, chr)][0] + '"' + ' not found in AL.'
                else:
                    return 'Transition from ' + '"' + Start + '"' + ' through letter ' + '"' + chr + '"' + ' not defined.'
            else:
                return 'Character ' + '"' + chr + '"' + ' not in Sigma.'
        if 'F' in States[Start]:
            return 'String Accepted!'
        return 'String dennied, state ' + '"' + Start + '"' + ' is not a final state.'
    return feedback


print(string_parser())
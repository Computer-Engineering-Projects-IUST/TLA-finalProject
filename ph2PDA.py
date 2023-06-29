class PDA:
    def __init__(self, states, alphabet, stack_alphabet, transitions, start_state, start_stack_symbol, final_states):
        self.states = states
        self.alphabet = alphabet
        self.stack_alphabet = stack_alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.start_stack_symbol = start_stack_symbol
        self.final_states = final_states

    def accepts(self, input_string):
        stack = [self.start_stack_symbol]
        current_state = self.start_state

        for symbol in input_string:
            valid_transitions = [t for t in self.transitions if t[0] == current_state and t[1] == symbol and t[2] == stack[-1] ]
            if len(valid_transitions) > 0:
                current_state = valid_transitions[4]
                stack.pop()
                if '#' not in valid_transitions[3] :
                    stack.extend(valid_transitions[3][::-1])
                
            else:
                valid_transitions = [t for t in self.transitions if t[0] == current_state and t[1] == symbol and t[2][0]=='#']
                if len(valid_transitions)>0 :
                    current_state = valid_transitions[0][4]
                    if '#' not in valid_transitions[0][3] :
                        stack.extend(valid_transitions[0][3][-1])##suppose each simbol has one charachter
                else:
                    return False
        return current_state in self.final_states


# Read input
states = set(input().strip('{}').split(','))
alphabet = set(input().strip('{}').split(','))
stack_alphabet = set(input().strip('{}').split(','))
final_states = set(input().strip('{}').split(','))
num_transitions = int(input())

transitions = []
for i in range(num_transitions):
    transition = input().strip('()').split(',')
    transitions.append((transition[0], transition[1], transition[2], transition[3], transition[4]))

input_string = input().strip()

# Initialize PDA
start_state = transitions[0][0]
start_stack_symbol = '$'
pda = PDA(states, alphabet, stack_alphabet, transitions, start_state, start_stack_symbol, final_states)

# Check if input string is accepted
if pda.accepts(input_string):
    print("Accepted")
else:
    print("Rejected")
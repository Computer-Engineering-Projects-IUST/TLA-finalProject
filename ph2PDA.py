class State:
    def __init__(self, name_state):
        self.name_state = name_state
        self.transition = {}
        
class PDA:
    def __init__(self, ss, ai, aas, fs):
        self.states = []
        self.alphabet_inputs = []
        self.alphabet_stacks = []
        self.final_states = []
        for s in ss:
            temp = State(s)
            self.states.append(temp)
            if s in fs:
                self.final_states.append(temp)
        for i in range(len(ai)):
            self.alphabet_inputs.append(ai[i][0])
        self.alphabet_inputs.append('#')
        for i in range(len(aas)):
            self.alphabet_stacks.append(aas[i][0])
        self.alphabet_stacks.append('#')
        self.alphabet_stacks.append('$')

def accepted(string_input, s, stack, i, pda):
    if i == len(string_input):
        if s in pda.final_states:
            return True
    if len(stack) == 0:
        return False
    st1 = []
    st2 = []
    st3 = []
    st4 = []
    tempp = []
    n = len(stack)
    for j in range(n):
        tempp.append(stack.pop())
    for j in range(n - 1, -1, -1):
        st1.append(tempp[j])
        st2.append(tempp[j])
        st3.append(tempp[j])
        st4.append(tempp[j])
    temp = tempp[0]
    s1 = "#," + temp
    s2 = "#,#"
    s3 = ""
    s4 = ""
    if i < len(string_input):
        s3 = string_input[i] + ",#"
        s4 = string_input[i] + "," + temp
    b = False
    if s.transition.get(s1):
        st1.pop()
        for j in range(len(s.transition[s1])):
            if s.transition[s1][j][1] != "#":
                for k in range(len(s.transition[s1][j][1]) - 1, -1, -1):
                    st1.append(s.transition[s1][j][1][k])
            b = accepted(string_input, s.transition[s1][j][0], st1, i, pda)
            st1.clear()
            for k in range(len(tempp) - 1, 0, -1):
                st1.append(tempp[k])
            if b:
                return True
    if s.transition.get(s2):
        for j in range(len(s.transition[s2])):
            if s.transition[s2][j][1] != "#":
                for k in range(len(s.transition[s2][j][1]) - 1, -1, -1):
                    st2.append(s.transition[s2][j][1][k])
            b = accepted(string_input, s.transition[s2][j][0], st2, i, pda)
            st2.clear()
            for k in range(len(tempp) - 1, -1, -1):
                st2.append(tempp[k])
            if b:
                return True
    if s.transition.get(s3):
        for j in range(len(s.transition[s3])):
            if s.transition[s3][j][1] != "#":
                for k in range(len(s.transition[s3][j][1]) - 1, -1, -1):
                    st3.append(s.transition[s3][j][1][k])
            b = accepted(string_input, s.transition[s3][j][0], st3, i + 1, pda)
            st3.clear()
            for k in range(len(tempp) - 1, -1, -1):
                st3.append(tempp[k])
            if b:
                return True
    if s.transition.get(s4):
        st4.pop()
        for j in range(len(s.transition[s4])):
            if s.transition[s4][j][1] != "#":
                for k in range(len(s.transition[s4][j][1]) - 1, -1, -1):
                    st4.append(s.transition[s4][j][1][k])
            b = accepted(string_input, s.transition[s4][j][0], st4, i + 1, pda)
            st4.clear()
            for k in range(len(tempp) - 1, 0, -1):
                st4.append(tempp[k])
            if b:
                return True
    return False

if __name__ == "__main__":
    states = input().strip('{').strip('}').split(',')
    alphabet_input = input().strip('{').strip('}').split(',')
    alphabet_stack = input().strip('{').strip('}').split(',')
    final_states = input().strip('{').strip('}').split(',')
    n = int(input())
    pda = PDA(states, alphabet_input, alphabet_stack, final_states)
    for i in range(n):
        input_str = input().split("),(")
        one = input_str[0].strip('(').split(',')
        two = input_str[1].strip(')').split(',')
        find1 = -1
        find2 = -1
        for j in range(len(pda.states)):
            if pda.states[j].name_state == one[0]:
                find1 = j
            if pda.states[j].name_state == two[1]:
                find2 = j
        if one[1] + "," + one[2] in pda.states[find1].transition:
            pda.states[find1].transition[one[1] + "," + one[2]].append((pda.states[find2], two[0]))
        else:
            temp = [(pda.states[find2], two[0])]
            pda.states[find1].transition[one[1] + "," + one[2]] = temp
    string_input = input().strip()
    stack = ['$']
    string_input = string_input.replace("#", "")
    if accepted(string_input, pda.states[0], stack, 0, pda):
        print("Accepted")
    else:
        print("Rejected")
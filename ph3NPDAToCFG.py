class Variable:
    def __init__(self, ruleName):
        self.Variable_Name = ''
        self.Rule_Name = ruleName
        self.count = 'A'
        self.content = ['', '', '']
        self.adjacent = []
        self.convertedState = {}
        self.adjacent_in_Rule = []

    def __init__(self, startState, endState, between):
        self.Variable_Name = ''
        self.Rule_Name = ''
        self.count = 'A'
        self.content = [startState, between, endState]
        self.adjacent = []
        self.convertedState = {}
        self.adjacent_in_Rule = []

        self.Variable_Name = f"(q{self.content[0]} {self.content[1]} q{self.content[2]})"
        
        if self.Variable_Name in self.convertedState:
            self.Rule_Name = self.convertedState[self.Variable_Name]
        else:
            self.Rule_Name = self.count
            self.convertedState[self.Variable_Name] = self.Rule_Name
            self.count = chr(ord(self.count) + 1)
            if self.count == 'S':
                self.count = chr(ord(self.count) + 1)

class Rule:
    def __init__(self, s, n):
        self.S = s
        self.Nt = n

    def Check(self, c):
        for i in range(len(self.Nt)):
            if c == self.Nt[i]:
                return True
        return False

    def Check(self, X, Y):
        if self.Nt[0] == X.S and self.Nt[1] == Y.S:
            return True
        return False
def Main():
    stateNumber = len(input().strip('{}').split(','))
    alphabet = input().strip('{}').split(',')
    stackContent = input().strip('{}').split(',')
    final_states = input().strip('{}').split(',')
    transitionsNumber = int(input())

    NPDA_Stack = []
    variables = []
    temp_Simplified = []
    chomskyVariables = []
    rules = []
    initialState = ' '
    startVariable = ''
    right_part = ''

    NPDA_Stack.append('$')
    i = 0
    while i < transitionsNumber:
        transition = input().replace('(', '').replace(')', '').split(',')
        
        if transition[-1] == 'qf' or transition[0] == 'qf':
            transition[-1] = 'q' + str(stateNumber - 1)

        if transition[3] == '#':
            if i == 0:
                line = '->' + transition[0].replace('(', '').replace(')', '')
                transition = line.split(',')
            else:
                transition = transition

            if final_states.__contains__(transition[-1]):
                transition[-1] = '*' + transition[-1]

            if len(transition[0]) == 4:
                initialState = transition[0][3]
                if len(transition[4]) == 3:
                    AddAdjacent(variables, 3, 2, transition, stateNumber)
                else:
                    AddAdjacent(variables, 3, 1, transition, stateNumber)
            else:
                if len(transition[4]) == 3:
                    AddAdjacent(variables, 1, 2, transition, stateNumber)
                else:
                    AddAdjacent(variables, 1, 1, transition, stateNumber)
        else:
            if len(transition[0]) == 4:
                initialState = transition[0][3]
                if len(transition[4]) == 3:
                    variables.append(Variable(transition[0][3], transition[4][2], transition[2][0]))
                    variables[-1].adjacent.append((transition[1][0], '', ''))
                    variables[-1].adjacent_in_Rule.append((transition[1][0], '', ''))

                    if transition[2] == '$':
                        startVariable = variables[-1].Variable_Name

                    temp_Simplified.append(variables[-1])
                else:
                    variables.append(Variable(transition[0][3], transition[4][1], transition[2][0]))
                    variables[-1].adjacent.append((transition[1][0], '', ''))
                    variables[-1].adjacent_in_Rule.append((transition[1][0], '', ''))
                    temp_Simplified.append(variables[-1])
            else:
                if len(transition[4]) == 3:
                    variables.append(Variable(transition[0][1], transition[4][2], transition[2][0]))
                    variables[-1].adjacent.append((transition[1][0], '', ''))
                    variables[-1].adjacent_in_Rule.append((transition[1][0], '', ''))

                    if transition[0][1] == initialState and transition[2] == '$':
                        startVariable = variables[-1].Variable_Name

                    temp_Simplified.append(variables[-1])
                else:
                    variables.append(Variable(transition[0][1], transition[4][1], transition[2][0]))
                    variables[-1].adjacent.append((transition[1][0], '', ''))
                    variables[-1].adjacent_in_Rule.append((transition[1][0], '', ''))
                    temp_Simplified.append(variables[-1])
    
    i += 1
    result = ''
    PrintGrammar(variables, result)

    EditStartVariable(variables, startVariable)
    variables = SimplifiedVariable(variables, temp_Simplified)
    variables = RemoveNullableVariable(variables, temp_Simplified)

    chomskyVariables = variables
    ConvertToChomsky(chomskyVariables, len(chomskyVariables))

    for variable in chomskyVariables:
        for i in range(len(variable.adjacent_in_Rule)):
            right_part = ''
            if variable.adjacent_in_Rule[i][0] != ' ':
                right_part += variable.adjacent_in_Rule[i][0]

            if variable.adjacent_in_Rule[i][1] != ' ':
                right_part += variable.adjacent_in_Rule[i][1] + variable.adjacent_in_Rule[i][2]

            rules.append(Rule(variable.Rule_Name, right_part))

def SimplifiedVariable(var, temp_Simplified):
    hasChanged = False
    simple_member = []
    simplified = []

    for variable in temp_Simplified:
        simplified.append(variable)
        simple_member.append(variable.Rule_Name)

    while True:
        for variable in var:
            hasChanged = False
            for adjacent in variable.adjacent_in_Rule:
                if adjacent.Item2 in simple_member and adjacent.Item3 in simple_member:
                    simplified.append(Variable(variable.Rule_Name))
                    simplified[-1].adjacent_in_Rule.append(adjacent)
                    simple_member.append(variable.Rule_Name)
                    hasChanged = True
        if not hasChanged:
            break

    return simplified


def RemoveNullableVariable(all_variables, temp_Simplified):
    nullableVariable = None
    variablesWithoutNullable = []

    for variable in temp_Simplified:
        for adj in variable.adjacent_in_Rule:
            if adj.Item1 == '_':
                nullableVariable = variable.Rule_Name

    for variable in all_variables:
        variablesWithoutNullable.append(variable)

    for i in range(len(all_variables)):
        for j in range(len(all_variables[i].adjacent_in_Rule)):
            if all_variables[i].adjacent_in_Rule[j].Item2 == "S" and all_variables[i].adjacent_in_Rule[j].Item3 != "S":
                variablesWithoutNullable[i].adjacent_in_Rule.append((all_variables[i].adjacent_in_Rule[j].Item1, all_variables[i].adjacent_in_Rule[j].Item2, ""))

            if all_variables[i].adjacent_in_Rule[j].Item3 == "S" and all_variables[i].adjacent_in_Rule[j].Item2 != "S":
                variablesWithoutNullable[i].adjacent_in_Rule.append((all_variables[i].adjacent_in_Rule[j].Item1, all_variables[i].adjacent_in_Rule[j].Item2, ""))

    return variablesWithoutNullable


def ConvertToChomsky(chomskyVariables, chomskyVariablesCount):
    i = 0
    while i < chomskyVariablesCount:
        j = 0
        while j < len(chomskyVariables[i].adjacent_in_Rule):
            if chomskyVariables[i].adjacent_in_Rule[j].Item2 != "":
                if chomskyVariables[i].adjacent_in_Rule[j].Item3 != "":
                    letter = str(chomskyVariables[i].adjacent_in_Rule[j].Item1)
                    chomskyVariables.append(Variable(letter, "", ""))
                    chomskyVariables[-1].adjacent_in_Rule.append((letter, "", ""))
                    letter = chomskyVariables[-1].Rule_Name
                    adjacentVariable = chomskyVariables[i].adjacent_in_Rule[j].Item2
                    chomskyVariables.append(Variable(letter, adjacentVariable, ""))
                    chomskyVariables[-1].adjacent_in_Rule.append((letter, adjacentVariable, ""))
                    adjacentVariable = chomskyVariables[i].adjacent_in_Rule[j].Item3
                    chomskyVariables[i].adjacent_in_Rule[j] = (' ', chomskyVariables[-2].Rule_Name, adjacentVariable)
                else:
                    letter = str(chomskyVariables[i].adjacent_in_Rule[j].Item1)
                    chomskyVariables.append(Variable(letter, "", ""))
                    chomskyVariables[-1].adjacent_in_Rule.append((letter, "", ""))
                    adjacentVariable = chomskyVariables[i].adjacent_in_Rule[j].Item2
                    chomskyVariables[i].adjacent_in_Rule[j] = (' ', chomskyVariables[-1].Rule_Name, adjacentVariable)
            j += 1
        i += 1
def EditStartVariable(variables, startVariable):
    i = 0
    while i < len(variables):
        if startVariable == variables[i].Variable_Name:
            variables[i].Rule_Name = "S"

        j = 0
        while j < len(variables[i].adjacent):
            if startVariable == variables[i].adjacent[j].Item2 and startVariable == variables[i].adjacent[j].Item3:
                variables[i].adjacent_in_Rule[j] = (' ', "S", "S")

            if startVariable == variables[i].adjacent[j].Item2:
                variables[i].adjacent_in_Rule[j] = (' ', "S", variables[i].adjacent_in_Rule[j].Item3)

            if startVariable == variables[i].adjacent[j].Item3:
                variables[i].adjacent_in_Rule[j] = (' ', variables[i].adjacent_in_Rule[j].Item2, "S")
            j += 1
        i += 1


def PrintGrammar(variables, output):
    i = 0
    while i < len(variables):
        variable = variables[i]
        j = 0
        while j < len(variable.adjacent):
            adj = variable.adjacent[j]
            if adj.Item2 == "" and adj.Item3 == "":
                print(f"{variable.Variable_Name} -> {adj.Item1}")
                output += f"{variable.Variable_Name} -> {adj.Item1}   "
            else:
                print(f"{variable.Variable_Name} -> {adj.Item1} {adj.Item2} {adj.Item3}")
                output += f"{variable.Variable_Name} -> {adj.Item1} {adj.Item2} {adj.Item3}   "
            j += 1
        i += 1


def AddAdjacent(variables, firstIndex, secondIndex, input, stateNumber):
    i = 0
    while i < stateNumber:
        variables.append(Variable(input[0][firstIndex], str(i), input[2]))
        index = len(variables) - 1
        state = 0
        while state < stateNumber:
            variables.append(Variable(input[4][secondIndex], str(state), input[3][0]))
            variables.append(Variable(str(state), str(i), input[3][1]))
            variables[-2].adjacent.append((input[1][0], variables[-1].variableName, variables[-2].Variable_Name))
            variables[-2].adjacent_in_Rule.append((input[1][0], variables[-1].Rule_Name, variables[-2].Rule_Name))
            state += 1
        i += 1
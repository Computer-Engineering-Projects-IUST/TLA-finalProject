class State:
    def __init__(self, StateName):
        self.StateName = StateName
        self.Tra = {}
        
class PushdownAutomata:
    def __init__(self, sts, Inputalphabs, Stackalphabs, Finals):
        self.States = []
        self.InputAlphabet = []
        self.StackAlphabet = []
        self.FinalStates = []
        for s in sts:
            temp = State(s)
            self.States.append(temp)
            if s in Finals:
                self.FinalStates.append(temp)
        for i in range(len(Inputalphabs)):
            self.InputAlphabet.append(Inputalphabs[i][0])
        self.InputAlphabet.append('#')
        for i in range(len(Stackalphabs)):
            self.StackAlphabet.append(Stackalphabs[i][0])
        self.StackAlphabet.append('#')
        self.StackAlphabet.append('$')

def DoesThePDAAccept(Inpstr, states, Stack, Counter, InputPDA):
    if Counter == len(Inpstr):
        if states in InputPDA.FinalStates:
            return True
    if len(Stack) == 0:
        return False
    FirstStack = []
    SecondStack = []
    ThirdStack = []
    FourthStack = []
    TemporaryList = []
    n = len(Stack)
    i = 0
    while i < n:
        TemporaryList.append(Stack.pop())
        i += 1

    FirstStack.extend(reversed(TemporaryList))
    SecondStack.extend(reversed(TemporaryList))
    ThirdStack.extend(reversed(TemporaryList))
    FourthStack.extend(reversed(TemporaryList))
    
    FirstChar = TemporaryList[0]
    FirstString = "#," + FirstChar
    SecondString = "#,#"
    ThirdString = ""
    FourthString = ""
    if Counter < len(Inpstr):
        ThirdString = Inpstr[Counter] + ",#"
        FourthString = Inpstr[Counter] + "," + FirstChar
    Result = False
    if states.Tra.get(FirstString):
        FirstStack.pop()
        i = 0
        while i < len(states.Tra[FirstString]):
            if states.Tra[FirstString][i][1] != "#":
                k = len(states.Tra[FirstString][i][1]) - 1
                while k >= 0:
                    FirstStack.append(states.Tra[FirstString][i][1][k])
                    k -= 1
            Result = DoesThePDAAccept(Inpstr, states.Tra[FirstString][i][0], FirstStack, Counter, InputPDA)
            FirstStack.clear()
            k = len(TemporaryList) - 1
            while k > 0:
                FirstStack.append(TemporaryList[k])
                k -= 1
            if Result:
                return True
            i += 1
    if states.Tra.get(SecondString):
        i = 0
        while i < len(states.Tra[SecondString]):
            if states.Tra[SecondString][i][1] != "#":
                k = len(states.Tra[SecondString][i][1]) - 1
                while k >= 0:
                    SecondStack.append(states.Tra[SecondString][i][1][k])
                    k -= 1
            Result = DoesThePDAAccept(Inpstr, states.Tra[SecondString][i][0], SecondStack, Counter, InputPDA)
            SecondStack.clear()
            k = len(TemporaryList) - 1
            while k >= 0:
                SecondStack.append(TemporaryList[k])
                k -= 1
            if Result:
                return True
            i += 1
    if states.Tra.get(ThirdString):
        i = 0
        while i < len(states.Tra[ThirdString]):
            if states.Tra[ThirdString][i][1] != "#":
                k = len(states.Tra[ThirdString][i][1]) - 1
                while k >= 0:
                    ThirdStack.append(states.Tra[ThirdString][i][1][k])
                    k -= 1
            Result = DoesThePDAAccept(Inpstr, states.Tra[ThirdString][i][0], ThirdStack, Counter + 1, InputPDA)
            ThirdStack.clear()
            k = len(TemporaryList) - 1
            while k >= 0:
                ThirdStack.append(TemporaryList[k])
                k -= 1
            if Result:
                return True
            i += 1
    if states.Tra.get(FourthString):
        FourthStack.pop()
        i = 0
        while i < len(states.Tra[FourthString]):
            if states.Tra[FourthString][i][1] != "#":
                k = len(states.Tra[FourthString][i][1]) - 1
                while k >= 0:
                    FourthStack.append(states.Tra[FourthString][i][1][k])
                    k -= 1
            Result = DoesThePDAAccept(Inpstr, states.Tra[FourthString][i][0], FourthStack, Counter + 1, InputPDA)
            FourthStack.clear()
            k = len(TemporaryList) - 1
            while k > 0:
                FourthStack.append(TemporaryList[k])
                k -= 1
            if Result:
                return True
            i += 1
    return False

if __name__ == "__main__":
    states = input().strip('{').strip('}').split(',')
    InputAlphabet = input().strip('{').strip('}').split(',')
    StackAlphabet = input().strip('{').strip('}').split(',')
    FinalStates = input().strip('{').strip('}').split(',')
    n = int(input())
    InputPDA = PushdownAutomata(states, InputAlphabet, StackAlphabet, FinalStates)
    i = 0
    while i < n:
        Input = input().split("),(")
        First = Input[0].strip('(').split(',')
        Second = Input[1].strip(')').split(',')
        Result1 = -1
        Result2 = -1
        j = 0
        while j < len(InputPDA.States):
            if InputPDA.States[j].StateName == First[0]:
                Result1 = j
            if InputPDA.States[j].StateName == Second[1]:
                Result2 = j
            j += 1
        if First[1] + "," + First[2] in InputPDA.States[Result1].Tra:
            InputPDA.States[Result1].Tra[First[1] + "," + First[2]].append((InputPDA.States[Result2], Second[0]))
        else:
            tempList = [(InputPDA.States[Result2], Second[0])]
            InputPDA.States[Result1].Tra[First[1] + "," + First[2]] = tempList
        i += 1
    Inpstr = input().strip()
    stack = ['$']
    Inpstr = Inpstr.replace("#", "")
    if DoesThePDAAccept(Inpstr, InputPDA.States[0], stack, 0, InputPDA) is False:
        print("Rejected")
    else:
        print("Accepted")
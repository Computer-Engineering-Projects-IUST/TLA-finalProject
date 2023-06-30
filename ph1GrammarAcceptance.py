import sys

class Grammar:
    def __init__(self):
        self.productions = {}
        self.Letters = {}
        self.root = None
        self.reshte=""
    def callGrammarInitialize(self):
        lineNumber = int(input())
        for i in range(lineNumber):
            self.parser(input(), i==0)
        self.removeLambdaProduction()
        self.removeUnitProductions()
        self.simplifyMoreThanTwoVariables()
        self.reshte=input()
        print(self.Acceptance())

    def parser(self, input, isRoot):
        left = ""
        for i in range(1, len(input)):
            if input[i] == '>':
                break
            left += input[i]
        if isRoot:
            self.root = left
        index = 1
        for index in range(1, len(input) - 1):
            if input[index] == '-' and input[index + 1] == '>':
                index += 2
                break

        right = ""
        for i in range(index, len(input)):
            if input[i] != ' ':
                right += input[i]

        Output = right.split('|')
        newProduction = []
        for str in Output:
            newGrammar = []
            i = 0
            while i < len(str):
                if str[i] == '<':
                    i += 1
                    newString = ""
                    while str[i] != '>':
                        newString += str[i]
                        i += 1

                    newGrammar.append(newString)

                else:
                    if str[i] == '#':
                        newGrammar.append("#")
                    else:
                        if str[i] not in self.Letters.keys():
                            self.Letters[str[i]] = "l{}".format(len(self.Letters))
                            self.productions[self.Letters[str[i]]] = [[str[i]]]
                        
                        newGrammar.append(self.Letters[str[i]])
                i += 1
            newProduction.append(newGrammar)
        self.productions[left] = newProduction

    def removeLambdaProduction(self):
        states = list(self.productions.keys())
        for k in range(len(states)):
            prd = (states[k], self.productions[states[k]])
            i = 0
            while i < len(prd[1]):
                if len(prd[1][i]) == 1 and prd[1][i][0] == "#":
                    prd[1].pop(i)
                    for x in self.productions.items():
                        for j in range(len(x[1])):
                            if prd[0] in x[1][j]:
                                newstr = [z for z in x[1][j] if z != prd[0]]
                                if x[0] != prd[0] and len(newstr) == 0:
                                    newstr.append("#")
                                x[1].append(newstr)
                    k = -1
                    i += 1
                else:
                    i += 1

    def getReachable(self, start, Visited):
        Visited.append(start)
        if start in self.productions:
            for subPrd in self.productions[start]:
                if len(subPrd) == 1 and subPrd[0] not in self.Letters and subPrd[0] not in Visited:
                    self.getReachable(subPrd[0], Visited)
        else:
             Visited.remove(start)

    def removeUnitProductions(self):
        for Prd in self.productions.items():
            visited = []

            self.getReachable(Prd[0], visited)
            visited.remove(Prd[0])
            for visit in visited:
                for i in range(len(self.productions[visit])):
                    subPrd = self.productions[visit][i]
                    if len(subPrd) != 1 or subPrd[0] in self.Letters:
                        Prd[1].append(subPrd)
        for Prd in self.productions:
            i = 0
            while i < len(self.productions[Prd]):
                subPrd = self.productions[Prd][i]
                if len(subPrd) == 1 and subPrd[0] not in self.Letters.keys():
                    self.productions[Prd].pop(i)
                    i+=1
                else:
                    i += 1

    def simplifyMoreThanTwoVariables(self):
        madeStates = {}
        for Prd in self.productions.items():
            for subPrd in Prd[1]:
                while len(subPrd) > 2:
                    if f"{subPrd[-2]}*{subPrd[-1]}" not in madeStates:
                        madeStates[f"{subPrd[-2]}*{subPrd[-1]}"] = f"NS{len(madeStates)}"
                    subPrd.append(madeStates[f"{subPrd[-2]}*{subPrd[-1]}"])
                    subPrd.pop(-3)
                    subPrd.pop(-2)

        for x in madeStates.items():
            newstr = x[0].split('*')
            news = []
            for y in newstr:
                news.append(y)
            self.productions[x[1]] = [news]

    def Acceptance(self):
        n = len(self.reshte)

        for i in range(len(self.reshte)):
            if self.reshte[i] not in self.Letters.keys():
                return "Rejected"

        AcceptTeble = [[[] for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for Prd in self.productions.items():
                for subPrd in Prd[1]:
                    if len(subPrd) == 1 and subPrd[0] == self.reshte[i]:
                        AcceptTeble[i][i].append(Prd[0])

        for l in range(2, n + 1):
            for i in range(n - l + 1):
                j = i + l - 1

                for k in range(i, j):
                    for Prd in self.productions.items():
                        for subPrd in Prd[1]:
                            if (len(subPrd) == 2 and subPrd[0] in AcceptTeble[i][k] and subPrd[1] in AcceptTeble[k + 1][j]):
                                AcceptTeble[i][j].append(Prd[0])
                                break

        if self.root in AcceptTeble[0][n - 1]:
            return "Accepted"
        else:
            return "Rejected"


g = Grammar()
g.callGrammarInitialize()
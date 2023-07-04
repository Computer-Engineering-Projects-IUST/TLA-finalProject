using System;
using System.Collections.Generic;
using System.Linq;
namespace Final_TLA_Project
{
    public class NPDA_TO_CFG
    {
        public partial class Variable
        {
            public string variableName;
            public string nameInRule;
            public char count = 'A';
            public string[] content = new string[3];
            public List<Tuple<char, string, string>> adjacent = new List<Tuple<char, string, string>>();
            public Dictionary<string, string> convertedState = new Dictionary<string, string>();
            public List<Tuple<char, string, string>> adjacent_in_Rule = new List<Tuple<char, string, string>>();

            public Variable(string ruleName)
            {
                nameInRule = ruleName;
            }
            public Variable(string startState, string endState, string between)
            {
                content[0] = startState;
                content[1] = between;
                content[2] = endState;
                variableName = $"(q{content[0]} {content[1]} q{content[2]})";

                if (convertedState.ContainsKey(variableName))
                    nameInRule = convertedState[variableName];
                else
                {
                    nameInRule = count.ToString();
                    convertedState.Add(variableName, nameInRule);
                    count++;
                    if (count == 'S')
                        count++;
                }
            }
        }
        public partial class Rule
        {
            public string S;
            private string Nt;

            public Rule(string s, string n)
            {
                S = s;
                Nt = n;
            }
            public bool Check(string c)
            {
                for (int i = 0; i < Nt.Length; i++)
                {
                    if (c == Nt[i].ToString())
                        return true;
                }
                return false;
            }

            public bool Check(Rule X, Rule Y)
            {
                if (Nt[0].ToString() == X.S && Nt[1].ToString() == Y.S)
                    return true;

                return false;
            }
        }
        public static void Main(string[] args)
        {
            int stateNumber = Console.ReadLine().Trim('{', '}').Split(',').ToArray().Length;
            string[] alphabet = Console.ReadLine().Trim('{', '}').Split(',').ToArray();
            string[] stackContent = Console.ReadLine().Trim('{', '}').Split(',').ToArray();
            List<string> final_states = Console.ReadLine().Trim('{', '}').Split(',').ToList();
            int transitionsNumber = int.Parse(Console.ReadLine());

            Stack<string> NPDA_Stack = new Stack<string>();
            List<Variable> variables = new List<Variable>();
            List<Variable> temp_Simplified = new List<Variable>();
            List<Variable> chomskyVariables;
            List<Rule> rules = new List<Rule>();
            char initialState = ' ';
            string startVariable = "";
            string right_part;


            NPDA_Stack.Push("$");
            for (int i = 0; i < transitionsNumber; i++)
            {
                string[] transition;
                if (i == 0)
                {
                    string line = "->" + Console.ReadLine().Replace("(", "").Replace(")", "");
                    transition = line.Split(new char[] { ',' }).ToArray();
                }
                else
                    transition = Console.ReadLine().Replace("(", "").Replace(")", "").Split(new char[] { ',' }).ToArray();

                if (transition[transition.Length - 1] == "qf" || transition[0] == "qf")
                    transition[transition.Length - 1] = "q" + (stateNumber - 1).ToString();

                if (final_states.Contains(transition[transition.Length - 1]))
                    transition[transition.Length - 1] = "*" + transition[transition.Length - 1];

                if (transition[3] == "#")
                {
                    //first transition has "-->" symbol
                    if (transition[0].Length == 4)
                    {
                        initialState = transition[0][3];
                        //last transition has * as final state 
                        if (transition[4].Length == 3)
                        {
                            variables.Add(new Variable(transition[0][3].ToString(), transition[4][2].ToString(), transition[2][0].ToString()));
                            variables[variables.Count - 1].adjacent.Add(new Tuple<char, string, string>(transition[1][0], "", ""));
                            variables[variables.Count - 1].adjacent_in_Rule.Add(new Tuple<char, string, string>(transition[1][0], "", ""));
                            if (transition[2] == "$")
                                startVariable = variables[variables.Count - 1].variableName;

                            temp_Simplified.Add(variables[variables.Count - 1]);
                        }
                        else
                        {
                            variables.Add(new Variable(transition[0][3].ToString(), transition[4][1].ToString(), transition[2][0].ToString()));
                            variables[variables.Count - 1].adjacent.Add(new Tuple<char, string, string>(transition[1][0], "", ""));
                            variables[variables.Count - 1].adjacent_in_Rule.Add(new Tuple<char, string, string>(transition[1][0], "", ""));
                            temp_Simplified.Add(variables[variables.Count - 1]);
                        }
                    }
                    else
                    {
                        //last transition has * as final state 
                        if (transition[4].Length == 3)
                        {
                            variables.Add(new Variable(transition[0][1].ToString(), transition[4][2].ToString(), transition[2][0].ToString()));
                            variables[variables.Count - 1].adjacent.Add(new Tuple<char, string, string>(transition[1][0], "", ""));
                            variables[variables.Count - 1].adjacent_in_Rule.Add(new Tuple<char, string, string>(transition[1][0], "", ""));

                            if (transition[0][1] == initialState && transition[2] == "$")
                                startVariable = variables[variables.Count - 1].variableName;

                            temp_Simplified.Add(variables[variables.Count - 1]);
                        }
                        else
                        {
                            variables.Add(new Variable(transition[0][1].ToString(), transition[4][1].ToString(), transition[2][0].ToString()));
                            variables[variables.Count - 1].adjacent.Add(new Tuple<char, string, string>(transition[1][0], "", ""));
                            variables[variables.Count - 1].adjacent_in_Rule.Add(new Tuple<char, string, string>(transition[1][0], "", ""));
                            temp_Simplified.Add(variables[variables.Count - 1]);
                        }
                    }
                }
                else
                {
                    //first transition has "-->" symbol
                    if (transition[0].Length == 4)
                    {
                        initialState = transition[0][3];
                        //last transition has * as final state 
                        if (transition[4].Length == 3)
                            AddAdjacent(variables, 3, 2, transition, stateNumber);
                        else
                            AddAdjacent(variables, 3, 1, transition, stateNumber);
                    }
                    else
                    {
                        //last transition has * as final state 
                        if (transition[4].Length == 3)
                            AddAdjacent(variables, 1, 2, transition, stateNumber);
                        else
                            AddAdjacent(variables, 1, 1, transition, stateNumber);
                    }
                }
            }
            string result = "";
            PrintGrammer(variables, ref result);


            EditStartVariable(variables, startVariable);
            variables = SimplifiedVariable(variables, temp_Simplified);
            variables = RemoveNullableVariable(variables, temp_Simplified);

            chomskyVariables = variables;
            ConvertToChomsky(chomskyVariables, chomskyVariables.Count);


            foreach (var variable in chomskyVariables)
            {
                for (int i = 0; i < variable.adjacent_in_Rule.Count(); i++)
                {
                    right_part = "";
                    if (variable.adjacent_in_Rule[i].Item1 != ' ')
                        right_part += variable.adjacent_in_Rule[i].Item1;

                    if (variable.adjacent_in_Rule[i].Item2 != " ")
                        right_part += variable.adjacent_in_Rule[i].Item2 + variable.adjacent_in_Rule[i].Item3;

                    rules.Add(new Rule(variable.nameInRule, right_part));
                }

            }

        }
        public static List<Variable> SimplifiedVariable(List<Variable> var, List<Variable> temp_Simplified)
        {
            bool hasChanged = false;
            List<string> simple_member = new List<string>();
            List<Variable> simplified = new List<Variable>();


            foreach (var variable in temp_Simplified)
            {
                simplified.Add(variable);
                simple_member.Add(variable.nameInRule);
            }
            do
            {
                foreach (var variable in var)
                {
                    hasChanged = false;
                    foreach (var adjacent in variable.adjacent_in_Rule)
                    {
                        if (simple_member.Contains(adjacent.Item2) && simple_member.Contains(adjacent.Item3))
                        {
                            simplified.Add(new Variable(variable.nameInRule));
                            simplified[simplified.Count - 1].adjacent_in_Rule.Add(adjacent);
                            simple_member.Add(variable.nameInRule);
                            hasChanged = true;
                        }
                    }
                }

            } while (hasChanged);
            return simplified;
        }
        public static List<Variable> RemoveNullableVariable(List<Variable> all_variables, List<Variable> temp_Simplified)
        {
            string nullableVariable;
            List<Variable> variablesWithoutNullable = new List<Variable>();

            foreach (var variable in temp_Simplified)
            {
                foreach (var adj in variable.adjacent_in_Rule)
                    if (adj.Item1 == '_')
                        nullableVariable = variable.nameInRule;
            }

            foreach (var variable in all_variables)
                variablesWithoutNullable.Add(variable);

            for (int i = 0; i < all_variables.Count; i++)
            {
                for (int j = 0; j < all_variables[i].adjacent_in_Rule.Count; j++)
                {
                    if (all_variables[i].adjacent_in_Rule[j].Item2 == "S" && all_variables[i].adjacent_in_Rule[j].Item3 != "S")
                        variablesWithoutNullable[i].adjacent_in_Rule.Add(new Tuple<char, string, string>(all_variables[i].adjacent_in_Rule[j].Item1, all_variables[i].adjacent_in_Rule[j].Item2, ""));

                    if (all_variables[i].adjacent_in_Rule[j].Item3 == "S" && all_variables[i].adjacent_in_Rule[j].Item2 != "S")
                        variablesWithoutNullable[i].adjacent_in_Rule.Add(new Tuple<char, string, string>(all_variables[i].adjacent_in_Rule[j].Item1, all_variables[i].adjacent_in_Rule[j].Item2, ""));
                }
            }
            return variablesWithoutNullable;
        }
        public static void ConvertToChomsky(List<Variable> chomskyVariables, int chomskyVariablesCount)
        {
            string letter;
            string adjacentVariable;
            for (int i = 0; i < chomskyVariablesCount; i++)
            {
                for (int j = 0; j < chomskyVariables[i].adjacent_in_Rule.Count(); j++)
                {
                    if (chomskyVariables[i].adjacent_in_Rule[j].Item2 != "")
                    {
                        if (chomskyVariables[i].adjacent_in_Rule[j].Item3 != "")
                        {
                            letter = chomskyVariables[i].adjacent_in_Rule[j].Item1.ToString();
                            chomskyVariables.Add(new Variable(letter, "", ""));
                            chomskyVariables[chomskyVariables.Count - 1].adjacent_in_Rule.Add(new Tuple<char, string, string>(char.Parse(letter), "", ""));
                            letter = chomskyVariables[chomskyVariables.Count - 1].nameInRule;
                            adjacentVariable = chomskyVariables[i].adjacent_in_Rule[j].Item2;
                            chomskyVariables.Add(new Variable(letter, adjacentVariable, ""));
                            chomskyVariables[chomskyVariables.Count - 1].adjacent_in_Rule.Add(new Tuple<char, string, string>(char.Parse(letter), adjacentVariable, ""));
                            adjacentVariable = chomskyVariables[i].adjacent_in_Rule[j].Item3;
                            chomskyVariables[i].adjacent_in_Rule[j] = new Tuple<char, string, string>(' ', chomskyVariables[chomskyVariables.Count - 1].nameInRule, adjacentVariable);
                        }
                        else
                        {
                            letter = chomskyVariables[i].adjacent_in_Rule[j].Item1.ToString();
                            chomskyVariables.Add(new Variable(letter, "", ""));
                            chomskyVariables[chomskyVariables.Count - 1].adjacent_in_Rule.Add(new Tuple<char, string, string>(char.Parse(letter), "", ""));
                            adjacentVariable = chomskyVariables[i].adjacent_in_Rule[j].Item2;
                            chomskyVariables[i].adjacent_in_Rule[j] = new Tuple<char, string, string>(' ', chomskyVariables[chomskyVariables.Count - 1].nameInRule, adjacentVariable);
                        }
                    }
                }
            }
        }
        public static void EditStartVariable(List<Variable> variables, string startVariable)
        {
            for (int i = 0; i < variables.Count; i++)
            {
                if (startVariable == variables[i].variableName)
                    variables[i].nameInRule = "S";

                for (int j = 0; j < variables[i].adjacent.Count; j++)
                {
                    if (startVariable == variables[i].adjacent[j].Item2 && startVariable == variables[i].adjacent[j].Item3)
                        variables[i].adjacent_in_Rule[j] = new Tuple<char, string, string>(variables[i].adjacent_in_Rule[j].Item1, "S", "S");

                    if (startVariable == variables[i].adjacent[j].Item2)
                        variables[i].adjacent_in_Rule[j] = new Tuple<char, string, string>(variables[i].adjacent_in_Rule[j].Item1, "S", variables[i].adjacent_in_Rule[j].Item3);

                    if (startVariable == variables[i].adjacent[j].Item3)
                        variables[i].adjacent_in_Rule[j] = new Tuple<char, string, string>(variables[i].adjacent_in_Rule[j].Item1, variables[i].adjacent_in_Rule[j].Item2, "S");
                }
            }
        }
        public static void PrintGrammer(List<Variable> variables, ref string output)
        {
            foreach (var variable in variables)
            {
                foreach (var adj in variable.adjacent)
                {
                    if (adj.Item2 == "" & adj.Item3 == "")
                        Console.WriteLine($"{variable.variableName} -> {adj.Item1} ");
                    else
                    {
                        Console.WriteLine($"{variable.variableName} -> {adj.Item1} {adj.Item2} {adj.Item3}");
                        output += $"{variable.variableName} -> {adj.Item1} {adj.Item2} {adj.Item3}   ";
                    }
                }
            }
        }
        public static void AddAdjacent(List<Variable> variables, int firstIndex, int secondIndex, string[] input, int stateNumber)
        {
            int index;
            for (int i = 0; i < stateNumber; i++)
            {
                variables.Add(new Variable(input[0][firstIndex].ToString(), i.ToString(), input[2]));
                index = variables.Count - 1;
                for (int state = 0; state < stateNumber; state++)
                {
                    variables.Add(new Variable(input[4][secondIndex].ToString(), state.ToString(), input[3][0].ToString()));
                    variables.Add(new Variable(state.ToString(), i.ToString(), input[3][1].ToString()));
                    variables[index].adjacent.Add(new Tuple<char, string, string>(input[1][0], variables[variables.Count - 2].variableName, variables[variables.Count - 1].variableName));
                    variables[index].adjacent_in_Rule.Add(new Tuple<char, string, string>(input[1][0], variables[variables.Count - 2].nameInRule, variables[variables.Count - 1].nameInRule));
                }
            }
        }
    }
}
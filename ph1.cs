using System;
using System.Collections.Generic;
using System.Linq;

namespace Q1
{
    class Grammer
    {
        Dictionary<string, List<List<string>>> Rules;
        Dictionary<string, string> Leters;
        string root;
        public Grammer()
        {
            Rules = new Dictionary<string, List<List<string>>>();
            Leters = new Dictionary<string, string>();

            int num = int.Parse(Console.ReadLine());
            for (int i = 0; i < num; i++)
            {
                inputParser(Console.ReadLine(), i == 0);
            }
            removeLambda();
            removeUnits();
            handleMoreTow();
            Console.WriteLine(Acceptance(Console.ReadLine()));
            /*foreach(var x in Rules)
            {
                Console.Write(x.Key+"->");
                foreach(var y in x.Value)
                {
                    foreach(var z in y)
                    {
                        Console.Write(z + " ");
                    }
                    Console.Write("|");
                }
                Console.WriteLine();
            }*/
        }
        void handleMoreTow()
        {
            Dictionary<string, string> madeStates = new Dictionary<string, string>();
            foreach (var Rule in Rules)
            {
                foreach (var subRule in Rule.Value)
                {
                    while (subRule.Count > 2)
                    {
                        if (!madeStates.ContainsKey(subRule[subRule.Count - 2] + "*" + subRule[subRule.Count - 1]))
                        {
                            madeStates.Add(subRule[subRule.Count - 2] + "*" + subRule[subRule.Count - 1], "NS" + madeStates.Count);
                        }
                        subRule.Add(madeStates[subRule[subRule.Count - 2] + "*" + subRule[subRule.Count - 1]]);
                        subRule.RemoveAt(subRule.Count - 2);
                        subRule.RemoveAt(subRule.Count - 2);
                    }
                }

            }
            foreach (var x in madeStates)
            {
                string[] newstr = x.Key.Split('*');
                List<string> news = new List<string>();
                foreach (var y in newstr)
                {
                    news.Add(y);
                }
                Rules.Add(x.Value, new List<List<string>>() { news });
            }
        }
        void removeLambda()
        {
            var states = Rules.Keys.ToArray();
            for (int k = 0; k < states.Length; k++)
            {
                var Rule = new KeyValuePair<string, List<List<string>>>(states[k], Rules[states[k]]);
                for (int i = 0; i < Rule.Value.Count; i++)
                {
                    if (Rule.Value[i].Count == 1 && Rule.Value[i][0] == "#")
                    {
                        Rule.Value.RemoveAt(i);
                        foreach (var x in Rules)
                        {
                            for (int j = 0; j < x.Value.Count; j++)
                            {
                                if (x.Value[j].Contains(Rule.Key))
                                {
                                    List<string> newstr = new List<string>();
                                    foreach (var z in x.Value[j])
                                    {
                                        if (z != Rule.Key)
                                        {
                                            newstr.Add(z);
                                        }
                                    }
                                    if (x.Key != Rule.Key && newstr.Count == 0)
                                        newstr.Add("#");
                                    x.Value.Add(newstr);
                                }
                            }
                        }
                        k = -1;
                    }
                }
            }
        }


        void GetReachable(string start, List<string> Visited)
        {
            Visited.Add(start);
            foreach (var subrule in Rules[start])
            {
                if (subrule.Count == 1 && !Leters.ContainsKey(subrule[0]) && !Visited.Contains(subrule[0]))
                {
                    GetReachable(subrule[0], Visited);
                }
            }
        }


        void removeUnits()
        {
            foreach (var rule in Rules)
            {
                List<string> visited = new List<string>();
                GetReachable(rule.Key, visited);
                visited.Remove(rule.Key);
                foreach (var visit in visited)
                    for (int i = 0; i < Rules[visit].Count; i++)
                    {
                        var subrule = Rules[visit][i];
                        if (subrule.Count != 1 || Leters.ContainsKey(subrule[0]))
                        {
                            rule.Value.Add(subrule);
                        }
                    }
            }
            foreach (var rule in Rules)
                for (int i = 0; i < Rules[rule.Key].Count; i++)
                {
                    var subrule = Rules[rule.Key][i];
                    if (subrule.Count == 1 && !Leters.ContainsKey(subrule[0]))
                    {
                        rule.Value.RemoveAt(i);
                    }
                }
        }
        void inputParser(string inp, bool start)
        {
            string first = "";
            for (int i = 1; inp[i] != '>'; i++)
            {
                first += inp[i].ToString();
            }
            if (start)
                root = first;
            int x = 1;
            while (inp[x] != '-' || inp[x + 1] != '>')
            {
                x++;
            }
            x += 2;
            string outP = "";
            for (int i = x; i < inp.Length; i++)
            {
                if (inp[i] != ' ')
                {
                    outP += inp[i].ToString();
                }
            }
            string[] Output = outP.Split('|');
            List<List<string>> newRule = new List<List<string>>();
            foreach (var str in Output)
            {
                List<string> newGram = new List<string>();
                for (int i = 0; i < str.Length; i++)
                {
                    if (str[i] == '<')
                    {
                        i++;
                        string newStr = "";
                        while (str[i] != '>')
                        {
                            newStr += str[i];
                            i++;
                        }

                        newGram.Add(newStr);

                    }
                    else if (str[i] == '#')
                    {
                        newGram.Add("#");
                    }
                    else
                    {
                        string newletter=str[i].ToString();
                        if (!Leters.ContainsKey(newletter))
                        {
                            Leters.Add(newletter, "l" + Leters.Count.ToString());
                            Rules.Add(Leters[newletter], new List<List<string>>() { new List<string>() { newletter } });
                        }
                        newGram.Add(Leters[newletter]);
                    }
                }

                newRule.Add(newGram);
            }
            Rules.Add(first, newRule);
        }

        string Acceptance(string str)
        {
            int n = str.Length;
            List<string>[,] Matrix = new List<string>[n, n];
            for (int i = 0; i < n; i++)
            {
                for (int j = 0; j < n; j++)
                {
                    Matrix[i, j] = new List<string>();
                }
            }
            for(int i = 0; i < n; i++)
            {
                foreach (var Rule in Rules)
                {
                    foreach (var sR in Rule.Value)
                    {
                        if (sR.Count == 1 && sR[0] == str[i].ToString())
                        {
                            Matrix[i, i].Add(Rule.Key);
                        }
                    }
                }
            }
            for (int l = 2; l <= n; l++)
            {
                for (int i = 0; i <= n - l; i++)
                {
                    int j = i + l - 1;
                    for (int k = i; k < j; k++)
                    {
                        foreach (var rule in Rules)
                        {
                            foreach (var sR in rule.Value)
                            {
                                if(i == 0 && j == 1)
                                {

                                }
                                if (sR.Count == 2 && Matrix[i, k].Contains(sR[0]) && Matrix[k + 1, j].Contains(sR[1]))
                                {
                                    Matrix[i, j].Add(rule.Key);
                                    break;
                                }
                            }
                        }
                    }
                }
            }
            return Matrix[0, n - 1].Contains(root) ? "Accepted" : "Rejected";

            if (Matrix[0, n - 1].Contains(root))
            {
                return "Accepted";
            }
            else
            {
                return "Rejected";
            }
        }
    }
    class Program
    {
        static void Main(string[] args)
        {
            Grammer x = new Grammer();
        }
    }
}
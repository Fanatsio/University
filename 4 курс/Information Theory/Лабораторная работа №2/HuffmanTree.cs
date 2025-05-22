using System.Collections.Generic;
using System.Linq;

namespace Kod
{
    internal class HuffmanTree
    {
        private readonly List<Node> nodes = new List<Node>();
        public Node Root { get; set; }
        public Dictionary<char, double> Frequencies = new Dictionary<char, double>();

        public void Build(Dictionary<char, double> organ_harvest)
        {
            Frequencies = organ_harvest;

            foreach (KeyValuePair<char, double> symbol in Frequencies)
            {
                nodes.Add(new Node() { Symbol = symbol.Key, Frequency = symbol.Value });
            }

            while (nodes.Count > 1)
            {
                List<Node> orderedNodes = nodes.OrderBy(node => node.Frequency).ToList();

                if (orderedNodes.Count >= 2)
                {
                    List<Node> taken = orderedNodes.Take(2).ToList();

                    Node parent = new Node()
                    {
                        Symbol = '*',
                        Frequency = taken[0].Frequency + taken[1].Frequency,
                        Left = taken[0],
                        Right = taken[1]
                    };

                    nodes.Remove(taken[0]);
                    nodes.Remove(taken[1]);
                    nodes.Add(parent);
                }

                this.Root = nodes.FirstOrDefault();
            }
        }

        public Dictionary<char, string> ReturnAlphabet()
        {
            Dictionary<char, string> codes = new Dictionary<char, string>();
            if (Root == null)
                return codes;

            foreach (KeyValuePair<char, double> symbol in Frequencies)
            {
                List<bool> encodedSymbol = Root.Traverse(symbol.Key, new List<bool>());
                if (encodedSymbol != null)
                {
                    codes[symbol.Key] = string.Concat(encodedSymbol.Select(x => x ? "1" : "0"));
                }
            }
            return codes;
        }
    }
}
using System;
using System.Collections.Generic;
using System.Linq;

namespace Kod
{
    public class ShannonFanoEncoder
    {
        private readonly Dictionary<char, double> probabilities;
        private readonly Dictionary<char, string> codes;

        public ShannonFanoEncoder(Dictionary<char, double> probabilities)
        {
            this.probabilities = probabilities;
            this.codes = new Dictionary<char, string>();
        }

        public Dictionary<char, string> Encode()
        {
            var sorted = probabilities.OrderByDescending(x => x.Value).ToList();
            if (sorted.Count == 0)
                return codes;

            Fano(0, sorted.Count - 1, sorted);
            return codes;
        }

        private void Fano(int left, int right, List<KeyValuePair<char, double>> sorted)
        {
            if (left < right)
            {
                int middle = FindSplitPoint(left, right, sorted);

                for (int i = left; i <= right; i++)
                {
                    var key = sorted[i].Key;
                    codes[key] = (codes.ContainsKey(key) ? codes[key] : "") + (i <= middle ? "1" : "0");
                }

                Fano(left, middle, sorted);
                Fano(middle + 1, right, sorted);
            }
            else if (left == right)
            {
                var key = sorted[left].Key;
                codes[key] = codes.ContainsKey(key) ? codes[key] : "0";
            }
        }

        private int FindSplitPoint(int left, int right, List<KeyValuePair<char, double>> sorted)
        {
            double totalSum = sorted.Skip(left).Take(right - left + 1).Sum(x => x.Value);
            double leftSum = 0;
            int splitIndex = left;
            double minDifference = double.MaxValue;

            for (int i = left; i < right; i++)
            {
                leftSum += sorted[i].Value;
                double rightSum = totalSum - leftSum;
                double difference = Math.Abs(leftSum - rightSum);
                if (difference < minDifference)
                {
                    minDifference = difference;
                    splitIndex = i;
                }
            }

            return splitIndex;
        }
    }
}
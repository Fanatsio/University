// ReSharper disable All

namespace Lab4.Tests;

public sealed class XunitOrderer : ITestCaseOrderer
{
    public const string OrdererTypeName = "Lab4.Tests.XunitOrderer";

    public const string OrdererAssemblyName = "Lab4.Tests";

    private readonly IMessageSink _messageSink;

    public XunitOrderer(IMessageSink messageSink)
    {
        _messageSink = messageSink;
    }

    public IEnumerable<TTestCase> OrderTestCases<TTestCase>(IEnumerable<TTestCase> testCases) where TTestCase : ITestCase
    {
        if (testCases.TryGetNonEnumeratedCount(out int count) && count is 1)
        {
            return testCases;
        }

        SortedDictionary<uint, TTestCase> sortedTestCases = new();

        foreach (TTestCase testCase in testCases)
        {
            IAttributeInfo[] attributes = testCase.TestMethod.Method.GetCustomAttributes(typeof(XunitOrdererFactAttribute)).ToArray();

            if (attributes is [IAttributeInfo attribute])
            {
                if (attribute.GetNamedArgument<uint>(nameof(XunitOrdererFactAttribute.SequenceNumber)) is uint priority && attribute.GetNamedArgument<bool>(nameof(XunitOrdererFactAttribute.AllowGroup)))
                {
                    if (sortedTestCases.TryAdd(priority, testCase))
                    {
                        continue;
                    }
                }
            }

            _messageSink.OnMessage(new DiagnosticMessage("The test {0} is ignored. Check the «{1}» arguments or presence.", testCase.DisplayName, nameof(XunitOrdererFactAttribute)));
        }

        return sortedTestCases.Values;
    }
}

// ReSharper disable All

namespace Lab4.Tests;

[AttributeUsage(AttributeTargets.Method, AllowMultiple = false)]
public sealed class XunitOrdererFactAttribute : Attribute
{
    public uint SequenceNumber { get; }

    public bool AllowGroup { get; set; }

    public XunitOrdererFactAttribute(uint sequenceNumber)
    {
        SequenceNumber = sequenceNumber;

        AllowGroup = true;
    }
}

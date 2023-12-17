using Iot.Device.OneWire;

bool flag = true;

Console.CancelKeyPress += (sender, eventArgs) =>
{
    flag = false;
};

while (flag)
{
    foreach (var dev in OneWireThermometerDevice.EnumerateDevices())
    {
        string str = $"Name: {dev.DeviceId}";
        Console.WriteLine(str);
        string str2 = $"Temperature: {dev.ReadTemperature().DegreesCelsius:g}";
        Console.WriteLine(str2);
        Console.WriteLine();
    }
}
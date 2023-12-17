using System.Device.I2c;
using Raven.Iot.Device;
using Raven.Iot.Device.Ina219;
using UnitsNet;
using System.Device.Gpio;


if (DeviceHelper.GetIna219Devices() is [I2cConnectionSettings settings])
{
    var calibrator = Ina219Calibrator.Default with
    {
        VMax = ElectricPotential.FromVolts(5),
        IMax = ElectricCurrent.FromAmperes(0.6),
    };

    var ina219 = calibrator.CreateCalibratedDevice(settings);

    using GpioController controller = new();
    int pin = DeviceHelper.WiringPiToBcm(0);

    controller.OpenPin(pin, PinMode.Output);
    controller.Write(pin, PinValue.High);

    var dataReadings = new List<string>
    {
        GetHeaderCSV(
            ina219.ReadBusVoltage(),
            ina219.ReadCurrent(),
            ina219.ReadPower()
            )
    };

    var t = TimeProvider.System.CreateTimer((_) =>
    {
        dataReadings.Add(GetRecordCSV(
            TimeProvider.System.GetLocalNow(),
            ina219.ReadBusVoltage(),
            ina219.ReadCurrent(),
            ina219.ReadPower()));

    }, default, TimeSpan.Zero, TimeSpan.FromSeconds(10));

    await Task.Delay(60000);
    t.Dispose();

    controller.Write(pin, PinValue.Low);
    controller.ClosePin(pin);

    WriteDataToFile(dataReadings);
}

string GetHeaderCSV(ElectricPotential voltage, ElectricCurrent current, Power power)
{
    var abbrVoltage = UnitAbbreviationsCache.Default.GetDefaultAbbreviation(voltage.Unit);
    var abbrCurrent = UnitAbbreviationsCache.Default.GetDefaultAbbreviation(current.Unit);
    var abbrPower = UnitAbbreviationsCache.Default.GetDefaultAbbreviation(power.Unit);
    return $"Date, Time, Voltage, {abbrVoltage}; Current, {abbrCurrent}; Power, {abbrPower}\n";
}

string GetRecordCSV(DateTimeOffset dateTime, ElectricPotential voltage, ElectricCurrent current, Power power)
{
    return $"{dateTime}; {voltage.Value}; {current.Value}; {power.Value}\n";
}

void WriteDataToFile(List<string> data)
{
    string currentDirectory = Directory.GetCurrentDirectory();
    string[] csvFiles = Directory.GetFiles(currentDirectory, "data_*.csv");
    using var sw = new StreamWriter($"data_{csvFiles.Length}.csv");

    foreach (string record in data)
    {
        sw.Write(record);
    }
}

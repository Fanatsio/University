using Raven.Iot.Device;
using Raven.Iot.Device.GpioExpander;
using System.Device.I2c;
using Iot.Device.RotaryEncoder;
using System.Device.Gpio;
using UnitsNet;

const int D0 = 24;
const int D1 = 25;
const int D2 = 0;

if (DeviceHelper.GetGpioExpanderDevices() is [I2cConnectionSettings settings])
{
    using GpioExpander gpioExpander = new(settings);
    CalibrateGpioExpander(gpioExpander);

    using ScaledQuadratureEncoder encoder = InitializeEncoder();
    encoder.ValueChanged += (o, e) =>
    {
        gpioExpander.WriteAngle(D2, Angle.FromDegrees(e.Value));
    };

    Console.ReadKey();
}

void CalibrateGpioExpander(GpioExpander gpioExpander)
{
    gpioExpander.Calibrate(Angle.FromDegrees(180), TimeSpan.FromMicroseconds(600), TimeSpan.FromMicroseconds(2600));
}

ScaledQuadratureEncoder InitializeEncoder()
{
    return new ScaledQuadratureEncoder(
        pinA: DeviceHelper.WiringPiToBcm(D0),
        pinB: DeviceHelper.WiringPiToBcm(D1),
        PinEventTypes.Falling,
        pulsesPerRotation: 20,
        pulseIncrement: 1,
        rangeMin: 0.0,
        rangeMax: 180.0)
    {
        Debounce = TimeSpan.FromMilliseconds(2)
    };
}



using Raven.Iot.Device;
using Raven.Iot.Device.GpioExpander;
using System;
using System.Device.Gpio;
using System.Device.I2c;
using Iot.Device.RotaryEncoder;
using UnitsNet;

class Program
{
    const int D0 = 24;
    const int D1 = 25;
    const int D2 = 0;
    const int D3 = 1;

    static void Main()
    {
        if (DeviceHelper.GetGpioExpanderDevices() is [I2cConnectionSettings settings])
        {
            using GpioExpander gpioExpander = InitializeGpioExpander(settings);
            using ScaledQuadratureEncoder encoder = InitializeRotaryEncoder(D0, D1);
            encoder.ValueChanged += Encoder_ValueChanged;
            Console.ReadKey();
        }
    }

    static GpioExpander InitializeGpioExpander(I2cConnectionSettings settings)
    {
        using GpioExpander gpioExpander = new(settings);
        gpioExpander.SetPwmFrequency(Frequency.FromKilohertz(25));
        return gpioExpander;
    }

    static ScaledQuadratureEncoder InitializeRotaryEncoder(int pinA, int pinB)
    {
        ScaledQuadratureEncoder encoder = new ScaledQuadratureEncoder(
            pinA: DeviceHelper.WiringPiToBcm(pinA),
            pinB: DeviceHelper.WiringPiToBcm(pinB),
            PinEventTypes.Falling,
            pulsesPerRotation: 20,
            pulseIncrement: 1,
            rangeMin: 0.0,
            rangeMax: 255.0);

        encoder.Debounce = TimeSpan.FromMilliseconds(2);
        return encoder;
    }

    static void Encoder_ValueChanged(object sender, EncoderValueChangedEventArgs e)
    {
        int analogValue = (int)e.Value;
        gpioExpander.AnalogWrite(D2, analogValue);
        gpioExpander.AnalogWrite(D3, analogValue);
    }
}

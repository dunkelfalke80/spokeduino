using System;
using System.IO.Ports;
using System.Collections.Generic;
using System.Globalization;

class Program
{
    static void Main(string[] args)
    {
        string portName = "COM3";
        int baudRate = 9600;

        using (SerialPort serialPort = new SerialPort(portName, baudRate))
        {
            serialPort.Open();

            List<(float tension, float deflection)> measurements = new List<(float, float)>();
            float[] tensions = { 1500, 1400, 1300, 1200, 1100, 1000, 900, 800, 700, 600, 500, 400 };
            int tensionIndex = 0;

            while (tensionIndex < tensions.Length)
            {                
                Console.WriteLine($"Auf {tensions[tensionIndex]} N spannen, Leertaste wenn der Wert passt.");
                string data = string.Empty;
                while (true)
                {                    
                    try
                    {
                        data = serialPort.ReadLine();
                    }
                    catch (Exception)
                    {
                    }
                    Console.Write($"{data}\r");                    
                    if (Console.KeyAvailable)
                    {
                        var key = Console.ReadKey(true).Key;
                        if (key == ConsoleKey.Spacebar)
                        {                            
                            Console.WriteLine($"Arduino: {data}");

                            if (ParseGaugeValue(data, out float deflection))
                            {
                                measurements.Add((tensions[tensionIndex], deflection));
                                Console.WriteLine($"{tensions[tensionIndex]} N = {deflection} mm");
                                tensionIndex++;
                                break;
                            }
                            else
                            {
                                Console.WriteLine("WTF?");
                            }
                        }
                        else if (key == ConsoleKey.Escape)
                        {
                            Console.WriteLine("Bye bye.");
                            return;
                        }
                    }                    
                }
                
            }

            SaveMeasurements(measurements);
        }
    }

    static bool ParseGaugeValue(string data, out float deflection)
    {
        deflection = 0.0f;
        try
        {
            string[] parts = data.Split(':');
            if (parts.Length == 2 && parts[0] == "1")
            {
                deflection = float.Parse(parts[1], CultureInfo.InvariantCulture);
                return true;
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Fehler beim Parsen von {data}: {ex.Message}");
        }
        return false;
    }

    static void SaveMeasurements(List<(float tension, float deflection)> measurements)
    {
        string fileName = @"c:\temp\messung.csv";
        using (var writer = new System.IO.StreamWriter(fileName))
        {
            writer.WriteLine("Newton;mm");
            foreach (var (tension, deflection) in measurements)
                writer.WriteLine($"{tension};{deflection}");
        }
    }
}

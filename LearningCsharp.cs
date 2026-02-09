using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.NetworkInformation;
using System.Runtime.InteropServices.Marshalling;
using System.Threading.Tasks;

namespace api
{
    public class LearningCsharp
    {
        private string name;
        private int weight;
        private byte[] coordinates;

        // конструктор
        public LearningCsharp(string _name, int _waight, byte[] _coordinates)
        {
            System.Console.WriteLine("Object has been created"); // при каждом создании объекта будет выводится надпись
            setValue(_name, _waight, _coordinates);
        }

        // второй конструткор
        public LearningCsharp()
        {

        }

        public void setValue(string _name, int _waight, byte[] _coordinates)
        {
            name = _name;
            weight = _waight;
            coordinates = _coordinates;
        }
    }
};

// создание объекта от класса:
namespace api
{
    LearningCsharp bot = new LearningCsharp("Ришат", 175, new byte[] { 0, 1, 1 });
}
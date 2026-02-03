using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;

namespace api.Models // ← обозначаем простанство имен - это как папка с файлами

{
    public class Stock // фонд (бюджет)
    {
        public int Id { get; set; }

        // Без атрибута (по умолчанию)
        // В БД создастся столбец типа, подходящего для string
        public string Symbol { get; set; } = string.Empty;
        // Без атрибута (по умолчанию)
        public string CompanyName { get; set; } = string.Empty;

        // С атрибутом
        [Column(TypeName = "decimal(18,2)")]
        public decimal Purchase { get; set; } // для цифр валюты (закупка)
                                              // В БД создастся ТОЧНО decimal(18,2) - мы явно указали тип

        [Column(TypeName = "decimal(18,2)")]
        public decimal LastDiv { get; set; } // дивиденды

        public string Industry { get; set; } = string.Empty;

        public long MarkerCap { get; set; } // стоимость компании - long большое число
                                            
        // Один Stock ко многим List<Comment> List - значит 'Динамический массив' для коллекция комментриев
        public List<Comment> Comments { get; set; } = new List<Comment>();
    }
}
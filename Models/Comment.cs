using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;

// фонд
namespace api.Models
{
    public class Comment
    {
        public int Id { get; set; }
        public string Title { get; set; } = string.Empty;
        public string Content { get; set; } = string.Empty;
        public DateTime CreatedOn { get; set; } = DateTime.Now;
        
        // Id для связывания Stock (один) ко Comment (многие)
        [ForeignKey(nameof(Stock))]  //! ← ЯВНОЕ указание, что это внешний ключ! Это лучшая практика, Но можно без него
        public int? StockId { get; set; } // ? - МОЖЕТ быть null (может не быть значения)
        // отношение этой таблицы к таблице Stock с помщью навигации то таблицам,
        // то есть, мы должны найти Stock и сязаться с ним
        public Stock? Stock { get; set; }
        // ↑ Навигационное свойство (Navigation Property)
        // ↑ Позволяет обращаться к связанному объекту Stock
        // ↑ Может быть null → связь может отсутствовать



    }
}
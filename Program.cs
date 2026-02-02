var builder = WebApplication.CreateBuilder(args);

// Добавь эти строки
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Настройка Swagger (всегда, а не только в Development)
app.UseSwagger();
app.UseSwaggerUI();

app.UseHttpsRedirection();

app.Run();
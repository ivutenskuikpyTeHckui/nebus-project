# Client API

Асинхронные платежи. API пишет платёж и outbox в одной транзакции, relay публикует `payments.new`, consumer эмулирует шлюз и шлёт webhook.

## Запуск

```bash
docker compose -f docker-compose.dev.yml up --build
```

- API: http://localhost:8081/docs
- RabbitMQ: http://localhost:15672 (`root` / `root`)
- API key: `dev-api-key`


Очереди: `payments.new`, `payments.new.retry.1000`, `payments.new.retry.2000`, `payments.new.dlq`.

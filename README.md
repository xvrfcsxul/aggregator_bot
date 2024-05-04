**Запуск**
- Клоинровать проект
```bash
git clone https://github.com/xvrfcsxul/aggregator_bot.git
```
- Перейти в infra
```bash
cd aggregator_bot/infra
```
- В файл .env записать токен тг бота
- Запустить docker-compose
```bash
docker-compose up -d
```
- Заполнить БД
```bash
docker exec -it fastapi_backend bash -c "poetry run python load_data.py"
```
- Можно переходить в тг и отправлять боту запрос

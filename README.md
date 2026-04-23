# HotelFlow

## Что это вообще такое
HotelFlow — это обновлённая full-stack система бронирования отеля на Django + React. Я взял старый проект, вычистил древности, обновил стек, переделал структуру, освежил UI и сделал так, чтобы это выглядело уже не как привет из прошлого, а как нормальный современный курсовой проект.

## Что умеет проект
1. Регистрация пользователя
2. Логин через JWT
3. Просмотр списка комнат
4. Просмотр детальной страницы комнаты
5. Фильтрация комнат по цене, названию и вместимости
6. Создание бронирования
7. Проверка корректности дат и вместимости
8. Админ-дэшборд для отчётов
9. Check-in и checkout логика
10. DAO-классы для CRUD-операций
11. Unit tests для model methods
12. Responsive интерфейс
13. Сообщения об ошибках при неправильном вводе
14. UML class diagram
15. Weekly meeting documentation

## Стек
- Backend: Django 5.2, Django REST Framework, SimpleJWT
- Frontend: React 19, Vite, React Router
- Database: SQLite
- Images: Pillow

## MVC
### Model
Модели лежат в `hotel_app/models.py`.

### View
Интерфейс лежит в `src/`.

### Controller
Контроллерная логика находится во views и API endpoints.

## DAO classes
- `CategoryDAO`
- `RoomDAO`
- `BookingDAO`

Файл: `hotel_app/services/dao.py`

## Таблицы базы данных
- Category
- Room
- Booking
- CheckIn
- Amenity
- RoomImage

## 5 отчётов из базы данных
- Bookings by category
- Top rooms by bookings
- Room performance
- Latest bookings
- Status breakdown

Endpoint: `GET /api/dashboard/reports/`

## Team Members List
- Ulanbekov Ramazan
- Turarov Zhandar
- Kyrmanchieva Aidai

## Roles of Group Members
- Ulanbekov Ramazan — backend refactor, frontend redesign, documentation, integration
- Turarov Zhandar - database filling, testing, screenshots, demo preparation
- Kyrmanchieva Aidai — presentation, UML polishing, QA section preparation


## Screenshots
### Home
![Home](docs/screenshots/home.png)
<img width="1780" height="892" alt="image" src="https://github.com/user-attachments/assets/15b44b32-b034-4b5d-82c8-faea1cf47a46" />

### Rooms
![Rooms](docs/screenshots/rooms.png)
<img width="1537" height="562" alt="image" src="https://github.com/user-attachments/assets/28367e5f-a952-47c8-ad29-df9bbcd54204" />

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)
<img width="1501" height="813" alt="image" src="https://github.com/user-attachments/assets/2071e2c0-05b9-4870-83bf-f3155a0f77da" />

## UML Class Diagram
[docs/UML.md](docs/UML.md)
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/e8c523d7-fc7e-4329-b1cf-5015c3f9281b" />

## Weekly Meeting Documentation
[docs/weekly-meetings.md](docs/weekly-meetings.md)

## Reports Documentation
[docs/reports.md](docs/reports.md)

## Presentation Materials
[docs/presentation-outline.md](docs/presentation-outline.md)

## Структура проекта
```text
hotel_app/
accounts/
hotel_reservation_site/
src/
docs/
```

## Как запускать
### Backend
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend
```bash
npm install
npm run dev
```

### Адреса
- Backend API: `http://127.0.0.1:8000/api/`
- Frontend: `http://127.0.0.1:5173/`
- Admin panel: `http://127.0.0.1:8000/admin/`


## Media links
- UML: [docs/UML.md](docs/UML.md)
- Weekly meetings: [docs/weekly-meetings.md](docs/weekly-meetings.md)
- Reports: [docs/reports.md](docs/reports.md)
- Presentation outline: [docs/presentation-outline.md](docs/presentation-outline.md)
- Screenshots: `docs/screenshots/`

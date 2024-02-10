from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from sqlalchemy.orm import declarative_base

# Загрузка переменных окружения из файла .env
load_dotenv()

# Использование переменной окружения
database_url = os.getenv('DATABASE_URL')

# Создание базового класса для определения моделей данных
Base = declarative_base()


# Создание модели данных
class User(Base):
    __tablename__ = 'user'

    UserID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String, nullable=False)
    LastName = Column(String, nullable=False)
    Password = Column(String, nullable=True)
    Email = Column(String)
    VKID = Column(String, nullable=True)

# Создаем функцию движка базы данных
def create_engine(database_url: str):
    """
    Создаем движок БД
    :param database_url: путь к базе данных
    :return: объект движка базы данных
    """
    engine = create_engine(database_url, echo=True)
    return engine

# Создаем сессию
def get_session(engine):
    """
    Создает и возвращает объект сессии SQLAlchemy на основе переданного объекта движка базы данных.
    :param engine: объект движка базы данных
    :return: объект сессии SQLAlchemy
    """
    # Создаем фабрику сессий
    Session = sessionmaker(bind=engine)
    # Создаем сессию
    session = Session()
    return session

# Добавляем одного нового пользователя
def add_user(session, user_data: dict):
    """
    Добавляет нового пользователя в базу данных.
    :param session: объект сессии SQLAlchemy
    :param user_data: словарь с данными нового пользователя (FirstName, LastName, Password, Email, VKID)
    :return: ID добавленного пользователя
    """
    # Создаем экземпляр модели User на основе переданных данных
    new_user = User(**user_data)

    # Добавляем пользователя в сессию
    session.add(new_user)

    # Фиксируем изменения в базе данных
    session.commit()

    # Возвращаем ID добавленного пользователя
    return new_user.UserID

# Выводим пользователя по UserID
def get_user_by_id(session, user_id: int):
    """
    Читает пользователя из базы данных по его ID
    :param session: объект сессии SQLAlchemy
    :param user_id: ID пользователя
    :return: словарь с данными пользователя
    """
    # Выполняем запрос к таблице пользователей
    user = session.query(User).filter_by(UserID=user_id).first()

    # Проверяем, был ли найден пользователь
    if user:
        # Преобразуем данные пользователя в словарь
        user_data = {
            'UserID': user.UserID,
            'FirstName': user.FirstName,
            'LastName': user.LastName,
            'Password': user.Password,
            'Email': user.Email,
            'VKID': user.VKID
        }
        return user_data
    else:
        return None

# Получаем всех пользователей
def get_all_users(session):
    """
    Получаем всех пользователей
    :param session: объект сессии SQLAlchemy
    :return: список словарей с данными всех пользователей
    """
    # Формируем запрос к таблице пользователей
    query = session.query(User)

    users = []

    for user in query:
        user_data = {
            'UserID': user.UserID,
            'FirstName': user.FirstName,
            'LastName': user.LastName,
            'Password': user.Password,
            'Email': user.Email,
            'VKID': user.VKID
        }
        users.append(user_data)
    return users

# Обновляем данные пользователя
def update_user(session, user_data: dict):
    """
    Обновляет данные пользователя в базе данных.
    :param session: объект сессии SQLAlchemy
    :param user_data: словарь с обновленными данными пользователя
    :return ID обновленного пользователя
    """
    # Получаем ID пользователя из словаря user_data
    user_id = user_data.get('UserID')
    # Проверяем, существует ли пользователь с таким ID в базе данных
    existing_user = session.query(User).filter_by(UserID=user_id).first()

    if existing_user:
        # Обновляем поля пользователя данными из словаря user_data
        for key, value in user_data.items():
            setattr(existing_user, key, value)

        # Зафиксировать изменения в базе данных
        session.commit()
        return user_id
    else:
        return None

# Удаление одного пользователя по ID
def delete_user_by_id(session, user_id: int):
    """
    Удаляет пользователя из базы данных по его ID.
    :param session: объект сессии SQLAlchemy
    :param user_id: ID пользователя
    :return: ID удаленного пользователя
    """
    # Находим пользователя по его ID
    user_to_delete = session.query(User).filter_by(UserID=user_id).first()

    # Проверяем, был ли найден пользователь с указанным ID
    if user_to_delete:
        # Удаляем пользователя из сессии
        session.delete(user_to_delete)

        # Зафиксировать изменения в базе данных
        session.commit()

        # Возвращаем ID удаленного пользователя
        return user_id
    else:
        # Если пользователь с указанным ID не найден, возвращаем None
        return None

# испортируем модули стандартнй библиотеки uuid и datetime
import uuid
import datetime

# импортируем библиотеку sqlalchemy и некоторые функции из нее
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

class User(Base):
    """
    Описывает структуру таблицы athelete, содержащую данные об атлетах
    """
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)


class Athelete(Base):
    """
    Описывает структуру таблицы athelete, содержащую данные об атлетах
    """
    __tablename__ = 'athelete'

    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    weight = sa.Column(sa.Integer)
    name = sa.Column(sa.Text)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

def connect_db(db_path):
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(db_path)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()


def request_data(first_name=None, last_name=None, gender=None, email=None, birthdate=None, height=None):
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    if first_name is None:
        first_name = input("Введите имя: ")
    if last_name is None:
        last_name = input("Введите фамилию: ")
    if gender is None:
        gender = input("Пол: Male/Female")
    if email is None:
        email = input("Введите адрес электронной почты: ")
    if birthdate is None:
        birthdate = input("Введите дату рождения в формате ГГГГ-ММ-ДД: ")
    if height is None:
        height = input("Рост в метрах:")
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    return user


def create_new_user(user, session):
    """Создание пользователя
    Args:
        user: пользователь
        session: соединение с БД
    """
    session.add(user)
    session.commit()
    print('Добавлен новый пользователь')

def find_user(user_id, session):
    """Поиск пользователя"""
    athelete_query = session.query(Athelete)
    find_athelete = athelete_query.filter(Athelete.id == user_id).all()[0]
    if not find_athelete:
        print('Не найден спортсмен с указанным идентификатором')
        return 0
    atheletes_list = athelete_query.filter(Athelete.id != user_id).all()
    similar_height = abs(find_athelete.height - atheletes_list[0].height)
    similar_height_athelete = atheletes_list[0]
    find_birthdate = datetime.datetime.strptime(find_athelete.birthdate, '%Y-%m-%d')
    athelte_birthdate = datetime.datetime.strptime(atheletes_list[0].birthdate, '%Y-%m-%d')
    similar_birthdate = abs(find_birthdate - athelte_birthdate)
    similar_birthdate_athelete = atheletes_list[0]
    for athelete in atheletes_list[1:]:
        if not athelete.height:
            athelete.height = 0
        if abs(find_athelete.height - athelete.height) < similar_height:
            similar_height_athelete = athelete
            similar_height = abs(find_athelete.height - athelete.height)
        athelte_birthdate = datetime.datetime.strptime(athelete.birthdate, '%Y-%m-%d')
        if abs(find_birthdate - athelte_birthdate) < similar_birthdate:
            similar_birthdate_athelete = athelete
            similar_birthdate = abs(find_birthdate - athelte_birthdate)

    print(f'Ближайший к пользователю по росту атлет:{similar_height_athelete.id} {similar_height_athelete.name}')
    print(f'Ближайший к пользователю по дате рождения атлет:{similar_birthdate_athelete.id} {similar_birthdate_athelete.name}')

if __name__ == '__main__':
    db = connect_db(db_path=DB_PATH)
    user = request_data(first_name='Vera', last_name='Basko', gender='Female', email='vr.basko@gmail.com',
                        birthdate='1995-06-16', height=1.64)
    #create_new_user(user, db)
    find_user(55, db)
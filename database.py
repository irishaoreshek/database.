import pymysql
import time

from aiogram.types import Message

from config_data.config import Config, load_config

config: Config = load_config('\.env')


def connection(config: Config) -> pymysql.connect:
    return pymysql.connect(host=config.database.host, user=config.database.user,
                           passwd=config.database.password, database=config.database.database,
                           port=int(config.database.port))


def addUser(msg: Message) -> bool:
    first_name = msg.from_user.first_name
    last_name = msg.from_user.last_name
    print(first_name)
    print(last_name)
    print(msg.from_id, msg.from_user.id)
    con = connection(config)
    try:
        with con.cursor() as cursor:
            insert_query = f'INSERT INTO users_game (`idUser`, `First_Name`, `Last_name`, `secret_number`, `attempts`, `wins`, `total_games`, `in_game`)'\
            f'VALUES({msg.from_user.id}, "{first_name}", "{last_name}", null, null, 0, 0, False);'
            cursor.execute(insert_query)
            con.commit()
        return True
    except Exception as ex:
        print(ex)
        print("Ошибка работы бд")
    finally:
        return False

def SelectOneUser(msg: Message):
    try:
        con = connection(config)
        with con.cursor() as cursor:
            select_user = "SELECT * FROM users_game"\
            f" WHERE idUser = {msg.from_user.id}"
            cursor.execute(select_user)
            return cursor.fetchone()
    except Exception as ex:
        print(ex)

def UpdateUser(msg: Message, secret_number: int = None, attempts: int = None, wins: int = None, total_games: int = None, in_game: bool = None):
    try:
        con = connection(config)
        if secret_number is not None:
            with con.cursor() as cursor:
                update_user = f"UPDATE users_game SET secret_number = {secret_number} WHERE idUser = {msg.from_user.id}"
                cursor.execute(update_user)
                con.commit()
        
        if attempts is not None:
            with con.cursor() as cursor:
                update_user = f"UPDATE users_game SET attempts = {attempts} WHERE idUser = {msg.from_user.id}"
                cursor.execute(update_user)
                con.commit()
        
        if wins is not None:
            with con.cursor() as cursor:
                update_user = f"UPDATE users_game SET wins = {wins} WHERE idUser = {msg.from_user.id}"
                cursor.execute(update_user)
                con.commit()
            
        if total_games is not None:
            with con.cursor() as cursor:
                update_user = f"UPDATE users_game SET total_games = {total_games} WHERE idUser = {msg.from_user.id}"                    
                cursor.execute(update_user)
                con.commit()
            
        if in_game is not None:
            with con.cursor() as cursor:
                update_user = f"UPDATE users_game SET in_game = {in_game} WHERE idUser = {msg.from_user.id}"
                cursor.execute(update_user)
                con.commit()
    except Exception as ex:
        print(ex)

def FirstFiveUsers(msg: Message) -> str:
    first_five: str = "Tоп-игроков\n"
    try:
        con = connection(config)
        with con.cursor() as cursor:
            sortusers = "select * from users_game order by wins DESC limit 5"
            cursor.execute(sortusers)
            rows = cursor.fetchall()
            count: int = 1
            for row in rows:
                first_five += f"{count}). " + f"{row[3]} {row[2]} --- Сыграно: " + f'{row[7]}, Побед: {row[6]};\n'
                count += 1
        return first_five
    except Exception as ex:
        print(ex)
    finally:
        return first_five

def isFindUser(id: int):
    try:
        con = connection(config)
        with con.cursor() as cursor:
            select_user = "SELECT * FROM users_game"\
                    f" WHERE idUser = {id}"
            cursor.execute(select_user)
            if len(cursor.fetchall()) > 0:
                return False
        return True
    finally:
        return False

def addHistory(msg: Message, iswin: int):
    try:
        con = connection(config)
        named_tuple = time.localtime() # получить struct_time
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
        with con.cursor() as cursor:
            add_history = f'INSERT INTO history (`id_user`, `old_game`, `time`) '\
            f'VALUES ({msg.from_id}, {iswin}, "{time_string}");'
            cursor.execute(add_history)
            con.commit()
    except Exception as ex:
        print(ex)

def updateKD(msg: Message):
    count_win = _counWinGame(msg)
    count_game = _countGame(msg)
    print(count_game, count_win, count_win/count_game)
    try:
        con = connection(config)
        with con.cursor() as cursor:
            update_kd = f'UPDATE kd SET total_games = {count_game}, total_wins = {count_win}, ratio = {count_win/count_game} WHERE id=1;'
            cursor.execute(update_kd)
            con.commit()
    except Exception as ex:
        print(ex, "updateKD")

def _counWinGame(msg: Message) -> int:
    try:
        con = connection(config)
        with con.cursor() as cursor:
            count_win_game = 'select * from history where old_game=1;'
            count = cursor.execute(count_win_game)
            print("Победныx игр: ",count)
            return count
    except Exception as ex:
        print(ex)

def _countGame(msg: Message) -> int:
    try:
        con = connection(config)
        with con.cursor() as cursor:
            count_game = 'select * from history;'
            count = cursor.execute(count_game)
            print("Всего игр", count)
            return count
    except Exception as ex:
        print(ex)

def stringKD(msg: Message):
    try:
        con = connection(config)
        string = "Статистика игр всего сервера:\n"
        with con.cursor() as cursor:
            string_kd = "SELECT * FROM kd WHERE id=1;"
            cursor.execute(string_kd)
            data = cursor.fetchone()
            string += f"Всего игр сыграно на сервере: {data[1]}\n\n"
            string += f"Всего побед на сервере: {data[2]}\n\n"
            string += f"Побед/кол-во игр: {data[3]}\n"       
        return string
    except Exception as ex:
        print(ex)
    finally:
        return string
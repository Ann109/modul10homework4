import time
from threading import Thread
from time import sleep
from random import randint
import random
from queue import Queue

class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

class Guest(Thread):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def run(self):
        pause = random.randint(3, 10)
        sleep(pause)

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = list(tables)

    def guest_arrival(self, *guests):
        for guest in guests:
            # TODO: Не проверять каждый раз свободный стол, а просто запихнуть 5 гостей за столы,
            # а потом в очередь
            free_table = next((x for x in self.tables if x.guest is None), None)
            if free_table is not None:
                free_table.guest = guest
                guest.start()
                print(f'{guest.name} сел за стол {free_table.number}')
            else:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')

    def discuss_guests(self):
        while self.queue.empty() is False or any(x.guest is not None for x in self.tables):
            for table in self.tables:
                if table.guest is not None and table.guest.is_alive() is False:
                    print(f'{table.guest.name} покушал и ушел')
                    table.guest = None

            if self.queue.empty() is False:
                free_table = next((x for x in self.tables if x.guest is None), None)
                if free_table is not None:
                    guest = self.queue.get()
                    free_table.guest = guest
                    guest.start()
                    print(f'{guest.name} вышел(-ла) из очереди и сел(-а) за стол {free_table.number}')


if __name__ == '__main__':
    # Создание столов
    tables = [Table(number) for number in range(1, 6)]
    # Имена гостей
    guests_names = [
        'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
        'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
    ]
    # Создание гостей
    guests = [Guest(name) for name in guests_names]
    # Заполнение кафе столами
    cafe = Cafe(*tables)
    # Приём гостей
    cafe.guest_arrival(*guests)
    # Обслуживание гостей
    cafe.discuss_guests()

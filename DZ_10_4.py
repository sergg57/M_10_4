import threading
from time import sleep
from random import randint
import queue


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        time_to_eat = randint(3, 10)
        sleep( time_to_eat)
        print(f'{self.name} его(её) время еды {time_to_eat} истекло ')
        for table in cafe.tables:
            if table.guest == self.name:
                table.guest = None
                print(f'Стол {table.number} свободен')


class Cafe():
    def __init__(self, *tables):
        self.tables = list(tables)
        self.queue = queue.Queue()

    def guest_arrival(self, *guests):
        for guest in guests:
            # Ищем свободный стол
            # free_table = next((table for table in self.tables if table.guest is None), None)
            # if free_table:
            #     free_table.guest = guest
            #     guest.start()
            #     print(f"{guest.name} сел(-а) за стол номер {free_table.number}")
            # else:
            #     self.queue.put(guest)
            #     print(f"{guest.name} в очереди")


            busy_table_counter = 0
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    print(f'{guest.name} сел(-а) за стол номер {table.number}')
                    guest.start()
                    break
                else:
                    busy_table_counter += 1
                if busy_table_counter == len(self.tables):
                    self.queue.put(guest)
                    print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest for table in self.tables):
            for table in self.tables:
                guest = table.guest
                if guest and not guest.is_alive():
                    print(f"{guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None

                    if not self.queue.empty():
                        next_guest = self.queue.get()
                        table.guest = next_guest
                        next_guest.start()
                        print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")

            sleep(1)


if __name__ == '__main__':
    tables = [Table(number) for number in range(1, (randint(1, 6) + 1))]
    print(f'В кафе {len(tables)} столов')

    guest_name = ['Maria', 'Oleg', 'Vakhtdang', 'Sergey', 'Darya', 'Arman', 'Vitoria',
                  'Nikita', 'Galina', 'Pavel', 'Ilia', 'Alexandra']
    print(f'Список гостей {len(guest_name)} {guest_name}')

    guests = [Guest(name) for name in guest_name]
    cafe = Cafe(*tables)
    cafe.guest_arrival(*guests)
    cafe.discuss_guests()


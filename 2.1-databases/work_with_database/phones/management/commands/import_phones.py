import csv

from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    help = 'Выполняет перенос данных из csv-файла в модель Phone.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='Указывает путь к файлу csv')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file_path']

        try:
            with open(csv_file_path, 'r') as file:
                phones = list(csv.DictReader(file, delimiter=';'))

            for phone in phones:
                try:
                    phone_model = Phone(
                        name=phone['name'],
                        image=phone['image'],
                        price=phone['price'],
                        release_date=phone['release_date'],
                        lte_exists=phone['lte_exists']
                    )
                    phone_model.save()
                except KeyError as e_key:
                    print(f'Ошибка: {e_key}')
                except Exception as ex:
                    print(f'Ошибка: {ex}')

        except FileNotFoundError:
            print(f'Файл по пути: {csv_file_path} не существует.')
        except Exception as e:
            print(f'Ошибка: {e}')

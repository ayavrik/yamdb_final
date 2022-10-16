from django.apps import apps
from django.core.management.base import BaseCommand
from django.utils.module_loading import import_string

from import_export.formats import base_formats
from import_export.resources import modelresource_factory


class Command(BaseCommand):
    help = 'Create model objects from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='csv file path')
        parser.add_argument('app_name', type=str, help='app name')
        parser.add_argument('model_name', type=str, help='model name')
        parser.add_argument(
            '--resource_class',
            type=str,
            help='Resource class as dotted path: app.resources.ModelResource'
        )

    @staticmethod
    def get_resource_class(app_name, model_name, resource_class):
        if not resource_class:
            model = apps.get_model(app_name, model_name)
            return modelresource_factory(model=model)
        else:
            return import_string(resource_class)

    def handle(self, *args, **options):
        file_path = options['path']
        file_format = base_formats.CSV()
        resource_class = self.get_resource_class(
            options.get('app_name'),
            options.get('model_name'),
            options.get('resource_class')
        )
        resource = resource_class()
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            data = csv_file.read()
            dataset = file_format.create_dataset(data)
            self.stdout.write(
                self.style.MIGRATE_HEADING('\nЗагрузка файла: ') + file_path
            )
            result = resource.import_data(dataset)
            self.stdout.write(f'Количество строк: {result.total_rows}')
            if result.has_errors():
                self.stdout.write(self.style.ERROR('Критические ошибки:'))
                for error in result.base_errors:
                    self.stdout.write(self.style.ERROR(error.error))
                for line, errors in result.row_errors():
                    for error in errors:
                        self.stdout.write(self.style.ERROR(
                            f'  Номер строки: {line} - '
                            f'{error.error}')
                        )
                self.stdout.write(self.style.ERROR('Данные не загружены'))
            elif result.has_validation_errors():
                self.stdout.write(self.style.ERROR('Ошибки валидации:'))
                for invalid_row in result.invalid_rows:
                    self.stdout.write(
                        self.style.ERROR(f'  Номер строки: '
                                         f'{invalid_row.number}')
                    )
                    for field, errors in invalid_row.error:
                        self.stdout.write(
                            self.style.ERROR(f'    Поле: {field} - '
                                             f'{", ".join(errors)}')
                        )
                self.stdout.write(self.style.ERROR(
                    f'Загружено {len(result.valid_rows())} из '
                    f'{result.total_rows} строк\n'
                    f'Создано объектов: {result.totals.get("new")}, '
                    f'Обновлено: {result.totals.get("update")}, '
                    f'Ошибок валидации: {result.totals.get("invalid")}')
                )
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'Данные успешно загружены в модель '
                    f'{options["model_name"]}\n'
                    f'Создано объектов: {result.totals.get("new")}, '
                    f'Обновлено: {result.totals.get("update")}')
                )
            csv_file.close()

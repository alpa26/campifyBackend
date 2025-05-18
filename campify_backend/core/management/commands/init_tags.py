
from django.core.management.base import BaseCommand
from core.models import Tag

TAGS = [
    'новичок', 'кемпинг', 'опытный', 'профи',
    'пеший', 'сплав', 'фото', 'пещеры', 'релакс',
    '1_день', 'выходные', 'неделя', 'экспедиция',
    'комфорт_авто', 'дикий', 'глэмпинг', 'укрытие',
    'горы', 'вода', 'лес', 'история', 'секретные',
    'взрослые', 'дети', 'с_собакой', 'группа',
    'лето', 'осень', 'зима', 'весна',
    'экстрим', 'природа', 'культура',
    'аренда_снаряжение', 'аренда_кухня', 'аренда_транспорт', 'без_аренды',
    'легко', 'средне', 'сложно', 'транспорт'
]

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        created_count = 0
        for name in TAGS:
            tag, created = Tag.objects.get_or_create(name=name)
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f"Добавлено {created_count} новых тегов."))

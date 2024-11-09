from typing import Optional

from django.db import models
from django.utils import timezone


class Reference(models.Model):
    code = models.CharField(
        max_length=100,
        db_index=True,
        unique=True,
        verbose_name='Код',
    )
    name = models.CharField(
        max_length=300,
        verbose_name='Наименование',
    )
    description = models.TextField(
        default='',
        verbose_name='Описание',
    )

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'

    def __str__(self) -> str:
        return f'{self.code} - {self.name}'


class ReferenceVersionQuerySet(models.QuerySet):
    def active_version(self) -> Optional['ReferenceVersion']:
        """Возвращает активную версию"""
        return self.filter(
            start_date__lte=timezone.now().date()
        ).order_by('-start_date').first()


class ReferenceVersion(models.Model):
    reference = models.ForeignKey(
        Reference,
        on_delete=models.CASCADE,
        related_name='versions',
        verbose_name='Справочник',
    )
    code = models.CharField(
        max_length=50,
        verbose_name='Версия',
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата начала действия версии',
    )

    class Meta:
        verbose_name = 'Версия справочника'
        verbose_name_plural = 'Версии справочников'
        unique_together = (
            ('reference', 'code'),
            ('reference', 'start_date'),
        )

    objects = ReferenceVersionQuerySet.as_manager()

    def __str__(self) -> str:
        return f'{self.reference_id} - {self.code}'


class ReferenceElement(models.Model):
    version = models.ForeignKey(
        ReferenceVersion,
        on_delete=models.CASCADE,
        related_name='elements',
        verbose_name='Версия'
    )
    code = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Код элемента',
    )
    value = models.CharField(
        max_length=300,
        verbose_name='Значение элемента',
    )

    class Meta:
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочников'
        unique_together = (
            ('version', 'code'),
        )

    def __str__(self) -> str:
        return f'{self.code} - {self.value} - {self.version_id}'

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from apps.records.models import Record


@receiver(post_save, sender=Record)
def update_account_sum_on_record_save(sender, instance, **kwargs):
    instance.account.cal_cur_amount()


@receiver(post_delete, sender=Record)
def update_account_sum_on_record_delete(sender, instance, **kwargs):
    instance.account.cal_cur_amount()

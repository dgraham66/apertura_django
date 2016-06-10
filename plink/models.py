from django.db import models
from django.core.urlresolvers import reverse


# Create your models here.
class Plink(models.Model):
    plink_id = models.CharField(
        max_length=64,
        primary_key=True
    )
    description = models.CharField(
        max_length=256,
        blank=True,
        default=''
    )
    prefab_path = models.CharField(
        max_length=256,
        blank=True,
        default=''
    )
    options_str = models.CharField(
        max_length=256,
        blank=True,
        default='{}'
    )
    pretty_name = models.CharField(
        max_length=64,
        blank=True,
        default=''
    )

    def get_absolute_url(self):
        return reverse(
            'detail',
            kwargs={'plink_id': self.plink_id})

    def __unicode__(self):
        return self.plink_id


class PlinkPrefabs(models.Model):
    PREFAB_TUPLES = (('one', 1), ('two', 2))
    PREFAB_IDS = ['one', 'two', 'three']

    config_id = models.CharField(
        max_length=264,
        primary_key=True
    )
    selected_prefab_id = models.CharField(
        max_length=64
    )
    selected_prefab_path = models.CharField(
        max_length=264
    )

    def get_absolute_url(self):
        return reverse('prefabs')

    def __unicode__(self):
        return self.config_id


class PlinkJob(models.Model):
    STATUS_CHOICES = [
        ('0',   'Job Not Ready'),
        ('101', 'Job Pending'),
        ('111', 'Job Ready'),
        ('121', 'Job Scheduled'),
        ('131', 'Job Processing'),
        ('141', 'Job Error'),
        ('888', 'Cancelled'),
        ('999', 'All Completed'),
    ]
    # job_id = models.CharField(
    #     primary_key=True,
    #     auto_created=True,
    #     max_length=128
    # )
    name = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        default=''
    )
    status = models.CharField(
        max_length=64,
        choices=STATUS_CHOICES,
        default='0'
    )
    plink_id = models.CharField(
        max_length=64,
        blank=True,
        default=''
    )
    result_text = models.CharField(
        max_length=2048,
        blank=True,
        default=''
    )

    def get_absolute_url(self):
        return reverse(
            'plinkjob_detail',
            kwargs={'job_id': str(self.pk)}
        )

    def __unicode__(self):
        return str(self.pk)


class PlinkOption(models.Model):
    TYPE_CHOICES = [
        ('OPT_TEXT', 'Text String Option'),
        ('OPT_FILE', 'File Path Option'),
        ('OPT_DIR', 'Directory Path Option'),
        ('OPT_BOOL', 'Boolean Flag Option'),
        ('OPT_INT', 'Integer Value Option'),
        ('OPT_FLOAT', 'Floating Point Value Option'),
    ]
    plink_id = models.ForeignKey(
        Plink,
        on_delete=models.CASCADE
    )
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=255, blank=True, null=True, default='')
    type = models.CharField(
        max_length=64,
        default='OPT_TEXT',
        choices=TYPE_CHOICES
    )

    def __unicode__(self):
        return str(self.key)

    def get_absolute_url(self):
        return reverse(
            'detail',
            kwargs={'plink_id': self.plink_id})

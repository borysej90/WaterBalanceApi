from django.db import models


# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=2)


class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING, db_column="language_id")
    last_remind = models.PositiveIntegerField(null=True, help_text="Last message ID sent to remind drink water")
    start_silence = models.TimeField(null=True, db_column="start_silence_at")
    end_silence = models.TimeField(null=True, db_column="end_silence_at")
    timezone = models.SmallIntegerField(null=True, help_text="Offset from UTC time, e.g: <pre>±hh</pre>")
    has_reminding = models.BooleanField(default=False, help_text="If user has active reminding")

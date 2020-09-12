from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=2)

    def __str__(self):
        return f"<Language: {self.name}>"


class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING)
    last_remind = models.PositiveIntegerField(null=True, blank=True,
                                              help_text="Last message ID sent to remind to drink water")
    start_silence = models.TimeField(null=True, blank=True, db_column="start_silence_at")
    end_silence = models.TimeField(null=True, blank=True, db_column="end_silence_at")
    timezone = models.SmallIntegerField(null=True, blank=True, help_text="Offset from UTC time, e.g: <pre>±hh</pre>")
    has_reminding = models.BooleanField(default=False, help_text="If user has active reminding")

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

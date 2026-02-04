from django.db import models
from django.db.models import Q


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        return self.username


class Event(models.Model):
    name = models.CharField(max_length=150)
    event_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "events"

    def __str__(self) -> str:
        return f"{self.name} ({self.event_date})"


class Plage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="plages")
    name = models.CharField(max_length=120, blank=True, null=True)  # optionnel
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_duration_minutes = models.PositiveSmallIntegerField()
    break_start_time = models.TimeField(blank=True, null=True)
    break_end_time = models.TimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "plages"
        indexes = [
            models.Index(fields=["event", "name"]),
        ]
        constraints = [
            # (EventId, Name) mais en DBML Name est optionnel => on force l'unicité seulement si name n'est pas NULL
            models.UniqueConstraint(
                fields=["event", "name"],
                condition=Q(name__isnull=False),
                name="uq_plage_event_name_not_null",
            ),
        ]

    def __str__(self) -> str:
        return self.name or f"Plage #{self.pk}"


class Slot(models.Model):
    plage = models.ForeignKey(Plage, on_delete=models.CASCADE, related_name="slots")
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    # Réservation (NULL = libre)
    client_fname = models.CharField(max_length=120, blank=True, null=True)
    client_lname = models.CharField(max_length=120, blank=True, null=True)
    client_email = models.EmailField(max_length=255, blank=True, null=True)
    client_phone = models.CharField(max_length=25, blank=True, null=True)

    item = models.CharField(max_length=100, blank=True, null=True)
    item_description = models.TextField(blank=True, null=True)

    liability_accepted = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "slots"
        constraints = [
            models.UniqueConstraint(
                fields=["plage", "start_at"],
                name="uq_slot_plage_startat",
            )
        ]
        indexes = [
            models.Index(fields=["plage", "start_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.plage_id} - {self.start_at}"

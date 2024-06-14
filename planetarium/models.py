from django.db import models
from user.models import User


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "AstronomyShows"

    def __str__(self):
        return f"AstronomyShow {self.title}, {self.description}"


class ShowTheme(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    class Meta:
        verbose_name_plural = "ShowThemes"


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    class Meta:
        verbose_name_plural = "PlanetariumDomes"

    @property
    def category(self):
        if self.rows * self.seats_in_row <= 50:
            return "small"
        if 50 < self.rows * self.seats_in_row <= 100:
            return "medium"
        return "big"

    def __str__(self):
        return f"PlanetariumDome {self.name}, rows: {self.rows}, seats in row: {self.seats_in_row}"


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE, db_index=True)
    planetarium_dome = models.ForeignKey(PlanetariumDome, on_delete=models.CASCADE, db_index=True)
    show_time = models.DateTimeField(db_index=True)

    class Meta:
        verbose_name_plural = "ShowSessions"

    def __str__(self):
        return f"ShowSession, astronomy show: {self.astronomy_show.title}, planetarium dome: {self.planetarium_dome.name}, show time: {self.show_time}"


class Ticket(models.Model):
    row = models.IntegerField(db_index=True)
    seat = models.IntegerField(db_index=True)
    show_session = models.ForeignKey(ShowSession, on_delete=models.CASCADE, db_index=True)
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE, null=True, related_name="ticket",
                                    db_index=True)

    class Meta:
        verbose_name_plural = "Tickets"
        constraints = [
            models.UniqueConstraint(fields=["seat", "row"], name="unique_ticket_seat_and_row")
        ]

    def __str__(self):
        return f"Ticket. Seat: {self.seat}, show session: {self.show_session}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)

    class Meta:
        verbose_name_plural = "Reservations"

    def __str__(self):
        return f"Reservation. Created at: {self.created_at}, user: {self.user.first_name} {self.user.last_name}"

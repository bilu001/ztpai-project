from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Player(models.Model):
    """
    Matches the 'players' table in your ERD.

    You can add more fields if you want, such as referencing 'statistics_id' 
    or 'injury_id', but typically you'd store them as foreign keys or in separate tables 
    referencing 'player_id'. We'll keep it simple here.
    """
    player_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    position = models.CharField(max_length=100, blank=True, null=True)
    contract_ends = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'players' 

    def __str__(self):
        return f"{self.name} {self.surname}"

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255) 
    role = models.CharField(max_length=50, null=True, blank=True) 
    changed_password = models.BooleanField(default=False)
    player_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "users"

    def save(self, *args, **kwargs):
        """
        Automatically hash the password before saving if it's not already hashed.
        """
        if not self.password.startswith("pbkdf2_") and not self.password.startswith("argon2"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """
        Check if a raw password matches the stored hashed password.
        """
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Injury(models.Model):
    injury_id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="injuries")
    type = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    feelings = models.TextField(blank=True, null=True)
    next_visit = models.DateField(blank=True, null=True)
    class Meta:
            db_table = "injuries"

    def __str__(self):
        return f"{self.type} - {self.player}"
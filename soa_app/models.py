from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class RucInfo(models.Model):
    ruc = models.CharField(max_length=11, unique=True)
    razon_social = models.CharField(max_length=255)
    estado = models.CharField(max_length=50)
    condicion = models.CharField(max_length=50)
    direccion = models.CharField(max_length=255)
    departamento = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50)
    distrito = models.CharField(max_length=50)
    ubigeo = models.CharField(max_length=6)


class DniInfo(models.Model):
    dni = models.CharField(max_length=8, unique=True)
    nombres = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    cod_verifica = models.IntegerField()
    correo = models.EmailField(max_length=255, unique=True)
    contrasena = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Hashear la contraseña antes de guardarla
        self.contrasena = make_password(self.contrasena)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dni} - {self.nombres} {self.apellido_paterno} {self.apellido_materno}"
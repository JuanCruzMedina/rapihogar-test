from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=765, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    whatsapp_phone = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        db_index=True,
        verbose_name="Telefono WhatsApp (+54)",
    )
    last_name = models.CharField(
        max_length=100,
        null=True,
    )
    first_name = models.CharField(
        max_length=100,
        null=True,
    )

    @property
    def full_name(self):
        return "{} {}".format(
            self.first_name if self.first_name else "",
            self.last_name if self.last_name else "",
        )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    objects = UserManager()

    class Meta:
        app_label = "rapihogar"
        verbose_name = _("RapiHogar User")
        verbose_name_plural = _("RapiHogar Users")


class Scheme(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "rapihogar"
        verbose_name = _("Esquema de un pedido")
        verbose_name_plural = _("Esquemas de pedidos")


class Company(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=80)
    website = models.CharField(max_length=100)

    class Meta:
        app_label = "rapihogar"
        verbose_name = _("Empresa")
        verbose_name_plural = _("Empresas")


class Order(models.Model):
    REQUEST = 0
    ORDER = 1

    TIPO_PEDIDO = (
        (REQUEST, "Solicitud"),
        (ORDER, "Pedido"),
    )
    type_request = models.IntegerField(
        choices=TIPO_PEDIDO, db_index=True, default=ORDER
    )
    client = models.ForeignKey(User, verbose_name="cliente", on_delete=models.CASCADE)
    technician = models.ForeignKey(
        "Technician", verbose_name="tecnico", on_delete=models.CASCADE, null=False
    )
    scheme = models.ForeignKey(Scheme, null=True, on_delete=models.CASCADE)
    hours_worked = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = "rapihogar"
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ("-id",)


class Technician(models.Model):
    last_name = models.CharField(
        max_length=100,
        null=True,
    )
    first_name = models.CharField(
        max_length=100,
        null=True,
    )

    @property
    def full_name(self):
        return "{} {}".format(
            self.first_name if self.first_name else "",
            self.last_name if self.last_name else "",
        )

    def __str__(self):
        return self.full_name

    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        app_label = "rapihogar"
        verbose_name = _("Tecnicos")
        verbose_name_plural = _("Tecnicos")

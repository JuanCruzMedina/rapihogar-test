"""Register model"""

from django.contrib import admin

from .models import Company, Order, Scheme, Technician, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_active", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_active", "is_staff")
    ordering = ("email",)


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "website")
    search_fields = ("name", "email")
    ordering = ("name",)


@admin.register(Order)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type_request",
        "client",
        "technician",
        "scheme",
        "hours_worked",
    )
    list_filter = ("type_request", "technician")
    search_fields = ("client__email", "scheme__name", "technician__first_name")
    ordering = ("-id",)


@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "full_name")
    search_fields = ("first_name", "last_name")
    ordering = ("last_name",)
    readonly_fields = ("full_name",)

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline
from .models import User, Profile, ProfileOnboard, Address

@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('email', 'full_name', 'role', 'is_active', 'is_staff', 'date_joined', 'dob', 'password')
    search_fields = ('email', 'full_name')
    list_filter = ('role', 'is_active', 'is_staff')
    ordering = ('-date_joined',)

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('user', 'gender', 'mobile', 'language', 'dob')
    search_fields = ('user__email', 'mobile')
    list_filter = ('gender',)

@admin.register(ProfileOnboard)
class ProfileOnboardAdmin(ModelAdmin):
    list_display = ('user', 'from_where', 'gender', 'health_condition')
    search_fields = ('user__email', 'from_where', 'health_condition')

@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'city', 'country', 'updated_at')
    search_fields = ('user__email', 'first_name', 'last_name', 'city')
    list_filter = ('country',)
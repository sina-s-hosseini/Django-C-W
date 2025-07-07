from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile


# Customize User Display in Admin Panel
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'username', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'username')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    ordering = ('-date_joined',)

# Register CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)


# Customize UserProfile Display
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture', 'bio')  # Adjust fields based on your model
    search_fields = ('user__email', 'user__username')

admin.site.register(UserProfile, UserProfileAdmin)





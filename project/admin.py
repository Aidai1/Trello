from django.contrib import admin
from .models import Board, Card, Color, Column, Comment, Label, Checklist, ChecklistItem, User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin



class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'full_name', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'username', 'full_name')
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Board) 
admin.site.register(Color) 
admin.site.register(Card) 
admin.site.register(Column) 
admin.site.register(Label) 
admin.site.register(Comment) 
admin.site.register(Checklist)
admin.site.register(ChecklistItem)
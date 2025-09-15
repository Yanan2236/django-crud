from django.contrib import admin

from .models import SkillBook, SkillVariant, SkillEffect, SkillEffectTerm

class SkillEffectTermInline(admin.TabularInline):
    model = SkillEffectTerm
    extra = 0

class SkillEffectInline(admin.TabularInline):
    model = SkillEffect
    extra = 0
    show_change_link = True

class SkillVariantInline(admin.StackedInline):
    model = SkillVariant
    extra = 0
    show_change_link = True

@admin.register(SkillBook)
class SkillBookAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [SkillVariantInline]

@admin.register(SkillVariant)
class SkillVariantAdmin(admin.ModelAdmin):
    list_display = ("book", "rank")
    inlines = [SkillEffectInline]

@admin.register(SkillEffect)
class SkillVariantAdmin(admin.ModelAdmin):
    list_display = ("variant", "order", "kind", "target_side", "target_stat", "value_base")
    inlines = [SkillEffectTermInline]

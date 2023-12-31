from typing import Any, Optional

from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin, widgets
from django.http import HttpRequest
from django.utils.html import format_html

from ..models import Course, Link, Phone, Place, Text, TGUser


@admin.register(Text)
class TextAdmin(ModelAdmin[Text]):
    list_display = (
        "name",
        "is_button",
        "text",
    )

    readonly_fields = (
        "name",
        "is_button",
    )

    fields = (
        "name",
        "is_button",
        "text",
    )

    def has_add_permission(self, request: HttpRequest) -> bool:
        super().has_add_permission(request)
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Optional[Text] = None
    ) -> bool:
        super().has_delete_permission(request, obj)
        return False


@admin.register(TGUser)
class TGUserAdmin(ModelAdmin[TGUser]):
    list_display = (
        "id",
        "full_name",
        "username",
    )

    def has_add_permission(self, request: HttpRequest) -> bool:
        super().has_add_permission(request)
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: Optional[TGUser] = None
    ) -> bool:
        super().has_change_permission(request, obj)
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Optional[TGUser] = None
    ) -> bool:
        super().has_delete_permission(request, obj)
        return False


@admin.register(Course)
class CourseAdmin(ModelAdmin[Course]):
    class CourseForm(forms.ModelForm[Course]):
        class Meta:
            model = Course
            fields = "__all__"

        prerequisite_courses = forms.ModelMultipleChoiceField(
            queryset=Course.objects.all(),
            required=False,
            widget=widgets.FilteredSelectMultiple(
                verbose_name="Prerequisite Courses",
                is_stacked=False,
            ),
        )

    form = CourseForm

    list_display = (
        "fa_title",
        "course_type",
        "unit_type",
    )

    def save_related(
        self,
        request: HttpRequest,
        form: Any,
        formsets: Any,
        change: Any,
    ) -> None:
        super().save_related(request, form, formsets, change)

        form.instance.prerequisite_courses.clear()
        form.instance.prerequisite_courses.set(form.cleaned_data["prerequisite_courses"])


@admin.register(Place)
class PlaceAdmin(ModelAdmin[Place]):
    list_display = (
        "name",
        "group",
        "latitude",
        "longitude",
    )


@admin.register(Phone)
class PhoneAdmin(ModelAdmin[Phone]):
    list_display = (
        "name",
        "phone_number",
    )


@admin.register(Link)
class LinkAdmin(ModelAdmin[Link]):
    list_display = (
        "name",
        "url_address",
    )

    @admin.display()
    def url_address(self, obj: Link) -> str:
        return format_html(f'<a href="{obj.address}">{obj.address}</a>')

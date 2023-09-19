from django.shortcuts import render, redirect
from django.views import View
from django.db import models
from django.forms import ModelForm
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from django.urls import path


class CRUDView(View):
    model: models.Model
    form: ModelForm
    template_create: str
    template_delete: str
    template_list: str
    template_current: str

    @classmethod
    def create(
        cls,
        request: HttpRequest,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:
        if request.method == 'GET':
            return render(
                request=request,
                template_name=cls.template_create,
                context={
                    'form': cls.form
                }
            )
        if request.FILES:
            form: ModelForm = cls.form(request.POST, request.FILES)
        else:
            form: ModelForm = cls.form(request.POST)
        message: str = None
        if form.is_valid():
            form.save()
            message: str = "ok"
            return render(
                request=request,
                template_name=cls.template_create,
                context={
                    'form': cls.form,
                    'message': message
                }
            )
        return render(
            request=request,
            template_name=cls.template_create,
            context={
                'form': cls.form
            }
        )

    @classmethod
    def read(
        cls,
        request: HttpRequest,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:
        queryset: list[cls.model] = \
            cls.model.objects.all()
        return render(
            request=request,
            template_name=cls.template_list,
            context={
                'models': queryset
            }
        )

    @classmethod
    def as_my_view(cls, endpoint: str):
        return [
            path(endpoint, cls.read),
            path(f'{endpoint}/create/', cls.create)
        ]

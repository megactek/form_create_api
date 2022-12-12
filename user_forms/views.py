from rest_framework import viewsets, response, status
from .serializers import (
    FormFieldSerializer,
    FormSerializer,
    UserResponseSerializer,
    Form,
    FormInput,
    UserFormResponses,
)
from timi.custom_methods import IsAuthenticatedCustom
from rest_framework.decorators import action
from django.core.exceptions import (
    TooManyFieldsSent,
    ObjectDoesNotExist,
    PermissionDenied,
)


class FormView(viewsets.ModelViewSet):
    serializer_class = FormSerializer
    permission_classes = (IsAuthenticatedCustom,)
    queryset = Form.objects.select_related("user")

    def list(self, request, *args, **kwargs):
        data = Form.objects.filter(user=request.user.id)
        serialize = self.serializer_class(data, many=True)
        return response.Response({"forms": serialize.data})

    def create(self, request, *args, **kwargs):
        user = request.user
        request.data.update({"user": user.id})
        return super().create(request, *args, **kwargs)

    @action(methods=["post"], detail=True)
    def add_input(self, request, pk):
        if isinstance(request.data, list):
            raise TooManyFieldsSent({"input": "fields should be added one at a time"})
        form = self.serializer_class(self.get_object()).data
        request.data.update({"form": form.get("id")})
        data = FormFieldSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        return response.Response({"success": "input added"})

    @action(methods=["post"], detail=True)
    def submit_response(self, request, pk):
        form = self.get_object()
        check_response = UserFormResponses.objects.filter(
            form=form.id, created_by=request.user
        )
        if len(check_response) > 0:
            return response.Response(
                {"error": "form response already submitted"},
                status=status.HTTP_403_FORBIDDEN,
            )
        request.data.update({"created_by": request.user.id})
        request.data.update({"form": form.id})
        _response = UserResponseSerializer(data=request.data)
        _response.is_valid(raise_exception=True)
        _response.save()
        return response.Response(_response.data)


class FormInputView(viewsets.ModelViewSet):
    serializer_class = FormFieldSerializer
    queryset = FormInput.objects.select_related("form")
    permission_classes = (IsAuthenticatedCustom,)

    def update(self, request, *args, **kwargs):
        form_obj = request.query_params.dict()
        if not form_obj.get("form", None):
            raise ObjectDoesNotExist({"form": "form id"})
        check = Form.objects.get(id=form_obj.get("form"))
        if not check.user == request.user:
            raise PermissionDenied({"form": "this form does not belong to you"})
        request.data.update({"form": form_obj.get("form")})
        data_ = self.serializer_class(data=request.data)
        data_.is_valid(raise_exception=True)
        return super().update(request, *args, **kwargs)

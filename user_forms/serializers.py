from rest_framework import serializers
from .models import Form, FormInput, UserFormResponses


class OptionsSerializer(serializers.Serializer):
    option_value = serializers.CharField()


class FormFieldSerializer(serializers.ModelSerializer):
    options = OptionsSerializer(many=True, required=False)

    class Meta:
        model = FormInput
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFormResponses
        fields = "__all__"


class FormSerializer(serializers.ModelSerializer):
    field = serializers.SerializerMethodField(read_only=True, required=False)
    responses = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = Form
        fields = "__all__"

    def get_field(self, form):
        field = FormInput.objects.filter(form=form)
        serialize = FormFieldSerializer(field, many=True)
        return serialize.data

    def get_responses(self, form):
        field = UserFormResponses.objects.filter(form=form)
        serialize = UserResponseSerializer(field, many=True)
        return serialize.data

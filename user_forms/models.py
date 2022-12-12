from django.db import models
from timi_app.models import CustomUser
from django.db.models import JSONField
from django.core.exceptions import ValidationError


FORM_OBJECT_OPTIONS = (
    ("input", "input"),
    ("textarea", "textarea"),
    ("select", "select"),
    ("radio", "radio"),
    ("file", "file"),
)


class Form(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} form"


class FormInput(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="inputs")
    label = models.CharField(max_length=255)
    input_type = models.CharField(max_length=255, choices=FORM_OBJECT_OPTIONS)
    options = models.JSONField(null=True)

    def __str__(self) -> str:
        return f"{self.form.name} - {self.label} input field"


class UserFormResponses(models.Model):
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    response = models.JSONField()

    def __str__(self) -> str:
        return f"{self.created_by.first_name} response to {self.form.name}"

    def clean(self, *args, **kwargs):
        if not isinstance(self.response, list):
            raise ValidationError({"response": "Should be an array"})
        for resp in self.response:
            for _input, input_value in resp.items():
                try:
                    form_input = FormInput.objects.get(id=_input)
                except FormInput.DoesNotExist:
                    raise ValidationError({"response": "Form input not found"})
                if form_input.input_type == "select":
                    options = [op.get("name", None) for op in form_input.option]
                    if not input_value in options:
                        raise ValidationError(
                            {"response": "Selected Value is not in allowed options"}
                        )

        return super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

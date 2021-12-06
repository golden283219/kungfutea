from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext as _

from .models import LcOrderEmail, User


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(
        max_length=128, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = (
            "email",
            "full_name",
            "revel_est_id",
            "company_name",
            "new_password",
        )

    def validate_email(self, val):
        if not LcOrderEmail.objects.filter(email=val).exists():
            raise ValidationError(_("Given email is not registered."))
        return val

    def create(self, validated_data):
        password = validated_data.pop("new_password")
        user = super().create(validated_data)
        user.set_password(password)

        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "full_name",
            "revel_est_id",
            "company_name",
            "RC_username",
            "RC_password",
        )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        max_length=128, style={"input_type": "password"}, write_only=True
    )
    password1 = serializers.CharField(
        max_length=128, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=128, style={"input_type": "password"}, write_only=True
    )

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise ValidationError(_("Passwords didn't match."))
        return attrs

    def validate_old_password(self, val):
        if not self.instance.check_password(val):
            raise ValidationError(_("Old password is incorrect."))
        return val

    def update(self, user, validated_data):
        password = validated_data.pop("password1")

        user.set_password(password)
        user.save()
        return user


class TokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, val):
        user_exists = User.objects.filter(email=val).exists()
        if not user_exists:
            if not LcOrderEmail.objects.filter(email=val).exists():
                raise ValidationError(
                    _(
                        "Email not associated with Kung Fu Tea Franchise. Please contact IT support"
                    )
                )
            else:
                raise ValidationError(_("User with given email does not exist"))
        return val

    def validate(self, attrs):
        authenticate_kwargs = {
            "email": attrs["email"],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass
        self.user = authenticate(**authenticate_kwargs)

        if self.user is None or not self.user.is_active:
            raise ValidationError({"password": _("Wrong password")})

        data = super().validate(attrs)
        return data

    def create(self, validated_data):
        return self.user


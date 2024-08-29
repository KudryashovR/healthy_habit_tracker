from rest_framework import serializers

from users.models import CustomUser


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для профиля пользователя.
    """

    class Meta:
        model = CustomUser
        fields = ["email", "password", "tg_id", "phone", "city", "avatar"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            phone=validated_data["phone"],
            city=validated_data["city"],
            tg_id=validated_data["tg_id"],
        )

        return user

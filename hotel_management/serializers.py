from unicodedata import decimal

from rest_framework import serializers
from .models import User, Reservation, Menu


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'password']

    username = serializers.CharField(required=False)  # Make required=False
    phone_number = serializers.CharField(required=False)  # Make required=False
    password = serializers.CharField(required=False)  # Make required=False
    def validate(self, data):
        errors = []
        extra_fields = set(self.initial_data.keys()) - set(self.fields)
        if extra_fields:
            raise serializers.ValidationError(
                {"error": f"Additional fields not allowed: {', '.join(extra_fields)}"}
            )
        # Custom validation for 'username'
        username = data.get('username', None)
        if not username:
            errors.append("username is required")
        elif User.objects.filter(username=username).exists():
            errors.append("username already exists")

        # Custom validation for 'phone_number'
        phone_number = data.get('phone_number', None)
        if not phone_number:
            errors.append("phone_number is required")
        elif User.objects.filter(phone_number=phone_number).exists():
            errors.append("phone_number already exists")

        # Custom validation for 'password'
        password = data.get('password', None)
        if not password:
            errors.append("password is required")

        # If there are any errors, raise a validation error
        if errors:
            raise serializers.ValidationError({"error": errors})

        # Hash the password before saving it
        data['password'] = self.hash_password(data.get('password'))

        return data

    def hash_password(self, password):
        """
        Hashes the password before saving.
        """
        user = User()  # Create a temporary User instance to hash the password
        user.set_password(password)  # Hash the password
        return user.password  # Return the hashed password

class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Display username instead of ID

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'room_number', 'check_in_date', 'check_out_date', 'created_at']
        read_only_fields = ['created_at']

    check_out_date = serializers.CharField(required=False)  # Make required=False
    check_in_date = serializers.CharField(required=False)  # Make required=False
    room_number = serializers.IntegerField(required=False)

    def validate(self, data):
        """
        Validate that the reservation does not overlap with existing reservations for the same room
        and prevent duplicate reservations with the same data.
        """
        errors = []

        check_in_date = data.get('check_in_date')
        check_out_date = data.get('check_out_date')
        room_number = data.get('room_number')
        extra_fields = set(self.initial_data.keys()) - set(self.fields)
        if extra_fields:
            raise serializers.ValidationError(
                {"error": f"Additional fields not allowed: {', '.join(extra_fields)}"}
            )
        if not check_in_date:
            errors.append("check_in_date is required.")

        if not check_out_date:
            errors.append("check_out_date is required.")

        if not room_number:
            errors.append("room_number is required.")

        if check_in_date and check_out_date and check_out_date <= check_in_date:
            errors.append("check_out_date must be after the check_in_date.")

        if check_in_date and check_out_date and room_number:
            # Check for duplicate reservation
            duplicate_reservations = Reservation.objects.filter(
                room_number=room_number,
                check_in_date=check_in_date,
                check_out_date=check_out_date
            )

            # Exclude the current reservation when updating
            if self.instance:
                duplicate_reservations = duplicate_reservations.exclude(id=self.instance.id)

            if duplicate_reservations.exists():
                errors.append("An identical reservation already exists for the selected room and dates.")

            # Check for overlapping reservations
            overlapping_reservations = Reservation.objects.filter(
                room_number=room_number,
                check_in_date__lt=check_out_date,
                check_out_date__gt=check_in_date
            )

            if self.instance:
                overlapping_reservations = overlapping_reservations.exclude(id=self.instance.id)

            if overlapping_reservations.exists():
                errors.append("This reservation overlaps with an existing reservation for the selected room.")

        if errors:
            raise serializers.ValidationError({"errors": errors})

        return data

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'description', 'price', 'created_at']
        read_only_fields = ['created_at']

    name = serializers.CharField(required=False)  # Make required=False
    description = serializers.CharField(required=False)  # Make required=False
    price = serializers.FloatField(required=False)


    def validate(self, data):
        name = data.get('name', None)
        description = data.get('description', None)
        price = data.get('price', None)

        extra_fields = set(self.initial_data.keys()) - set(self.fields)
        if extra_fields:
            raise serializers.ValidationError(
                {"error": f"Additional fields not allowed: {', '.join(extra_fields)}"}
            )

        errors = []
        if not name:
            errors.append("name is required.")
        elif type(name) is not str:
            errors.append("name should be string.")

        if not description:
            errors.append("description is required.")
        elif type(description) is not str:
            errors.append("description should be string.")

        if not price:
            errors.append("price is required.")
        elif type(price) not in [float, int]:
            errors.append("price should be float or int.")

        if errors:
            raise serializers.ValidationError({"error": errors})

        return data



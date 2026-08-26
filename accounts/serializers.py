from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True,min_length=8)
    confirm_password = serializers.CharField(write_only=True,min_length=8)

    class Meta:
        model = User
        fields = ('phone','password','confirm_password','participant','organizer')

    def validate_phone(self,value):
        
        if not value:
            raise serializers.ValidationError('Phone number is required')

        if not value.isdigit():
            raise serializers.ValidationError('Phone number must contain only digits')
        
        if len(value) != 11:
            raise serializers.ValidationError('Phone number must be exactly 11 digits')
        
        return value
    
    def validate(self,attrs):
        
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password':'"The passwords do not match."'})
        
        participant = attrs.get("participant")
        organizer = attrs.get("organizer")

        if participant is None or organizer is None:
            raise serializers.ValidationError('Role selection is required')
        
        if participant == organizer:
            raise serializers.ValidationError('One of the roles must be True and the other False')
        
        return attrs
    
    def create(self,validated_data):
        
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password,**validated_data)

        return user
    
class LoginSerializer(serializers.ModelSerializer):

    phone = serializers.CharField(max_length=11,write_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('phone','password')

    def validate(self, attrs):
        
        phone = attrs.get('phone')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'),phone=phone,password=password)

        if not user:
            raise serializers.ValidationError('The phone number or password is incorrect.')

        if not user.is_active:
            raise   serializers.ValidationError('This account is inactive.')
        
        attrs['user'] = user
        return attrs
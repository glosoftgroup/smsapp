from rest_framework import serializers
from .models import SmsMessage


class SmsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SmsMessage
        fields = ('to', 'request_id', 'message', 'priority')


class MessageInstructionSerializer(serializers.Serializer):

    request_id = serializers.CharField(max_length=50)
    network = serializers.CharField(max_length=50)
    msisdn = serializers.CharField(max_length=50)
    message = serializers.CharField(max_length=200)
    sender_id = serializers.CharField(max_length=50)
    priority = serializers.CharField(max_length=50)


class MessageSerializer(serializers.Serializer):

    message_id = serializers.CharField(max_length=50)
    msisdn = serializers.CharField()
    message = serializers.CharField(max_length=200)
    sender_id = serializers.CharField(max_length=50, required=False)
    priority = serializers.ChoiceField(
        ['notification', 'bulk', 'mini-statement'])
    partner = serializers.ChoiceField(['tigo-tz'])

    def validate(self, data):

        if len(data['msisdn']) > 12:
            raise serializers.ValidationError("Invalid msisdn. Msisdn characters too long")
        else:
            return data

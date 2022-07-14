from rest_framework import serializers


def get_error_body(message):
    return {'detail': message}


def validate_promotion_data(body):
    users_limit = 'users_limit'
    start_date = 'start_date'
    end_date = 'end_date'

    if(users_limit not in body):
        if(start_date in body and end_date in body):
            if(body[start_date] >= body[end_date]):
                raise serializers.ValidationError(
                    'Start date must be before end date')
            return True  # valid by date
        else:
            raise serializers.ValidationError('Missing start date or end date')
    else:
        if(start_date in body or end_date in body):
            raise serializers.ValidationError(
                'Either use start date and end date or users limit')
        else:
            return True  # Using limit only so valid

from wafrcloudaccount.models import AwsAccount
from rest_framework.exceptions import ValidationError


def initiate(request):
    query_params = request.query_params
    account_id = query_params.get('account_id')
    account = AwsAccount.objects.filter(name=account_id).first()
    if not account_id:
        raise ValidationError(
            {'account_id': 'This field is required.'})
    account = AwsAccount.objects.filter(name=account_id).first()
    if not account:
        raise ValidationError(
            {'account_id': 'Invalid account ID.'})
    return account

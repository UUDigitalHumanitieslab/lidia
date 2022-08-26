from rest_framework.decorators import (
    api_view, authentication_classes, renderer_classes, parser_classes
)
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.authentication import BasicAuthentication
from rest_framework import status

from django.conf import settings

from hypothesis import Hypothesis


@api_view(['POST'])
@authentication_classes([BasicAuthentication])  # TODO change later
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@parser_classes([JSONParser])
def post_annotation_view(request):
    data = request.data
    try:
        uri = data['uri']
        text = data['text']
        target = data['target']
    except KeyError as err:
        return Response(
            {'error': '{} is missing'.format(err)},
            status=status.HTTP_400_BAD_REQUEST
        )

    h = Hypothesis(
        username=request.user.hypothesisauthentication.hypothesis_username,
        token=request.user.hypothesisauthentication.api_token
    )
    group_id = settings.HYPOTHESIS_GROUP_ID
    payload = {
        'uri': uri,
        'target': target,
        'tags': [],  # What to do with tags?
        'text': text,
        'document': {},  # Add data to this?
        'group': group_id
    }  # TODO: do we have to specify permissions?
    h_response = h.post_annotation(payload)
    if h_response.status_code != 200:
        return Response(
            {'error': 'API request on Hypothesis server did not succeed'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # TODO give a meaningful response
    response = {}

    return Response(response)

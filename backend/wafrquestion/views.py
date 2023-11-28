from typing import Any
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from awskservices.questions import WellArchitectedQuestions
from rest_framework import permissions


from awskservices.initiate_view import initiate


class Questions(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def get(self, request, format=None):
        self.account = initiate(request=request)
        self.wellArchitectedQuestions = WellArchitectedQuestions(self.account)
        query_params = request.query_params
        workloadId = query_params.get('workloadId')
        lensAlias = query_params.get('lensAlias')
        pillarId = query_params.get("pillarId")
        return Response(self.wellArchitectedQuestions.get_all_questions(workloadId, lensAlias, pillarId), status=status.HTTP_200_OK)


class Answer(APIView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def post(self, request, format=None):
        self.account = initiate(request=request)
        self.wellArchitectedQuestions = WellArchitectedQuestions(self.account)
        query_params = request.query_params
        workloadId = query_params.get('workloadId')
        lensAlias = query_params.get('lensAlias')
        questionId = request.data['questionId']
        selectedChoices = request.data['selectedChoices'] if "selectedChoices" in request.data else None

        isApplicable = request.data['isApplicable'] if "isApplicable" in request.data else True
        reason = request.data['reason'] if "reason" in request.data else None
        notes = request.data['notes'] if "notes" in request.data else None
        choiceUpdates = request.data['choiceUpdates'] if 'choiceUpdates' in request.data else None

        return Response(self.wellArchitectedQuestions.answer_question(workloadId, lensAlias, questionId, selectedChoices, choiceUpdates, notes, isApplicable, reason), status=status.HTTP_200_OK)

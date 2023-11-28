from awskservices.boto3_client import boto3_helpers


class WellArchitectedQuestions(boto3_helpers):
    def __init__(self, account=None) -> None:
        super().__init__(account=account)
        self.questions = []

    def get_all_questions(self, workloadId, lensAlias, pillarId):
        nextToken = ""

        while True:
            response = self.client.list_answers(
                WorkloadId=workloadId,
                LensAlias=lensAlias,
                NextToken=nextToken,
                MaxResults=50
            )
            self.questions = self.questions + response['AnswerSummaries']
            if 'NextToken' in response:
                nextToken = response['NextToken']
                if not nextToken or nextToken == "":
                    break
            else:
                break
        return_questions = []
        for question in self.questions:
            if question['PillarId'] == pillarId:
                return_questions.append(question)
        return return_questions

    def answer_question(self, workloadId, lensAlias, questionId, selectedChoices, choiceUpdates=None, notes=None, isApplicable=True, reason=None):
        args = {
            "WorkloadId": workloadId,
            "LensAlias": lensAlias,
            "QuestionId": questionId,
            "IsApplicable": isApplicable,

        }
        if selectedChoices is not None:
            args['SelectedChoices'] = selectedChoices
        if notes is not None:
            args['Notes'] = notes
        if reason is not None:
            args['Reason'] = reason
        if choiceUpdates is not None:
            args["ChoiceUpdates"] = choiceUpdates
        try:
            response = self.client.update_answer(**args)
        except Exception as exp:
            response = exp
        return response

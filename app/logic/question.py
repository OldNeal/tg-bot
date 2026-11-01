from app.logic.base import BaseLogic
from app.logic.utils import class_decor


@class_decor
class QuestionLogic(BaseLogic):
    async def create(
        self,
        body: str,
        description: str | None,
        correct_answers: list[str],
        incorrect_answers: list[str],
    ):
        query_body = await self.body
        data = self.schemas.QueryQuestionCreate.model_validate(
            query_body.model_dump()
            | {
                'question': self.schemas.QuestionCreate(
                    body=body,
                    description=description,
                    correct_answers=correct_answers,
                    incorrect_answers=incorrect_answers,
                )
            }
        )
        return await self.client.question_create(data)

    async def mine(self, page: int = 0):
        return await self.client.question_my(
            await self.body,
            page=page,
            per_page=10,
        )

    async def statistics(self, question_id: int):
        return await self.client.question_statistics(
            await self.body,
            question_id,
        )

    async def user_statistics(self):
        return await self.client.question_user_statistics(await self.body)

    async def random_question(self):
        return await self.client.question_random(await self.body)

    async def answer(self, question_id: int, answer_id: int):
        return await self.client.question_answer(
            await self.body,
            question_id,
            answer_id,
        )

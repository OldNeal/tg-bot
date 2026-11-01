import random

from app.service.base import BaseService, AnswerBody
from app.logic.question import QuestionLogic
from app.tg.text.question import QuestionText
from app.tg.buttons.question import QuestionIKB
from app.tg.fsm.state import QuestionState
from app.tg.fsm.utils import QuestionFSM


class QuestionService(BaseService):
    logic_class: type[QuestionLogic] = QuestionLogic
    logic: QuestionLogic
    text_class: type[QuestionText] = QuestionText
    text: type[QuestionText]
    ikb_class: type[QuestionIKB] = QuestionIKB
    IKB: QuestionIKB
    fsm_class: type[QuestionFSM] = QuestionFSM
    fsm: QuestionFSM

    async def clear_quiz(self):
        for key in (
            'quiz_question_id',
            'quiz_correct_answer_id',
            'quiz_correct_answer_body',
            'quiz_answer_ids',
            'quiz_answers',
        ):
            await self.fsm.remove_value(key)

    async def menu(self):
        await self.clear_quiz()
        await self.fsm.set_state()
        return await self.answer([
            AnswerBody(
                text=self.text.menu(),
                reply_markup=self.IKB.menu(),
            )
        ])

    async def random_question(self):
        await self.clear_quiz()
        await self.fsm.set_state()
        data = await self.logic.random_question()
        question = data.question
        correct_answers = [
            answer for answer in question.answers
            if answer.is_correct is True
        ]
        incorrect_answers = [
            answer for answer in question.answers
            if answer.is_correct is False
        ]
        if not correct_answers or len(incorrect_answers) < 3:
            return await self.answer([
                AnswerBody(
                    text=self.text.quiz_unavailable(),
                    reply_markup=self.IKB.back_to_menu(),
                )
            ])

        correct_answer = random.choice(correct_answers)
        answers = [correct_answer, *random.sample(incorrect_answers, 3)]
        random.shuffle(answers)
        await self.fsm.update_data(
            quiz_question_id=question.question_id,
            quiz_correct_answer_id=correct_answer.answer_id,
            quiz_correct_answer_body=correct_answer.body,
            quiz_answer_ids=[answer.answer_id for answer in answers],
            quiz_answers=[
                {'answer_id': answer.answer_id, 'body': answer.body}
                for answer in answers
            ],
        )
        return await self.answer([
            AnswerBody(
                text=self.text.quiz(question),
                data=question,
                reply_markup=self.IKB.quiz(question.question_id, answers),
            )
        ])

    async def submit_quiz_answer(self, question_id: int, answer_id: int):
        active_question_id = await self.fsm.get_value('quiz_question_id')
        answer_ids = await self.fsm.get_value('quiz_answer_ids', [])
        if active_question_id != question_id or answer_id not in answer_ids:
            return await self.answer([
                AnswerBody(
                    text=self.text.quiz_expired(),
                    reply_markup=self.IKB.back_to_menu(),
                )
            ])

        correct_answer_id = await self.fsm.get_value('quiz_correct_answer_id')
        correct_answer_body = await self.fsm.get_value('quiz_correct_answer_body')
        answers = await self.fsm.get_value('quiz_answers', [])
        selected_answer = next(
            answer['body'] for answer in answers
            if answer['answer_id'] == answer_id
        )
        await self.clear_quiz()
        question = (await self.logic.answer(question_id, answer_id)).question
        is_correct = answer_id == correct_answer_id
        return await self.answer([
            AnswerBody(
                text=self.text.quiz_result(
                    question,
                    selected_answer,
                    correct_answer_body,
                    is_correct,
                ),
                reply_markup=self.IKB.quiz_result(),
            )
        ])

    async def invalid_subcommand(self, subcommand: str):
        return await self.answer([
            AnswerBody(
                text=self.text.unknown_subcommand(subcommand),
                reply_markup=self.IKB.menu(),
            )
        ])

    async def questions(self, page: int = 0):
        await self.clear_quiz()
        data = await self.logic.mine(page)
        questions = data.questions
        if not questions:
            return await self.answer([
                AnswerBody(
                    text=self.text.empty(),
                    data=data,
                    reply_markup=self.IKB.back_to_menu(),
                )
            ])

        page_info = data.page
        current_page = page_info.number if page_info else page
        max_page = page_info.max if page_info else 1
        return await self.answer([
            AnswerBody(
                text=self.text.question_list(data.count, current_page, max_page),
                data=data,
                reply_markup=self.IKB.question_list(
                    questions,
                    current_page,
                    max_page,
                ),
            )
        ])

    async def open_question(self, page: int, index: int):
        await self.clear_quiz()
        data = await self.logic.mine(page)
        if index < 0 or index >= len(data.questions):
            return await self.questions(page)
        question = data.questions[index]
        statistics = await self.logic.statistics(question.question_id)
        return await self.answer([
            AnswerBody(
                text=self.text.question_card(question, statistics),
                data=statistics,
                reply_markup=self.IKB.question(page),
            )
        ])

    async def user_statistics(self):
        await self.clear_quiz()
        data = await self.logic.user_statistics()
        return await self.answer([
            AnswerBody(
                text=self.text.user_statistics(data.statistics),
                reply_markup=self.IKB.back_to_menu(),
            )
        ])

    async def start_create(self):
        await self.clear_quiz()
        await self.fsm.update_data(
            create_question={},
            create_step='body',
            create_editing=False,
        )
        await self.fsm.set_state(QuestionState.create)
        return await self.answer([
            AnswerBody(
                text=self.text.create_prompt('body'),
                reply_markup=self.IKB.create_edit_prompt(),
            )
        ])

    async def create_input(self, value: str):
        question_data = await self.fsm.get_value('create_question', {})
        step = await self.fsm.get_value('create_step', 'body')

        if step == 'confirm':
            return await self.review_create()
        elif step == 'body':
            if not value.strip():
                return await self.answer([
                    AnswerBody(
                        text=self.text.invalid_question(),
                        reply_markup=self.IKB.create_edit_prompt(
                            await self.fsm.get_value('create_editing', False),
                        ),
                    )
                ])
            question_data['body'] = value.strip()
            step = 'description'
        elif step == 'description':
            question_data['description'] = None if value.strip() == '-' else value.strip()
            step = 'correct_answers'
        elif step in ('correct_answers', 'incorrect_answers'):
            answers = [line.strip() for line in value.splitlines() if line.strip()]
            minimum = 1 if step == 'correct_answers' else 3
            if len(answers) < minimum:
                return await self.answer([
                    AnswerBody(
                        text=self.text.invalid_answers(step),
                        reply_markup=self.IKB.create_edit_prompt(
                            await self.fsm.get_value('create_editing', False),
                        ),
                    )
                ])
            question_data[step] = answers
            if step == 'correct_answers':
                step = 'incorrect_answers'
            else:
                step = 'confirm'

        if await self.fsm.get_value('create_editing', False):
            step = 'confirm'
            await self.fsm.remove_value('create_editing')

        await self.fsm.update_data(create_question=question_data, create_step=step)
        if step == 'confirm':
            return await self.review_create()
        return await self.answer([
            AnswerBody(
                text=self.text.create_prompt(step),
                reply_markup=self.IKB.create_edit_prompt(
                    await self.fsm.get_value('create_editing', False),
                ),
            )
        ])

    async def edit_create_field(self, field: str):
        if field not in ('body', 'description', 'correct_answers', 'incorrect_answers'):
            return await self.review_create()
        await self.fsm.update_data(create_step=field, create_editing=True)
        step_name = {
            'correct_answers': 'correct',
            'incorrect_answers': 'incorrect',
        }.get(field, field)
        question_data = await self.fsm.get_value('create_question', {})
        current_value = question_data.get(field)
        return await self.answer([
            AnswerBody(
                text=self.text.create_prompt(step_name, current_value),
                reply_markup=self.IKB.create_edit_prompt(show_review=True),
            )
        ])

    async def review_create(self):
        question_data = await self.fsm.get_value('create_question', {})
        steps = ('body', 'description', 'correct_answers', 'incorrect_answers')
        missing_step = next(
            (
                step for step in steps
                if step not in question_data
                or (step != 'description' and not question_data[step])
                or (
                    step == 'incorrect_answers'
                    and len(question_data[step]) < 3
                )
            ),
            None,
        )
        if missing_step:
            await self.fsm.update_data(
                create_step=missing_step,
                create_editing=False,
            )
            step_name = {
                'correct_answers': 'correct',
                'incorrect_answers': 'incorrect',
            }.get(missing_step, missing_step)
            return await self.answer([
                AnswerBody(
                    text=self.text.create_prompt(
                        step_name,
                        question_data.get(missing_step),
                    ),
                    reply_markup=self.IKB.create_edit_prompt(
                        await self.fsm.get_value('create_editing', False),
                    ),
                )
            ])
        await self.fsm.update_data(create_step='confirm', create_editing=False)
        return await self.answer([
            AnswerBody(
                text=self.text.create_confirmation(question_data),
                reply_markup=self.IKB.create_confirmation(),
            )
        ])

    async def submit_create(self):
        question_data = await self.fsm.get_value('create_question', {})
        if not all(
            question_data.get(key)
            for key in ('body', 'correct_answers', 'incorrect_answers')
        ) or len(question_data.get('incorrect_answers', [])) < 3:
            return await self.review_create()
        result = await self.logic.create(
            question_data['body'],
            question_data.get('description'),
            question_data['correct_answers'],
            question_data['incorrect_answers'],
        )
        await self.fsm.set_state()
        await self.fsm.remove_value('create_question')
        await self.fsm.remove_value('create_step')
        await self.fsm.remove_value('create_editing')
        return await self.answer([
            AnswerBody(
                text=self.text.created(result),
                data=result,
                reply_markup=self.IKB.menu(),
            )
        ])

    async def cancel_create(self):
        await self.clear_quiz()
        await self.fsm.set_state()
        await self.fsm.remove_value('create_question')
        await self.fsm.remove_value('create_step')
        await self.fsm.remove_value('create_editing')
        return await self.menu()

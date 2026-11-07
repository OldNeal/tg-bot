import json
import random

from aiogram.enums import ChatMemberStatus, ChatType
from aiogram.exceptions import TelegramForbiddenError
from app.redis.base import redis_client
from app.service.base import BaseService, AnswerBody
from app.logic.question import QuestionLogic
from app.tg.text.question import QuestionText
from app.tg.buttons.question import QuestionIKB
from app.tg.fsm.state import QuestionState
from app.tg.fsm.utils import QuestionFSM
from app.exception.question import (
    AnswerCorrectError,
    AnswerInCorrectError,
    QuestionAnswersError,
    QuestionBodyError,
    QuestionExpiredError,
    QuestionModerationPendingError,
    QuestionModerationPermissionError,
    QuestionModerationReasonError,
    QuestionModerationRequestError,
    QuestionPrivateChatError,
)
from app.validate.api import QueryQuestionCreate, QuestionCreate

class QuestionService(BaseService):
    logic_class: type[QuestionLogic] = QuestionLogic
    logic: QuestionLogic
    text_class: type[QuestionText] = QuestionText
    text: type[QuestionText]
    ikb_class: type[QuestionIKB] = QuestionIKB
    IKB: QuestionIKB
    fsm_class: type[QuestionFSM] = QuestionFSM
    fsm: QuestionFSM

    async def require_private_chat(self):
        if self.chat.type != ChatType.PRIVATE:
            raise QuestionPrivateChatError()

    async def require_moderator(self):
        if self.chat.id != self.settings.question_moderation_chat_id:
            raise QuestionModerationPermissionError()
        member = await self.bot.get_chat_member(
            chat_id=self.settings.question_moderation_chat_id,
            user_id=self.tg_id,
        )
        if member.status not in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR,
        ):
            raise QuestionModerationPermissionError()

    def moderation_storage_key(self, author_tg_id: int):
        return f'question_moderation:{self.settings.question_moderation_chat_id}:{author_tg_id}'

    async def moderation_payload(self, author_tg_id: int):
        try:
            payload_text = await redis_client.get(
                self.moderation_storage_key(author_tg_id),
            )
            if payload_text is None:
                raise QuestionModerationRequestError()
            payload = json.loads(payload_text)
            request = QueryQuestionCreate.model_validate(payload['request'])
            stored_author_tg_id = int(payload['author_tg_id'])
            moderation_message_id = int(payload['moderation_message_id'])
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            raise QuestionModerationRequestError()
        if (
            payload.get('status', 'pending') != 'pending'
            or stored_author_tg_id != author_tg_id
            or moderation_message_id != self.message.message_id
            or request.purpose_user_id is None
        ):
            raise QuestionModerationRequestError()
        return payload, request, stored_author_tg_id

    async def update_moderation_message(self, payload: dict):
        await redis_client.set(
            self.moderation_storage_key(int(payload['author_tg_id'])),
            json.dumps(payload, ensure_ascii=False),
            ex=self.settings.data_ttl,
        )
        await self.bot.edit_message_text(
            text=self.text.moderation_payload(payload),
            chat_id=self.chat.id,
            message_id=self.message.message_id,
            reply_markup=(
                self.IKB.moderation_request(int(payload['author_tg_id']))
                if payload.get('status', 'pending') == 'pending'
                else None
            ),
        )

    async def clear_moderation_state(self):
        for key in (
            'moderation_payload',
            'moderation_field',
            'moderation_message_id',
            'moderation_chat_id',
            'moderation_prompt_id',
        ):
            await self.fsm.remove_value(key)
        await self.fsm.set_state()

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
        await self.require_private_chat()
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
            raise QuestionAnswersError()

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
                text=self.text.quiz(question, answers),
                data=question,
                reply_markup=self.IKB.quiz(question.question_id, answers),
            )
        ])

    async def submit_quiz_answer(self, question_id: int, answer_id: int):
        await self.require_private_chat()
        active_question_id = await self.fsm.get_value('quiz_question_id')
        answer_ids = await self.fsm.get_value('quiz_answer_ids', [])
        if active_question_id != question_id or answer_id not in answer_ids:
            raise QuestionExpiredError()
        correct_answer_id = await self.fsm.get_value('quiz_correct_answer_id')
        await self.clear_quiz()
        await self.logic.answer(question_id, answer_id)
        is_correct = answer_id == correct_answer_id
        return await self.answer([
            AnswerBody(
                text=self.text.quiz_result(is_correct),
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
        await self.require_private_chat()
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
        await self.require_private_chat()
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
        await self.require_private_chat()
        await self.clear_quiz()
        data = await self.logic.user_statistics()
        return await self.answer([
            AnswerBody(
                text=self.text.user_statistics(data.statistics),
                reply_markup=self.IKB.back_to_menu(),
            )
        ])

    async def start_create(self):
        await self.require_private_chat()
        await self.clear_quiz()
        await self.fsm.update_data(
            create_question={},
            create_step='body',
            create_editing=False,
        )
        await self.fsm.set_state(QuestionState.create)
        await self.fsm.save_message(chat_id=self.chat.id, message_id=self.message.message_id)
        return await self.answer([
            AnswerBody(
                text=self.text.create_prompt('body'),
                reply_markup=self.IKB.create_edit_prompt(),
            )
        ])

    async def create_input(self):
        value = self.message.text
        await self.require_private_chat()
        await self.fsm.save_message(chat_id=self.chat.id, message_id=self.message.message_id)
        question_data = await self.fsm.get_value('create_question', {})
        step = await self.fsm.get_value('create_step', 'body')

        if step == 'confirm':
            return await self.review_create()
        elif step == 'body':
            if not value.strip():
                raise QuestionBodyError()
            question_data['body'] = value.strip()
            step = 'description'
        elif step == 'description':
            question_data['description'] = None if value.strip() == '-' else value.strip()
            step = 'correct_answers'
        elif step in ('correct_answers', 'incorrect_answers'):
            answers = [line.strip() for line in value.splitlines() if line.strip()]
            minimum = 1 if step == 'correct_answers' else 3
            if len(answers) < minimum and step == 'correct_answers':
                raise AnswerCorrectError()
            elif len(answers) < minimum:
                raise AnswerInCorrectError()
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
        await self.require_private_chat()
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
        await self.require_private_chat()
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

    async def submit_create(self, is_anonim: bool = False):
        await self.require_private_chat()
        question_data = await self.fsm.get_value('create_question', {})
        if not all(
            question_data.get(key)
            for key in ('body', 'correct_answers', 'incorrect_answers')
        ) or len(question_data.get('incorrect_answers', [])) < 3:
            return await self.review_create()
        author_id = await self.logic.user_id
        request = QueryQuestionCreate(
            user_id=author_id,
            request_id=self.logic.request_id,
            purpose_user_id=author_id,
            question=QuestionCreate(
                body=question_data['body'],
                description=question_data.get('description'),
                correct_answers=question_data['correct_answers'],
                incorrect_answers=question_data['incorrect_answers'],
            ),
        )
        await self.send_to_moderation({
            'request': request.model_dump(mode='json'),
            'author_tg_id': self.tg_id,
            'author_name': self.user.full_name,
            'status': 'pending',
            'is_anonim':is_anonim
        })
        await self.fsm.set_state()
        await self.fsm.remove_value('create_question')
        await self.fsm.remove_value('create_step')
        await self.fsm.remove_value('create_editing')
        return await self.answer([
            AnswerBody(
                text=self.text.sent_to_moderation(),
                reply_markup=self.IKB.menu(),
            )
        ])

    async def send_to_moderation(self, payload: dict):
        storage_key = self.moderation_storage_key(
            int(payload['author_tg_id']),
        )
        stored_payload = await redis_client.get(storage_key)
        if stored_payload is not None:
            try:
                status = json.loads(stored_payload).get('status')
            except (TypeError, ValueError, json.JSONDecodeError):
                raise QuestionModerationRequestError()
            if status == 'pending':
                raise QuestionModerationPendingError()

        message = await self.bot.send_message(
            chat_id=self.settings.question_moderation_chat_id,
            text=self.text.moderation_payload(payload),
            reply_markup=self.ikb_class(self.tg_id).moderation_request(
                int(payload['author_tg_id']),
            ),
        )
        payload['moderation_message_id'] = message.message_id
        await redis_client.set(
            storage_key,
            json.dumps(payload, ensure_ascii=False),
            ex=self.settings.data_ttl,
        )
        return message

    async def moderate(
        self,
        action: str,
        field: str = '',
        author_tg_id: int | None = None,
    ):
        await self.require_moderator()
        if author_tg_id is None:
            raise QuestionModerationRequestError()
        payload, request, author_tg_id = await self.moderation_payload(author_tg_id)
        await self.clear_moderation_state()
        if action == 'edit':
            return await self.bot.edit_message_reply_markup(
                chat_id=self.chat.id,
                message_id=self.message.message_id,
                reply_markup=self.IKB.moderation_fields(author_tg_id),
            )
        if action == 'back':
            return await self.bot.edit_message_reply_markup(
                chat_id=self.chat.id,
                message_id=self.message.message_id,
                reply_markup=self.IKB.moderation_request(author_tg_id),
            )
        if action == 'field':
            if field not in (
                'body',
                'description',
                'correct_answers',
                'incorrect_answers',
            ):
                raise QuestionModerationRequestError()
            await self.fsm.update_data(
                moderation_payload=payload,
                moderation_field=field,
                moderation_message_id=self.message.message_id,
                moderation_chat_id=self.chat.id,
            )
            await self.fsm.set_state(QuestionState.moderation_edit)
            current_value = getattr(request.question, field)
            prompt = await self.bot.send_message(
                chat_id=self.chat.id,
                reply_to_message_id=self.message.message_id,
                text=self.text.moderation_edit_prompt(field, current_value),
            )
            await self.fsm.save_message(chat_id=self.chat.id, message_id=prompt.message_id)
            await self.fsm.update_data(moderation_prompt_id=prompt.message_id)
            return prompt
        if action == 'reject':
            await self.fsm.update_data(
                moderation_payload=payload,
                moderation_message_id=self.message.message_id,
                moderation_chat_id=self.chat.id,
            )
            await self.fsm.set_state(QuestionState.moderation_reason)
            prompt = await self.bot.send_message(
                chat_id=self.chat.id,
                reply_to_message_id=self.message.message_id,
                text=self.text.moderation_reason_prompt(),
            )
            await self.fsm.save_message(chat_id=self.chat.id, message_id=prompt.message_id)
            await self.fsm.update_data(moderation_prompt_id=prompt.message_id)
            return prompt
        if action == 'approve':
            approved_request = request.model_copy(
                update={'user_id': await self.logic.user_id},
            )
            created = await self.logic.create(approved_request)
            payload['status'] = 'approved'
            payload['question_id'] = created.question.question_id
            await self.update_moderation_message(payload)
            try:
                await self.bot.send_message(
                    chat_id=author_tg_id,
                    text=self.text.moderation_author_approved(payload['request']['question']['body']),
                )
            except TelegramForbiddenError:
                payload['author_notification_delivered'] = False
                await self.update_moderation_message(payload)
            return created
        raise QuestionModerationRequestError()

    async def moderation_edit_input(self):
        value = self.message.text
        await self.require_moderator()
        payload = await self.fsm.get_value('moderation_payload')
        field = await self.fsm.get_value('moderation_field')
        chat_id = await self.fsm.get_value('moderation_chat_id')
        message_id = await self.fsm.get_value('moderation_message_id')
        prompt_id = await self.fsm.get_value('moderation_prompt_id')
        if (
            not payload
            or not field
            or chat_id != self.chat.id
            or not message_id
            or not prompt_id
        ):
            raise QuestionModerationRequestError()

        request = QueryQuestionCreate.model_validate(payload['request'])
        if field == 'body':
            if not value.strip():
                raise QuestionBodyError()
            updated_value = value.strip()
        elif field == 'description':
            updated_value = None if value.strip() == '-' else value.strip()
        elif field in ('correct_answers', 'incorrect_answers'):
            updated_value = [line.strip() for line in value.splitlines() if line.strip()]
            if field == 'correct_answers' and not updated_value:
                raise AnswerCorrectError()
            if field == 'incorrect_answers' and len(updated_value) < 3:
                raise AnswerInCorrectError()
        else:
            raise QuestionModerationRequestError()

        updated_question = request.question.model_copy(
            update={field: updated_value},
        )
        updated_request = request.model_copy(update={'question': updated_question})
        payload['request'] = updated_request.model_dump(mode='json')
        await redis_client.set(
            self.moderation_storage_key(int(payload['author_tg_id'])),
            json.dumps(payload, ensure_ascii=False),
            ex=self.settings.data_ttl,
        )
        await self.bot.edit_message_text(
            text=self.text.moderation_payload(payload),
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=self.IKB.moderation_request(
                int(payload['author_tg_id']),
            ),
        )
        await self.clear_moderation_state()

    async def moderation_rejection_reason(self):
        reason = self.message.text
        await self.require_moderator()
        payload = await self.fsm.get_value('moderation_payload')
        message_id = await self.fsm.get_value('moderation_message_id')
        chat_id = await self.fsm.get_value('moderation_chat_id')
        prompt_id = await self.fsm.get_value('moderation_prompt_id')
        if (
            not payload
            or not message_id
            or chat_id != self.chat.id
            or not prompt_id
        ):
            raise QuestionModerationRequestError()
        if not reason.strip():
            raise QuestionModerationReasonError()

        payload['status'] = 'rejected'
        payload['reason'] = reason.strip()
        await redis_client.set(
            self.moderation_storage_key(int(payload['author_tg_id'])),
            json.dumps(payload, ensure_ascii=False),
            ex=self.settings.data_ttl,
        )
        try:
            await self.bot.send_message(
                chat_id=int(payload['author_tg_id']),
                text=self.text.moderation_author_rejected(payload['request']['question']['body'], reason.strip()),
            )
        except TelegramForbiddenError:
            payload['author_notification_delivered'] = False
        await self.bot.edit_message_text(
            text=self.text.moderation_payload(payload),
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=None,
        )
        await self.clear_moderation_state()

    async def cancel_create(self):
        await self.clear_quiz()
        await self.fsm.set_state()
        await self.fsm.remove_value('create_question')
        await self.fsm.remove_value('create_step')
        await self.fsm.remove_value('create_editing')
        return await self.menu()

    async def go_private_chat(self):
        return await self.answer([
            AnswerBody(
                text=self.text.private_chat_func(),
                reply_markup=self.IKB.deep_menu(self.message.message_id, self.message.chat.id),
            )
        ])
from app.api.schemas import (
    AnswerQuestion,
    AnswerQuestionStatistics,
    Question,
    QuestionAnswer,
    UserQuestionStatistics,
)
from app.tg.text.base import BaseText


class QuestionText(BaseText):
    @classmethod
    def menu(cls):
        return '❔ Меню вопросов'

    @classmethod
    def unknown_subcommand(cls, subcommand: str):
        return cls.html('❌ Неизвестная подкоманда: ') + cls.html(subcommand).escape()

    @classmethod
    def question(cls, question: Question):
        text = cls.html('❔ ') + cls.html(question.body).escape()
        if question.description:
            text += cls.html.separator(n=2) + '📜 Описание' + cls.html(question.description).escape().blockquote(True)
        return text

    @classmethod
    def question_list(cls, count: int, page: int, max_page: int):
        return f'📝 Ваши вопросы ({count} шт.) {cls.page_text(page, max_page)}'

    @classmethod
    def created(cls):
        return '➕ Вопрос создан'

    @classmethod
    def sent_to_moderation(cls):
        return '✅ Заявка отправлена на модерацию. Результат придёт в личный чат с ботом.'

    @classmethod
    def json_create_prompt(cls):
        return (
            '📋 Отправьте JSON-объект или массив объектов с полями '
            '<code>body</code>, <code>correct_answers</code>, '
            '<code>incorrect_answers</code> и необязательным '
            '<code>description</code>. Для каждого вопроса нужен минимум '
            'один правильный и три неправильных ответа. '
            'Каждый вопрос будет отправлен модераторам отдельной заявкой.'
            + cls.html.separator(n=2)
            + '<code>{"body":"Вопрос?","description":"Описание",'
            '"correct_answers":["Да"],"incorrect_answers":["Нет","Возможно","Не знаю"]}</code>'
        )

    @classmethod
    def json_create_error(cls, message: str):
        return cls.html('❌ ').bold() + cls.html(message).escape()

    @classmethod
    def json_create_result(cls, count: int):
        return (
            f'✅ Отправлено вопросов на модерацию: {count}. '
            'Каждый вопрос рассматривается отдельно.'
        )

    @classmethod
    def empty(cls):
        return '❌ Вопросы не найдены'

    @classmethod
    def create_prompt(cls, step: str, current_value=None):
        prompts = {
            'body': '✒️ Введите текст вопроса',
            'description': '📝 Введите описание или отправьте «-», чтобы пропустить',
            'correct': '✅ Введите правильные варианты ответа, каждый с новой строки',
            'incorrect': '❌ Введите неправильные варианты ответа, каждый с новой строки',
        }
        step = {
            'correct_answers': 'correct',
            'incorrect_answers': 'incorrect',
        }.get(step, step)
        text = prompts[step]
        if current_value:
            if isinstance(current_value, list):
                current_value = cls.html.separator().join(current_value)
            text = (
                cls.html(text)
                + cls.html.separator(n=2)
                + 'Текущее значение:'
                + cls.html.separator()
                + cls.html(str(current_value)).escape()
            )
        return cls.html(text)

    @classmethod
    def statistics(cls, data: AnswerQuestionStatistics, question: Question):
        lines = []
        for answer in data.answers:
            percent = (
                answer.count / data.statistics.total * 100
                if data.statistics.total
                else 0
            )
            lines.append(
                cls.html(answer.body).escape()
                + f': {answer.count} ({percent:.1f}%)'
            )
        return cls.html(f'🧮 Всего ответов на вопрос: {data.statistics.total}') + cls.html.separator(n=2) + cls.html('📊 Статистика ответов') + cls.html.separator().join(lines).blockquote()

    @classmethod
    def question_card(cls, question: Question, statistics: AnswerQuestionStatistics):
        return f'{cls.question(question)}{cls.html.separator(n=2)}{cls.statistics(statistics, question)}'

    @classmethod
    def quiz(cls, question: Question, answers: list[QuestionAnswer]):
        answer_lines = [
            cls.html(f'{index}. ').bold() + cls.html(answer.body).escape()
            for index, answer in enumerate(answers, start=1)
        ]
        return (
            cls.question(question)
            + cls.html.separator(n=2)
            + cls.html('Варианты ответа:').bold()
            + cls.html.separator()
            + cls.html.separator().join(answer_lines)
        )

    @classmethod
    def quiz_result(
        cls,
        is_correct: bool,
    ):
        return '✅ Правильно' if is_correct else '❌ Неправильно'

    @classmethod
    def create_confirmation(cls, data: dict):
        return (
            cls.html('📝 Проверьте вопрос перед созданием').bold()
          + cls.html.separator(n=2) + cls.create_text(data) + cls.html.separator()
          + cls.html('✒️ Вы можете изменить любое поле перед созданием.')
          )

    @classmethod
    def create_text(cls, data: dict):
        description = data.get('description')
        correct_answers = cls.html.to_list(
            [str(cls.html(answer).escape()) for answer in data['correct_answers']],
            type='bullet',
        )
        incorrect_answers = cls.html.to_list(
            [str(cls.html(answer).escape()) for answer in data['incorrect_answers']],
            type='bullet',
        )
        return cls.html.separator().join([
            cls.html('❔ ') + cls.html(data['body']).escape().code() + cls.html.separator(),
            cls.html('📜 Описание:') + (cls.html(description).escape().code().blockquote() if description else cls.html(' ❌') + cls.html.separator()),
            cls.html('✅ Правильные варианты:') + correct_answers.code().blockquote(True),
            cls.html('❌ Неправильные варианты:') + incorrect_answers.code().blockquote(True),
        ])

    @classmethod
    def moderation_payload(cls, data: dict):
        request = data['request']['question']
        text = ''
        if not data.get('is_anonim', False):
            text = (
            cls.html('📝 Новый вопрос от ')
            + cls.html(data.get('author_name', 'Пользователь'))
            .escape()
            .openmessage(int(data['author_tg_id'])))
        else:
            text = cls.html('📝 Новый вопрос')
        text += cls.html.separator(n=2)
        text += cls.create_text(request)
        
        status = data.get('status', 'pending')
        if status == 'approved':
            text += cls.html.separator(n=2) + '✅ Вопрос создан'
        elif status == 'rejected':
            text += (
                cls.html.separator(n=2)
                + '🗑 Вопрос отклонён. Причина: '
                + cls.html(data['reason']).escape()
            )
        return text

    @classmethod
    def moderation_edit_prompt(cls, field: str, current_value):
        labels = {
            'body': 'текст вопроса',
            'description': 'описание (или «-», чтобы очистить)',
            'correct_answers': 'правильные ответы, каждый с новой строки',
            'incorrect_answers': 'неправильные ответы, каждый с новой строки',
        }
        value = (
            cls.html.separator(n=2)
            + 'Текущее значение:'
            + cls.html.separator()
            + cls.html(str(current_value if current_value is not None else '❌'))
            .escape()
            .blockquote()
            if field in ('body', 'description')
            else cls.html.separator(n=2)
            + 'Текущие варианты:'
            + cls.html.separator()
            + cls.html('\n').join(current_value or ['❌']).escape().blockquote()
        )
        return cls.html(
            f'✒️ Отправьте новое {labels[field]} отдельным сообщением в группе.'
        ) + value

    @classmethod
    def moderation_reason_prompt(cls):
        return '✒️ Отправьте причину отказа отдельным сообщением в группе.'

    @classmethod
    def moderation_author_approved(cls, question: str):
        return f'✅ Ваш вопрос "{cls.html(question).escape()}" прошёл модерацию и создан.'

    @classmethod
    def moderation_author_rejected(cls, question: str, reason: str):
        return cls.html(f'❌ Ваш вопрос "{cls.html(question).escape()}" отклонён. Причина: {cls.html(reason).escape()}')

    @classmethod
    def user_statistics(cls, statistics: UserQuestionStatistics):
        return cls.html('📊 Статистика ваших ответов').bold() + cls.html.separator().join([
            cls.html(f'🧮 Всего ответов: {statistics.total}'),
            cls.html(f'✅ Правильные: {statistics.correct}'),
            cls.html(f'❌ Неправильные: {statistics.incorrect}'),
            cls.html(f'🎯 Точность: {statistics.accuracy:.1f}%'),
        ]).blockquote()

from app.api.schemas import (
    AnswerQuestion,
    AnswerQuestionStatistics,
    Question,
    UserQuestionStatistics,
)
from app.tg.text.base import BaseText
from app.tg.text.utils import TextHTML


class QuestionText(BaseText):
    @classmethod
    def menu(cls):
        return '❔ Меню вопросов'

    @classmethod
    def unknown_subcommand(cls, subcommand: str):
        return TextHTML('❌ Неизвестная подкоманда: ') + TextHTML(subcommand).escape()

    @classmethod
    def question(cls, question: Question, page: int | None = None, max_page: int | None = None):
        text = TextHTML('❔ ') + TextHTML(question.body).escape()
        if question.description:
            text += '\n\n' + TextHTML(question.description).escape()
        if page is not None and max_page is not None:
            text += f'\n\n📄 {page + 1}/{max_page}'
        return text

    @classmethod
    def question_list(cls, count: int, page: int, max_page: int):
        return TextHTML(f'📝 Ваши вопросы\nВсего: {count} · Страница {page + 1}/{max_page}')

    @classmethod
    def created(cls, data: AnswerQuestion):
        return f'✅ Вопрос создан\n\n{cls.question(data.question)}'

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
                current_value = '\n'.join(current_value)
            text = (
                TextHTML(text)
                + '\n\nТекущее значение:\n'
                + TextHTML(str(current_value)).escape().blockquote()
            )
        return TextHTML(text)

    @classmethod
    def invalid_answers(cls, step: str):
        if step == 'correct_answers':
            return TextHTML('❌ Добавьте хотя бы один правильный ответ, каждый с новой строки')
        return TextHTML('❌ Добавьте хотя бы 3 неправильных ответа, каждый с новой строки')

    @classmethod
    def invalid_question(cls):
        return TextHTML('❌ Текст вопроса не может быть пустым')

    @classmethod
    def statistics(cls, data: AnswerQuestionStatistics, question: Question):
        lines = [
            TextHTML('📊 ') + TextHTML(question.body).escape().bold(),
            TextHTML(f'Всего ответов на вопрос: {data.statistics.total}'),
        ]
        for answer in data.answers:
            percent = (
                answer.count / data.statistics.total * 100
                if data.statistics.total
                else 0
            )
            result = ' ✅' if answer.is_correct else ''
            lines.append(
                TextHTML(answer.body).escape()
                + f'{result} — {answer.count} ({percent:.1f}%)'
            )
        return TextHTML('\n').join(lines)

    @classmethod
    def question_card(cls, question: Question, statistics: AnswerQuestionStatistics):
        return f'{cls.question(question)}\n\n{cls.statistics(statistics, question)}'

    @classmethod
    def quiz(cls, question: Question):
        text = TextHTML('🎲 ') + TextHTML(question.body).escape().bold().blockquote()
        if question.description:
            text += '\n\n' + TextHTML(question.description).escape().blockquote()
        return text + '\n\nВыберите правильный ответ:'

    @classmethod
    def quiz_unavailable(cls):
        return TextHTML('❌ Для вопроса нужны минимум 1 правильный и 3 неправильных ответа.')

    @classmethod
    def quiz_expired(cls):
        return TextHTML('❌ Этот вопрос уже недоступен. Запросите случайный вопрос заново.')

    @classmethod
    def quiz_result(
        cls,
        question: Question,
        selected_answer: str,
        correct_answer: str,
        is_correct: bool,
    ):
        result = TextHTML('✅ Правильно!' if is_correct else '❌ Неправильно')
        text = (
            result
            + '\n\n❔ '
            + TextHTML(question.body).escape().bold().blockquote()
            + '\nВаш ответ:\n'
            + TextHTML(selected_answer).escape().blockquote()
        )
        if not is_correct:
            text += (
                '\nПравильный ответ:\n'
                + TextHTML(correct_answer).escape().blockquote()
            )
        return text

    @classmethod
    def create_confirmation(cls, data: dict):
        description = data.get('description')
        correct_answers = TextHTML.to_list(
            [str(TextHTML(answer).escape()) for answer in data['correct_answers']],
            type='bullet',
        )
        incorrect_answers = TextHTML.to_list(
            [str(TextHTML(answer).escape()) for answer in data['incorrect_answers']],
            type='bullet',
        )
        return TextHTML('\n').join([
            TextHTML('📝 Проверьте вопрос перед созданием').bold(),
            TextHTML('❔ ') + TextHTML(data['body']).escape().blockquote(),
            TextHTML('Описание:'),
            TextHTML(description).escape().blockquote() if description else TextHTML('—'),
            TextHTML('✅ Правильные варианты:'),
            correct_answers,
            TextHTML('❌ Неправильные варианты:'),
            incorrect_answers,
            TextHTML('Вы можете изменить любое поле перед созданием.'),
        ])

    @classmethod
    def user_statistics(cls, statistics: UserQuestionStatistics):
        return TextHTML('\n').join([
            TextHTML('📊 Статистика ваших ответов').bold(),
            TextHTML(f'Всего ответов: {statistics.total}'),
            TextHTML(f'✅ Правильные: {statistics.correct}'),
            TextHTML(f'❌ Неправильные: {statistics.incorrect}'),
            TextHTML(f'Точность: {statistics.accuracy:.1f}%'),
        ])

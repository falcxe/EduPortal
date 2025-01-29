// static/js/test_form.js

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('add_question').addEventListener('click', function() {
        const questionId = Date.now(); // Уникальный идентификатор для каждого вопроса
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question-block';
        questionDiv.innerHTML = `
            <input type="text" name="question_${questionId}_text" placeholder="Вопрос" required>
            <div class="answers" id="answers_${questionId}">
                <div class="answer">
                    <input type="text" name="answer_${questionId}_0_text" placeholder="Ответ" style="flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                    <input type="radio" name="correct_answer_${questionId}" value="0" style="width: 20px; height: 20px; transform: scale(0.8); margin-right: 10px;">
                </div>
            </div>
            <button type="button" class="add-answer" data-question-id="${questionId}">Добавить ответ</button>
            <p>Отметьте правильный ответ</p>
        `;
        document.getElementById('questions_container').appendChild(questionDiv);
    });

    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('add-answer')) {
            const questionId = e.target.getAttribute('data-question-id');
            const answersDiv = document.getElementById(`answers_${questionId}`);
            const answerCount = answersDiv.children.length;
            const answerDiv = document.createElement('div');
            answerDiv.className = 'answer';
            answerDiv.innerHTML = `
                <input type="text" name="answer_${questionId}_${answerCount}_text" placeholder="Ответ" style="flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                <input type="radio" name="correct_answer_${questionId}" value="${answerCount}" style="width: 20px; height: 20px; transform: scale(0.8); margin-right: 10px;">
            `;
            answersDiv.appendChild(answerDiv);
        }
    });
});
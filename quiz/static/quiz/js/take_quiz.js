let currentStep = 0;
let selectedChoices = []; 
const totalQuestions = document.querySelectorAll('.question-card').length;

function handleSelection(qId, cId, el, qType) {
    if (qType === 'MULTI') {
        el.classList.toggle('selected');
        if (selectedChoices.includes(cId)) {
            selectedChoices = selectedChoices.filter(id => id !== cId);
        } else {
            selectedChoices.push(cId);
        }
        const btn = document.getElementById(`btn-${qId}`);
        btn.style.visibility = selectedChoices.length > 0 ? 'visible' : 'hidden';
    } else {
        sendResult(qId, [cId]);
    }
}

async function submitMulti(qId) {
    if (selectedChoices.length === 0) return;
    await sendResult(qId, selectedChoices);
}

async function sendResult(qId, choiceIds) {
    const card = document.getElementById(`q-card-${qId}`);
    card.style.pointerEvents = 'none';

    try {
        // 1. Беремо URL та CSRF-токен з нашого конфігу
        const response = await fetch(window.QuizConfig.checkAnswerUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': window.QuizConfig.csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question_id: qId, choice_ids: choiceIds })
        });

        const data = await response.json();

        choiceIds.forEach(id => {
            const el = document.getElementById(`choice-${id}`);
            if (data.is_correct) {
                el.style.background = '#d4edda';
                el.style.borderColor = '#28a745';
            } else {
                el.style.background = '#f8d7da';
                el.style.borderColor = '#dc3545';
            }
        });

        if (!data.is_correct) {
            data.correct_ids.forEach(id => {
                const correctEl = document.getElementById(`choice-${id}`);
                if (correctEl) {
                    correctEl.style.border = '2px solid #28a745';
                    correctEl.style.background = '#f0fff4';
                }
            });
        }

        setTimeout(() => {
            if (currentStep + 1 < totalQuestions) {
                nextQuestion();
                selectedChoices = [];
            } else {
                showFinalResult();
            }
        }, 1500);

    } catch (error) {
        console.error("Помилка:", error);
        card.style.pointerEvents = 'auto';
    }
}

async function showFinalResult() {
    document.getElementById('quiz-title').style.display = 'none';
    
    const response = await fetch(window.QuizConfig.finalScoreUrl);
    const data = await response.json();

    window.location.href = ""
}

function nextQuestion() {
    const cards = document.querySelectorAll('.question-card');
    cards[currentStep].classList.remove('active');
    currentStep++;
    cards[currentStep].classList.add('active');
}

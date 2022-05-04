const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modalbody')
const startBtn = document.getElementById('start-button')

const url1 = window.location.href

modalBtns.forEach(modalBtn=> modalBtn.addEventListener('click', ()=>{
    const id = modalBtn.getAttribute('data-bs-pk')
    const topic = modalBtn.getAttribute('data-bs-topic')
    const numQuestions = modalBtn.getAttribute('data-bs-questions')
    const difficulty = modalBtn.getAttribute('data-bs-difficulty')
    const scoreToPass = modalBtn.getAttribute('data-bs-pass')
    const time = modalBtn.getAttribute('data-bs-time')

    modalBody.innerHTML = `
        <div class="h5 mb-3">Are you sure you want to begin "<b>${topic}</b>"?</div>
        <div class="text-muted">
            <ul>
                <li>Difficulty: <b>${difficulty}</b></li>
                <li>Number of questions: <b>${numQuestions}</b></li>
                <li>Score to pass: <b>${scoreToPass}%</b></li>
                <li>Time: <b>${time} mins</b></li>
            </ul>
        </div>
    `

    startBtn.addEventListener('click', ()=>{
        window.location.href = url1 + "/" + id
    })
}))
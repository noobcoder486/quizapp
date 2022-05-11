const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modalbody')
const startBtn = document.getElementById('start-button')

const url = window.location.href

modalBtns.forEach(modalBtn=> modalBtn.addEventListener('click', ()=>{
    const id = modalBtn.getAttribute('data-bs-pk')
    const topic = modalBtn.getAttribute('data-bs-topic')
    const time = modalBtn.getAttribute('data-bs-time')

    modalBody.innerHTML = `
        <div class="h5 mb-3">Are you sure you want to begin "<b>${topic}</b>"?</div>
        <div class="text-muted">
                Time: <b>${time} mins</b>
        </div>
    `
    startBtn.addEventListener('click', ()=>{
        window.location.href = url + id
    })
}))
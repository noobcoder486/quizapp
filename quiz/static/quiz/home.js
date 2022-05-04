const subject_buttons = [...document.getElementsByClassName('modal-button1')]

const url=window.location.href

subject_buttons.forEach(SubBtn=> SubBtn.addEventListener('click', ()=>{
    const id = SubBtn.getAttribute('data-bs-pk')
    window.location.href = url + id;
}))

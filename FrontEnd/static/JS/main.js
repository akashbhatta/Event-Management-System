let currentPage = 1;

function changePage(direction) {
    currentPage += direction;
    const page1 = document.querySelectorAll('.page-1');
    const page2 = document.querySelectorAll('.page-2');

    if (currentPage === 1) {
        page1.forEach(el => el.style.display = 'block');
        page2.forEach(el => el.style.display = 'none');
        document.getElementById('prevBtn').disabled = true;
        document.getElementById('nextBtn').disabled = false;
    } else {
        page1.forEach(el => el.style.display = 'none');
        page2.forEach(el => el.style.display = 'block');
        document.getElementById('prevBtn').disabled = false;
        document.getElementById('nextBtn').disabled = true;
    }
    document.getElementById('pageIndicator').innerText = `Page ${currentPage} of 2`;
}

function filterEvents() {
    let filter = document.getElementById('eventSearch').value.toUpperCase();
    let cards = document.getElementsByClassName('event-card');
    for (let i = 0; i < cards.length; i++) {
        let title = cards[i].querySelector(".card-title").innerText;
        cards[i].style.display = title.toUpperCase().indexOf(filter) > -1 ? "" : "none";
    }
}

// Загрузка списка кабинетов
fetch('/api/rooms')
    .then(res => res.json())
    .then(rooms => {
        const select = document.getElementById('roomSelect');
        rooms.forEach(r => {
            const opt = document.createElement('option');
            opt.value = r.number;
            opt.textContent = `${r.number} (этаж ${r.floor})`;
            select.appendChild(opt);
        });
    });

// Построение маршрута
function showRoute() {
    const num = document.getElementById('roomSelect').value;
    if (!num) return alert("Выберите кабинет из списка");
    fetch(`/api/route/${num}`)
        .then(res => res.json())
        .then(data => {
            const resDiv = document.getElementById('result');
            const hl = document.getElementById('highlight');
            const img = document.getElementById('floorMap');
            if (data.success) {
                resDiv.innerHTML = data.route;
                hl.style.display = 'block';
                hl.style.left = data.room.x + 'px';
                hl.style.top = data.room.y + 'px';
                img.src = `/static/images/floor${data.room.floor}.png`;
            } else {
                resDiv.innerHTML = `<p style="color:red;">${data.error}</p>`;
                hl.style.display = 'none';
            }
        });
}

// Уведомление о запрете курения
setInterval(() => {
    const delay = Math.floor(Math.random() * 7000) + 3000; // 3–10 сек
    setTimeout(() => {
        alert('⚠️ Внимание! Курение запрещено в зоне колледжа и рядом с прокуратурой!');
    }, delay);
}, 10000);
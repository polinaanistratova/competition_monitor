function openTab(tabName) {
    const tabs = document.querySelectorAll('.tab-content');
    const btns = document.querySelectorAll('.tab-btn');
    tabs.forEach(t => t.classList.remove('active'));
    btns.forEach(b => b.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');
    event.currentTarget.classList.add('active');
}

async function analyzeText() {
    const text = document.getElementById('textInput').value;
    const result = document.getElementById('textResult');
    result.textContent = 'Анализирую...';
    try {
        const formData = new FormData();
        formData.append('text', text);
        const res = await fetch('/analyzetext', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        result.textContent = JSON.stringify(data, null, 2);
    } catch (e) {
        result.textContent = 'Ошибка: ' + e;
    }
}

async function analyzeImage() {
    const file = document.getElementById('imageFile').files[0];
    const result = document.getElementById('imageResult');
    if (!file) {
        result.textContent = 'Выберите файл';
        return;
    }
    result.textContent = 'Анализирую...';
    try {
        const formData = new FormData();
        formData.append('file', file);
        const res = await fetch('/analyzeimage', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        result.textContent = JSON.stringify(data, null, 2);
    } catch (e) {
        result.textContent = 'Ошибка: ' + e;
    }
}

async function runParse() {
    const result = document.getElementById('parseResult');
    result.textContent = 'Парсинг...';
    try {
        const res = await fetch('/parsedemo');
        const data = await res.json();
        result.textContent = JSON.stringify(data, null, 2);
    } catch (e) {
        result.textContent = 'Ошибка: ' + e;
    }
}

async function getHistory() {
    const result = document.getElementById('parseResult');
    result.textContent = 'Загружаю историю...';
    try {
        const res = await fetch('/history');
        const data = await res.json();
        result.textContent = JSON.stringify(data, null, 2);
    } catch (e) {
        result.textContent = 'Ошибка: ' + e;
    }
}

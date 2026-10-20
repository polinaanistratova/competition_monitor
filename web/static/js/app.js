function openTab(tabName) {
    const tabs = document.querySelectorAll('.tab-content');
    const btns = document.querySelectorAll('.tab-btn');
    tabs.forEach(t => t.classList.remove('active'));
    btns.forEach(b => b.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');
    event.currentTarget.classList.add('active');
}

function formatResult(data) {
    if (data.error) return '<div style="color: #dc3545; font-weight: 600;">Ошибка: ' + data.error + '</div>';
    if (typeof data === 'object') {
        let html = '';
        
        if (data.competitor_name || data.overall_summary) {
            html += '<div class="result-section">';
            if (data.competitor_name) html += '<div class="result-title">🎯 Конкурент</div><div>' + data.competitor_name + '</div>';
            if (data.overall_summary) html += '<div style="margin-top: 10px;"><b>Краткое резюме:</b><br>' + data.overall_summary + '</div>';
            html += '</div>';
        }
        
        if (data.design_score !== undefined || data.animation_potential !== undefined) {
            html += '<div class="result-section">';
            html += '<div class="result-title">📊 Оценка</div>';
            if (data.design_score !== undefined) html += '<span class="result-score">🎨 Дизайн: ' + data.design_score + '/10</span>';
            if (data.animation_potential !== undefined) html += '<span class="result-score">✨ Анимация: ' + data.animation_potential + '/10</span>';
            html += '</div>';
        }
        
        if (data.strong_sides || data.weak_sides) {
            html += '<div class="result-section">';
            if (data.strong_sides) {
                html += '<div class="result-title">✅ Сильные стороны</div><ul class="result-list">';
                data.strong_sides.forEach(s => html += '<li>' + s + '</li>');
                html += '</ul>';
            }
            if (data.weak_sides) {
                html += '<div class="result-title" style="margin-top: 16px;">⚠️ Слабые стороны</div><ul class="result-list">';
                data.weak_sides.forEach(s => html += '<li>' + s + '</li>');
                html += '</ul>';
            }
            html += '</div>';
        }
        
        if (data.key_services) {
            html += '<div class="result-section">';
            html += '<div class="result-title">🛠 Ключевые услуги</div><ul class="result-list">';
            data.key_services.forEach(s => html += '<li>' + s + '</li>');
            html += '</ul>';
            html += '</div>';
        }
        
        if (data.target_audience || data.pricing_hints) {
            html += '<div class="result-section">';
            if (data.target_audience) html += '<div class="result-title">👥 Целевая аудитория</div><div>' + data.target_audience + '</div>';
            if (data.pricing_hints) {
                html += '<div class="result-title" style="margin-top: 16px;">💰 О ценообразовании</div><ul class="result-list">';
                data.pricing_hints.forEach(s => html += '<li>' + s + '</li>');
                html += '</ul>';
            }
            html += '</div>';
        }
        
        if (data.style_analysis || data.color_palette || data.typography) {
            html += '<div class="result-section">';
            html += '<div class="result-title">🎨 Визуальный анализ</div>';
            if (data.style_analysis) html += '<div style="margin-bottom: 10px;"><b>Стиль:</b> ' + data.style_analysis + '</div>';
            if (data.color_palette) html += '<div style="margin-bottom: 10px;"><b>Цветовая палитра:</b> ' + data.color_palette.join(', ') + '</div>';
            if (data.typography) html += '<div><b>Типографика:</b> ' + data.typography + '</div>';
            html += '</div>';
        }
        
        if (data.visual_strengths || data.visual_weaknesses) {
            html += '<div class="result-section">';
            if (data.visual_strengths) {
                html += '<div class="result-title">💪 Визуальные сильные стороны</div><ul class="result-list">';
                data.visual_strengths.forEach(s => html += '<li>' + s + '</li>');
                html += '</ul>';
            }
            if (data.visual_weaknesses) {
                html += '<div class="result-title" style="margin-top: 16px;">📉 Визуальные слабости</div><ul class="result-list">';
                data.visual_weaknesses.forEach(s => html += '<li>' + s + '</li>');
                html += '</ul>';
            }
            html += '</div>';
        }
        
        if (data.recommendations || data.inspiration_takeaways) {
            html += '<div class="result-section">';
            if (data.recommendations) {
                html += '<div class="result-title">💡 Рекомендации</div><ul class="result-list">';
                data.recommendations.forEach(s => html += '<li>' + s + '</li>');
                html += '</ul>';
            }
            if (data.inspiration_takeaways) {
                html += '<div class="result-title" style="margin-top: 16px;">✨ Что можно позаимствовать</div><ul class="result-list">';
                data.inspiration_takeaways.forEach(s => html += '<li>' + s + '</li>');
                html += '</ul>';
            }
            html += '</div>';
        }
        
        if (data.results || Array.isArray(data)) {
            html += '<pre style="background: #f8f9fa; padding: 16px; border-radius: 8px; overflow-x: auto;">' + JSON.stringify(data, null, 2) + '</pre>';
        }
        
        if (html) return html;
    }
    return '<pre style="background: #f8f9fa; padding: 16px; border-radius: 8px; overflow-x: auto;">' + JSON.stringify(data, null, 2) + '</pre>';
}

async function analyzeText() {
    const text = document.getElementById('textInput').value;
    const result = document.getElementById('textResult');
    if (!text.trim()) {
        result.innerHTML = '<div style="color: #dc3545;">Введите текст для анализа</div>';
        return;
    }
    result.innerHTML = '<div style="text-align: center; padding: 40px; color: #667eea;">⏳ Анализирую...</div>';
    try {
        const formData = new FormData();
        formData.append('text', text);
        const res = await fetch('/analyzetext', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        result.innerHTML = formatResult(data);
    } catch (e) {
        result.innerHTML = '<div style="color: #dc3545;">Ошибка: ' + e + '</div>';
    }
}

async function analyzeImage() {
    const file = document.getElementById('imageFile').files[0];
    const result = document.getElementById('imageResult');
    if (!file) {
        result.innerHTML = '<div style="color: #dc3545;">Выберите файл изображения</div>';
        return;
    }
    result.innerHTML = '<div style="text-align: center; padding: 40px; color: #667eea;">⏳ Анализирую изображение...</div>';
    try {
        const formData = new FormData();
        formData.append('file', file);
        const res = await fetch('/analyzeimage', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        result.innerHTML = formatResult(data);
    } catch (e) {
        result.innerHTML = '<div style="color: #dc3545;">Ошибка: ' + e + '</div>';
    }
}

async function runParse() {
    const result = document.getElementById('parseResult');
    result.innerHTML = '<div style="text-align: center; padding: 40px; color: #667eea;">⏳ Выполняется парсинг...</div>';
    try {
        const res = await fetch('/parsedemo');
        const data = await res.json();
        result.innerHTML = formatResult(data);
    } catch (e) {
        result.innerHTML = '<div style="color: #dc3545;">Ошибка: ' + e + '</div>';
    }
}

async function getHistory() {
    const result = document.getElementById('parseResult');
    result.innerHTML = '<div style="text-align: center; padding: 40px; color: #667eea;">⏳ Загружаю историю...</div>';
    try {
        const res = await fetch('/history');
        const data = await res.json();
        result.innerHTML = formatResult(data);
    } catch (e) {
        result.innerHTML = '<div style="color: #dc3545;">Ошибка: ' + e + '</div>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Логика Входа
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            console.log('Login attempt');
            window.location.href = '/register'; // Перенаправление на регистрацию
        });
    }

    // Логика Регистрации
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            console.log('Register attempt');
            window.location.href = '/verification'; // Перенаправление на верификацию
        });
    }
    // Логика Выбора роли
    const roleBtns = document.querySelectorAll('.role-btn');
    roleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            console.log('Role selected:', btn.innerText);
            alert('Role selected: ' + btn.innerText);
        });
    });
});
// --- Логика для role.html (Выбор роли) ---
const roleLinks = document.querySelectorAll('.role-link');
roleLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        // Здесь можно добавить анимацию или сохранить выбор в базу данных
        console.log('Выбрана роль:', link.querySelector('.role-btn').innerText);
        
        // Перенаправление происходит автоматически по ссылке <a href="...">
    });
});

// static/script.js

const verForm = document.getElementById('verification-form');
if (verForm) {
    verForm.addEventListener('submit', (e) => {
        e.preventDefault(); // Останавливаем стандартную отправку
        console.log('Verification attempt');

        // --- ЭТОТ КОД ДОЛЖЕН БЫТЬ ТУТ ---
        window.location.href = '/role'; 
        // --------------------------------
    });
}
document.addEventListener('DOMContentLoaded', () => {
    const card = document.querySelector('.glass-card');
    const buttons = document.querySelectorAll('.btn-lang');

    // 1. Эффект наклона за мышкой (как на премиум сайтах)
    document.addEventListener('mousemove', (e) => {
        let x = (window.innerWidth / 2 - e.pageX) / 40;
        let y = (window.innerHeight / 2 - e.pageY) / 40;
        
        card.style.transform = `rotateX(${y}deg) rotateY(${-x}deg)`;
    });

    // 2. Интерактивная подсветка фона при выборе роли
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            if (btn.innerText.includes('Startup')) {
                document.body.style.background = "radial-gradient(circle at center, #0d3d2b 0%, #0a0a12 100%)";
            } else {
                document.body.style.background = "radial-gradient(circle at center, #1a1a2e 0%, #0a0a12 100%)";
            }
        });

        btn.addEventListener('mouseleave', () => {
            // Возвращаем твой стандартный фон
            document.body.style.background = ""; 
        });
    });
});
async function loadProjects() {
    // В будущем здесь будет: const response = await fetch('https://api.crunchbase.com/...')
    const projects = [ /* Вставь сюда JSON выше или загрузи файл */ ];
    
    const grid = document.querySelector('.projects-grid');
    grid.innerHTML = ''; // Очищаем сетку перед загрузкой

    projects.forEach(project => {
        const progress = Math.round((project.raised / project.goal) * 100);
        
        const card = `
            <div class="glass-card project-card animate-fade-in">
                <div class="card-tag">${project.category}</div>
                <div class="project-info">
                    <h3>${project.title}</h3>
                    <p>${project.description}</p>
                    
                    <div class="funding-status">
                        <div class="progress-container">
                            <div class="progress-line" style="width: ${progress}%;"></div>
                        </div>
                        <div class="funding-details">
                            <span>Raised: <strong>$${project.raised.toLocaleString()}</strong></span>
                            <span>${progress}%</span>
                        </div>
                    </div>
                    <span class="goal">Goal: $${project.goal.toLocaleString()}</span>
                </div>
                <button class="btn-main invest-btn">INVEST NOW</button>
            </div>
        `;
        grid.innerHTML += card;
    });
}

// Запускаем при загрузке страницы
document.addEventListener('DOMContentLoaded', loadProjects);
// 1. ПОЛУЧАЕМ ДАННЫЕ (Имитация запроса к API)
const apiData = [
    { "title": "EcoEnergy", "raised": 40000, "goal": 50000 },
    { "title": "AI Medical", "raised": 15000, "goal": 100000 }
];

// 2. НАХОДИМ МЕСТО НА СТРАНИЦЕ
const container = document.querySelector('.projects-grid');

// 3. ВСТАВЛЯЕМ ДАННЫЕ В ШАБЛОН
apiData.forEach(project => {
    const html = `
        <div class="glass-card">
            <h3>${project.title}</h3>
            <p>Raised: $${project.raised}</p>
            <div class="bar" style="width: ${(project.raised / project.goal) * 100}%"></div>
        </div>
    `;
    container.innerHTML += html; 
});
document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/projects') // Вызываем наш новый API
        .then(response => response.json())
        .then(data => {
            const grid = document.querySelector('.projects-grid');
            grid.innerHTML = ''; // Очищаем заглушки

            data.forEach(project => {
                const percent = Math.round((project.raised / project.goal) * 100);
                
                // Создаем HTML карточки на лету
                const card = `
                    <div class="glass-card project-card animate-fade-in">
                        <div class="card-tag">${project.category}</div>
                        <div class="project-info">
                            <h3>${project.title}</h3>
                            <p>${project.desc}</p>
                            <div class="progress-container">
                                <div class="progress-line" style="width: ${percent}%"></div>
                            </div>
                            <div class="funding-details">
                                <span>Raised: $${project.raised.toLocaleString()}</span>
                                <span>${percent}%</span>
                            </div>
                            <span class="goal">Goal: $${project.goal.toLocaleString()}</span>
                        </div>
                        <button class="btn-main invest-btn">INVEST</button>
                    </div>
                `;
                grid.innerHTML += card;
            });
        })
        .catch(err => console.error("Ошибка загрузки API:", err));
});
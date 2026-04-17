from flask import Flask, render_template, url_for, session, request, redirect, jsonify

app = Flask(__name__)
app.secret_key = 'any_secret_string_123'

# В начале файла создаем список для хранения проектов стартапера
user_projects = []

@app.route('/submit-upload', methods=['POST'])
def submit_upload():
    try:
        title = request.form.get('project_title')
        summary = request.form.get('summary')
        goal = request.form.get('funding_goal')
        stage = request.form.get('stage')
        
        # Добавляем данные в список
        user_projects.append({
            "name": title,
            "description": summary,
            "goal": goal,
            "stage": stage
        })
        
        # Переходим на страницу портфолио
        return redirect(url_for('founder_portfolio')) 
    except Exception as e:
        print(f"Error: {e}")
        return "Something went wrong", 500

@app.route('/founder/portfolio')
def founder_portfolio():
    # Отдаем страницу портфолио и список проектов
    return render_template('founder_portfolio.html', projects=user_projects)

@app.route('/api/support', methods=['POST'])
def support_api():
    data = request.json
    subject_key = data.get('subject')  # Получаем категорию вопроса
    
    # Английские ответы на конкретные категории
    responses = {
        "investment": "To start investing, visit the Marketplace, select a project, and click the 'Invest' button.",
        "bug_report": "Thank you for reporting! Our tech team will investigate this issue within 24 hours.",
        "partnership": "We are always open to new missions! Please leave your email, and our manager will contact you.",
        "account": "If you have issues with your account, please try to reset your password in the Settings."
    }
    
    # Если тема не найдена, даем стандартный ответ
    reply = responses.get(subject_key, "Thank you for your message. We will get back to you soon!")
    
    return jsonify({"reply": reply})

@app.route('/api/search_projects')
def search_api():
    # 1. Получаем запрос и очищаем его от лишних пробелов
    query = request.args.get('q', '').strip().lower()
    
    # 2. Твои данные
    mock_data = [
        {
            "id": 1, 
            "name": "EcoEnergy Startup", 
            "category": "GreenTech",
            "description": "Innovative solar panels for urban environments.",
            "founder": "Leyla Alieva",
            "stage": "MVP Phase"
        },
        {
            "id": 2, 
            "name": "AI Medical", 
            "category": "Health",
            "description": "Diagnostic AI that detects anomalies in X-rays.",
            "founder": "Alex Smith",
            "stage": "Seed Round"
        },
        {
            "id": 3, 
            "name": "S&U Academy", 
            "category": "Education",
            "description": "Platform for young entrepreneurs to build startups.",
            "founder": "S&U Team",
            "stage": "Active"
        }
    ]
    
    # 3. Если запрос пустой, возвращаем пустой список, чтобы не грузить систему
    if not query:
        return jsonify([])

    # 4. Фильтруем (ищем вхождение строки в названии ИЛИ категории)
    results = [
        p for p in mock_data 
        if query in p['name'].lower() or query in p['category'].lower()
    ]
    
    # 5. Возвращаем результат
    return jsonify(results)

@app.route('/investor')
def invest_page():
    return render_template('investor.html')

# --- 1. САМАЯ ПЕРВАЯ СТРАНИЦА (ЗАСТАВКА) ---
@app.route('/')
def splash():
    return render_template('splash.html')

# --- 2. СТРАНИЦА ВЫБОРА ЯЗЫКА ---
@app.route('/welcome')
def welcome():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        # Берем имя из поля <input name="username">
        username = request.form.get('username')
        if username:
            session['user_name'] = username # Сохраняем в память
            return redirect(url_for('role_page'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['user_name'] = username
            return redirect(url_for('role_page'))
    return render_template('login.html')

@app.route('/role')
def role_page():
    return render_template('role.html')

# --- ИНВЕСТОР ---
@app.route('/dashboard/investor')
def dashboard_investor():
    return render_template('investor.html')

@app.route('/invest-page')
def marketplace():  # Я изменил имя функции с 'invest_page' на 'marketplace'
    return render_template('invest.page.html')

@app.route('/dashboard/investor/portfolio')
def investor_portfolio():
    return render_template('portfolio.html')

# --- ОБУЧЕНИЕ (8 УРОКОВ) ---
@app.route('/curriculum')
def curriculum():
    return render_template('curriculum.html')

@app.route('/curriculum/lesson1')
def lesson1(): return render_template('lesson1.html')

@app.route('/curriculum/lesson2')
def lesson2(): return render_template('lesson2.html')

@app.route('/curriculum/lesson3')
def lesson3(): return render_template('lesson3.html')

@app.route('/curriculum/lesson4')
def lesson4(): return render_template('lesson4.html')

@app.route('/curriculum/lesson5')
def lesson5(): return render_template('lesson5.html')

@app.route('/curriculum/lesson6')
def lesson6(): return render_template('lesson6.html')

@app.route('/curriculum/lesson7')
def lesson7(): return render_template('lesson7.html')

@app.route('/curriculum/lesson8')
def lesson8(): return render_template('lesson8.html')
   
@app.route('/certificate')
def certificate():
    return render_template('certificate.html')

# --- СТАРТАП ---
@app.route('/dashboard/startup')
def dashboard_startup():
    return render_template('startup.html')

@app.route('/dashboard/nextstartup')
def dashboard_nextstartup():
    return render_template('nextstartup.html')

@app.route('/create-project')
def create_project():
    return render_template('create-project.html')

# 1. Эта функция просто открывает страницу загрузки
@app.route('/upload-project')
def upload_project(): # <--- Удали слово _page
    return render_template('upload.html')

# 2. А эта функция принимает данные от кнопки "UPLOAD AND CONTINUE"

# Настройки (Settings)
@app.route('/settings')
def settings():
    return render_template('settings.html')

# Уведомления (Notifications)
@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

# Поддержка (Support/Help)
@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/logout')
def logout():
    session.pop('user_name', None)
    return redirect(url_for('index'))


     
     
# --- ЗАПУСК ---
if __name__ == '__main__':
    app.run(debug=True)
    
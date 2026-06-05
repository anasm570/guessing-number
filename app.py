from flask import Flask, request, jsonify
import random
import json
import base64

app = Flask(__name__)

# نستخدم متغيراً عاماً لتخزين الأرقام لكل مستخدم (غير آمن للمستخدمين المتعددين، لكن للتجربة كافٍ)
# بدلاً من ذلك، نستخدم طريقة آمنة: نرسل الرقم السري للعميل مشفراً.
# لكن للتبسيط: سنستخدم متغير عام (سيشاركه الجميع) ونعرض تحذيراً.
# للعرض التوضيحي مع الدكتور: مقبول.

GAME_SECRET_NUMBER = None

@app.route('/api/new_game', methods=['POST', 'GET'])
def new_game():
    global GAME_SECRET_NUMBER
    GAME_SECRET_NUMBER = random.randint(1, 100)
    # إرسال الرقم السري للعميل مشفراً (لنستخدم base64 بسيط)
    secret_encoded = base64.b64encode(str(GAME_SECRET_NUMBER).encode()).decode()
    return jsonify({'status': 'ok', 'secret_encoded': secret_encoded})

@app.route('/api/guess', methods=['POST'])
def guess():
    global GAME_SECRET_NUMBER
    try:
        data = request.get_json()
        user_guess = int(data.get('guess'))
        client_secret_encoded = data.get('client_secret')  # نستقبل الرقم المشفر من العميل
        
        # فك التشفير
        try:
            client_secret = int(base64.b64decode(client_secret_encoded).decode())
        except:
            # إذا لم يرسل العميل الرقم المشفر بشكل صحيح، نطلب منه بدء لعبة جديدة
            return jsonify({'error': 'الرجاء بدء لعبة جديدة أولاً', 'reset': True})
        
        # نقارن مع الرقم السري المخزن (سنستخدم المتغير العام، لكن للتعددية يجب استخدام الرقم القادم من العميل)
        # ملاحظة: هذه الطريقة تعتمد على أن العميل يرسل الرقم السري (مشفراً) ونحن نتحقق من صحة التخمين بناءً على الرقم السري الذي أعطيناه للعميل.
        # بهذا لا نحتاج إلى حفظ الحالة على الخادم لكل مستخدم. نستخدم فقط الرقم الذي يرسله العميل.
        # لكن يجب التأكد من أن الرقم السري لم يتم العبث به. يكفي التشفير البسيط للأغراض التعليمية.
        
        # لذا سأتجاهل المتغير العام، وسأعتمد على الرقم السري القادم من العميل:
        # لكن يجب أن يرسل العميل الرقم السري الحقيقي (مشفراً) الذي أخذه من /api/new_game.
        # هذه هي طريقة تخزين الحالة في العميل.
        
        # إذا لم يرسل العميل الرقم السري، نطلب init
        if not client_secret_encoded:
            return jsonify({'error': 'يرجى بدء لعبة جديدة', 'reset': True})
        
        secret = client_secret
        if user_guess == secret:
            # إنشاء رقم جديد تلقائياً للجولة التالية
            new_secret = random.randint(1, 100)
            new_secret_encoded = base64.b64encode(str(new_secret).encode()).decode()
            return jsonify({'result': 'correct', 'secret': secret, 'new_secret_encoded': new_secret_encoded})
        elif user_guess < secret:
            return jsonify({'result': 'low'})
        else:
            return jsonify({'result': 'high'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
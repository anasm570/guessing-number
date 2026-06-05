from flask import Flask, request, jsonify, session
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-for-vercel')

@app.route('/api/guess', methods=['POST'])
def guess():
    try:
        data = request.get_json()
        user_guess = int(data.get('guess'))
        
        if 'secret_number' not in session:
            session['secret_number'] = random.randint(1, 100)
        
        secret = session['secret_number']
        
        if user_guess == secret:
            session.pop('secret_number', None)
            return jsonify({'result': 'correct', 'secret': secret})
        elif user_guess < secret:
            return jsonify({'result': 'low'})
        else:
            return jsonify({'result': 'high'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/new_game', methods=['POST'])
def new_game():
    session['secret_number'] = random.randint(1, 100)
    return jsonify({'status': 'ok'})

# هذا السطر لن يُستخدم في Vercel لكنه مفيد للتجربة المحلية
if __name__ == '__main__':
    app.run(debug=True, port=5000)
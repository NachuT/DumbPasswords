from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__)
CORS(app)

# Had to use AI for connecting this supabase to the server
supabase_url = "https://wtezifwutiqkmylofqzd.supabase.co" 
supabase_key = os.getenv('DB_PASSWORD')

if not supabase_url or not supabase_key:
    raise ValueError("Missing Supabase credentials in environment variables")

print(f"Connecting to Supabase at: {supabase_url}")  

supabase: Client = create_client(supabase_url, supabase_key)

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        print("Received data:", data) 
        
        username = data.get('username')
        email = data.get('email')
        gesture = data.get('gesture')
        
        if not username or not email or not gesture:
            return jsonify({'error': 'Username, email, and gesture are required'}), 400
        
        try:
         
            user_response = supabase.table('users').insert({
                'username': username,
                'email': email,
                'gesturespass': gesture
            }).execute()
            
            print("User response:", user_response)  
            
            if user_response.data:
                return jsonify({'success': True, 'userId': user_response.data[0]['id']})
            return jsonify({'error': 'Failed to create user'}), 500
            
        except Exception as e:
            error_message = str(e)
            if 'duplicate key value violates unique constraint "users_username_key"' in error_message:
                return jsonify({'error': 'Username already exists. Please choose a different username.'}), 400
            elif 'duplicate key value violates unique constraint "users_email_key"' in error_message:
                return jsonify({'error': 'Email already exists. Please use a different email.'}), 400
            print(f"Database error: {error_message}")  
            raise  
            
    except Exception as e:
        print(f"Registration error: {str(e)}")
        print(f"Error type: {type(e)}")
        print(f"Error args: {e.args}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')
    gesture = data.get('gesture')
    
    if not username or not gesture:
        return jsonify({'error': 'Username and gesture are required'}), 400
    
    try:
 
        user_response = supabase.table('users').select('*').eq('username', username).execute()
        
        if user_response.data:  
            user_data = user_response.data[0]
            stored_gesture = user_data.get('gesturespass')
            
            if gesture == stored_gesture:
                return jsonify({'success': True, 'userId': user_data['id']})
            else:
                return jsonify({'error': 'Invalid gesture password'}), 401
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/save-app-password', methods=['POST'])
def save_app_password():
    data = request.get_json()
    user_id = data.get('userId')
    app_name = data.get('appName')
    username = data.get('username')
    password = data.get('password')
    
    if not user_id or not app_name or not password:
        return jsonify({'error': 'User ID, app name, and password are required'}), 400
    
    try:
        response = supabase.table('app_passwords').insert({
            'user_id': user_id,
            'app_name': app_name,
            'username': username,
            'password': password
        }).execute()
        
        if response.data:
            return jsonify({'success': True})
        return jsonify({'error': 'Failed to save app password'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/app-passwords/<int:user_id>', methods=['GET'])
def get_app_passwords(user_id):
    try:
        response = supabase.table('app_passwords').select('app_name, username, password').eq('user_id', user_id).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500





if __name__ == '__main__':
    app.run(debug=True, port=3000) 
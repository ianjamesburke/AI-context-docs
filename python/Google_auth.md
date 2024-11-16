    {% comment %} <button onclick="signInWithGoogle()" class="google-button">
        <img src="https://www.google.com/favicon.ico" alt="Google logo">
        Sign in with Google
    </button>

    <div class="divider">or</div> {% endcomment %}




@app.route('/auth/google', methods=['POST'])
def google_login():
    redirect_url = handle_google_login()
    if redirect_url:
        return jsonify({'url': redirect_url})
    return jsonify({'error': 'Failed to initialize Google login'}), 500

@app.route('/auth/callback')
def auth_callback():
    try:
        code = request.args.get('code')
        print(f"Received code in callback: {code}")
        
        if not code:
            raise ValueError("No code received from OAuth provider")
        
        if 'code_verifier' not in session:
            raise ValueError("No code verifier found in session")
            
        success, message = handle_oauth_callback()
        if success:
            return redirect(url_for('home'))
        flash(message, 'error')
        return redirect(url_for('login'))
    except Exception as e:
        print(f"Callback route error: {str(e)}")
        flash("Authentication failed. Please try again.", 'error')
        return redirect(url_for('login'))



def handle_google_login():
    """Handle Google OAuth login/signup"""
    try:
        redirect_url = request.host_url.rstrip('/') + url_for('auth_callback')
        print(f"Redirect URL: {redirect_url}")  # Debug log
        
        response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": redirect_url,
                "scopes": "email profile",
                "query_params": {
                    "access_type": "offline",
                    "prompt": "consent"
                }
            }
        })
        print(f"Supabase OAuth response: {response}")  # Debug log
        return response.url
    except Exception as e:
        print(f"Google login error: {str(e)}")  # Debug log
        return None

def handle_oauth_callback():
    """Handle OAuth callback and create session"""
    try:
        # Get the code from the request
        code = request.args.get('code')
        print(f"Received code: {code}")  # Debug log
        
        # Get the session data from Supabase
        session_data = supabase.auth.get_session()
        print(f"Session data: {session_data}")  # Debug log
        
        if not session_data or not session_data.user:
            print("No session data or user found")  # Debug log
            return False, "Failed to get user data"

        # Set session data
        session['user'] = {
            'id': session_data.user.id,
            'email': session_data.user.email,
            'access_token': session_data.session.access_token,
            'provider': 'google'
        }
        print(f"Set session user: {session['user']}")  # Debug log

        # Check if this is first login (sign up)
        is_new_user = session_data.user.app_metadata.get('provider') == 'google' and \
                      session_data.user.created_at == session_data.user.last_sign_in_at

        if is_new_user:
            return True, "Account created and logged in successfully"
        return True, "Login successful"
    except Exception as e:
        print(f"OAuth callback error: {str(e)}")  # Debug logging
        return False, str(e)

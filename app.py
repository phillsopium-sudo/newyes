import os
import logging
from flask import Flask, render_template, request, jsonify
from obfuscator import LuaObfuscator
from lua_parser import LuaParser

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Initialize obfuscator and parser
obfuscator = LuaObfuscator()
lua_parser = LuaParser()

@app.route('/')
def index():
    """Main page with obfuscation interface"""
    return render_template('index.html')

@app.route('/api/docs')
def api_docs():
    """API documentation page"""
    return render_template('api_docs.html')

@app.route('/api/obfuscate', methods=['POST'])
def obfuscate_code():
    """
    Obfuscate Lua code via API
    
    Expected JSON payload:
    {
        "code": "lua code string",
        "level": "basic|medium|advanced",
        "options": {
            "rename_variables": true,
            "encode_strings": true,
            "remove_comments": true,
            "minify": true,
            "obfuscate_control_flow": false,
            "obfuscate_metatables": false
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No JSON data provided',
                'success': False
            }), 400
        
        lua_code = data.get('code', '')
        if not lua_code.strip():
            return jsonify({
                'error': 'No Lua code provided',
                'success': False
            }), 400
        
        # Validate Lua syntax
        is_valid, error_msg = lua_parser.validate_syntax(lua_code)
        if not is_valid:
            return jsonify({
                'error': f'Invalid Lua syntax: {error_msg}',
                'success': False
            }), 400
        
        # Get obfuscation options
        level = data.get('level', 'basic')
        options = data.get('options', {})
        
        # Apply obfuscation based on level
        if level == 'basic':
            obfuscated_code = obfuscator.basic_obfuscation(lua_code, options)
        elif level == 'medium':
            obfuscated_code = obfuscator.medium_obfuscation(lua_code, options)
        elif level == 'advanced':
            obfuscated_code = obfuscator.advanced_obfuscation(lua_code, options)
        elif level == 'extreme':
            obfuscated_code = obfuscator.extreme_obfuscation(lua_code, options)
        else:
            return jsonify({
                'error': 'Invalid obfuscation level. Use: basic, medium, advanced, or extreme',
                'success': False
            }), 400
        
        return jsonify({
            'obfuscated_code': obfuscated_code,
            'original_size': len(lua_code),
            'obfuscated_size': len(obfuscated_code),
            'level': level,
            'success': True
        })
        
    except Exception as e:
        logging.error(f"Obfuscation error: {str(e)}")
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'success': False
        }), 500

@app.route('/api/validate', methods=['POST'])
def validate_lua():
    """
    Validate Lua code syntax
    
    Expected JSON payload:
    {
        "code": "lua code string"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No JSON data provided',
                'success': False
            }), 400
        
        lua_code = data.get('code', '')
        if not lua_code.strip():
            return jsonify({
                'error': 'No Lua code provided',
                'success': False
            }), 400
        
        is_valid, error_msg = lua_parser.validate_syntax(lua_code)
        
        return jsonify({
            'valid': is_valid,
            'error_message': error_msg if not is_valid else None,
            'success': True
        })
        
    except Exception as e:
        logging.error(f"Validation error: {str(e)}")
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'success': False
        }), 500

@app.route('/api/techniques', methods=['GET'])
def get_techniques():
    """Get available obfuscation techniques and levels"""
    return jsonify({
        'levels': ['basic', 'medium', 'advanced', 'extreme'],
        'techniques': {
            'rename_variables': 'Rename variables to random strings',
            'encode_strings': 'Encode string literals',
            'remove_comments': 'Remove all comments',
            'minify': 'Remove unnecessary whitespace',
            'obfuscate_control_flow': 'Add dummy control flow statements',
            'obfuscate_metatables': 'Wrap code with metamethods and proxy tables',
            'obfuscate_function_calls': 'Use indirect function invocation',
            'add_fake_functions': 'Insert fake/dummy functions',
            'obfuscate_numbers': 'Replace numbers with mathematical expressions'
        },
        'level_descriptions': {
            'basic': 'Variable renaming and comment removal',
            'medium': 'Basic + string encoding and minification',
            'advanced': 'Medium + control flow and metatable obfuscation',
            'extreme': 'Advanced + function call obfuscation, fake functions, and number obfuscation'
        },
        'version': obfuscator.VERSION,
        'success': True
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

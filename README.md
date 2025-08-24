# Lua Obfuscator v2.0 - Advanced Code Protection Suite

A professional-grade Lua code obfuscation API with multiple protection layers and advanced techniques.

## Features

### 🔒 Obfuscation Levels
- **Basic**: Variable renaming and comment removal
- **Medium**: Basic + string encoding and minification  
- **Advanced**: Medium + control flow and metatable obfuscation
- **Extreme**: Advanced + function call obfuscation, fake functions, and number obfuscation

### 🛡️ Protection Techniques
- **Variable Renaming**: Replace user variables with random names
- **String Encoding**: Base64 encode string literals with custom decoder
- **Comment Removal**: Strip all comments and unnecessary whitespace
- **Code Minification**: Reduce code size by removing formatting
- **Control Flow Obfuscation**: Add dummy conditional blocks
- **Metatable Obfuscation**: Wrap code with metamethods and proxy tables
- **Function Call Indirection**: Use indirect function invocation
- **Fake Function Injection**: Add dummy functions to confuse analysis
- **Number Obfuscation**: Replace numbers with mathematical expressions

## API Endpoints

### POST /api/obfuscate
Obfuscate Lua code with specified level and options.

```json
{
  "code": "local x = 5\nprint(x)",
  "level": "extreme",
  "options": {
    "rename_variables": true,
    "encode_strings": true,
    "remove_comments": true,
    "minify": true,
    "obfuscate_control_flow": true,
    "obfuscate_metatables": true,
    "obfuscate_function_calls": true,
    "add_fake_functions": true,
    "obfuscate_numbers": true
  }
}
```

### POST /api/validate
Validate Lua syntax before obfuscation.

### GET /api/techniques
Get available techniques and level descriptions.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   python main.py
   ```

3. **Access the web interface:**
   Open `http://localhost:5000` in your browser

4. **Use the API:**
   ```bash
   curl -X POST http://localhost:5000/api/obfuscate \
     -H "Content-Type: application/json" \
     -d '{"code": "print(\"Hello World\")", "level": "extreme"}'
   ```

## Deployment

This project is ready for deployment on various platforms:
- **Pella.app**: Python-optimized hosting starting at $3/year
- **PythonAnywhere**: Free tier available, Flask-ready
- **Railway**: $5/month with automatic GitHub deployment
- **Heroku**: Git-based deployment with buildpacks

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5 with dark theme
- **Deployment**: Gunicorn WSGI server
- **Dependencies**: Pure Python (no external obfuscation libraries)

## Security Notice

This tool is designed for educational purposes and legitimate code protection. Always ensure you have the right to obfuscate any code you process.

## Version History

### v2.0.0
- Added extreme obfuscation level
- Implemented metatable obfuscation 
- Added function call indirection
- Introduced fake function injection
- Added number obfuscation techniques
- Enhanced web interface design
- Improved API documentation

### v1.0.0
- Initial release with basic, medium, and advanced levels
- Core obfuscation techniques
- Web interface and REST API
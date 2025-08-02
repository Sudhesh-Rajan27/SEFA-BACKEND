"""
Unified API Backend for Python, C++ and JavaScript Code Execution
Provides REST API endpoints for code compilation and execution using Judge0 API
Platform-compatible deployment for Railway, Heroku, Vercel, etc.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.compilers.judge0_compiler import Judge0Compiler, format_judge0_output
import json
import logging
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Enable CORS for frontend integration (all origins for development, specific for production)
CORS(app, origins=[
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # React dev server
    "http://localhost:4000",  # Alternative frontend port
    "https://*.railway.app",  # Railway production URLs
    "https://*.vercel.app",   # Vercel frontend deployment
    "https://*.netlify.app"   # Netlify frontend deployment
])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global Judge0 compiler instance
judge0_compiler = None

def init_compilers():
    """Initialize Judge0 compiler for platform-compatible code execution"""
    global judge0_compiler
    
    try:
        judge0_compiler = Judge0Compiler()
        if judge0_compiler.is_available():
            supported_langs = judge0_compiler.get_supported_languages()
            logger.info("✅ Judge0 compiler initialized successfully")
            logger.info(f"🏛️ Judge0 supports: {', '.join(supported_langs)}")
            logger.info("🌍 Platform-compatible execution ready!")
            return True
        else:
            logger.error("❌ Judge0 API not accessible - check your API key")
            judge0_compiler = None
            return False
    except Exception as e:
        logger.error(f"❌ Failed to initialize Judge0 compiler: {e}")
        judge0_compiler = None
        return False

def detect_language(code):
    """Detect programming language based on code content"""
    code_lower = code.lower().strip()
    
    # C++ indicators
    cpp_indicators = [
        '#include <iostream>',
        '#include<iostream>',
        'std::cout',
        'std::cin',
        'std::endl',
        'int main()',
        'int main(',
        'using namespace std',
        '#include <vector>',
        '#include <string>',
        'cout <<',
        'cin >>'
    ]
    
    # JavaScript indicators
    js_indicators = [
        'console.log(',
        'console.error(',
        'function(',
        'const ',
        'let ',
        'var ',
        '=>',
        'document.',
        'window.',
        'require(',
        'module.exports'
    ]
    
    # Python indicators
    python_indicators = [
        'print(',
        'import ',
        'from ',
        'def ',
        'class ',
        'if __name__',
        'elif',
        'except:',
        'try:',
        '    ',  # Python indentation
    ]
    
    # Score each language
    cpp_score = sum(1 for indicator in cpp_indicators if indicator in code_lower)
    js_score = sum(1 for indicator in js_indicators if indicator in code_lower)
    python_score = sum(1 for indicator in python_indicators if indicator in code_lower)
    
    # Additional scoring logic
    if '#include' in code_lower:
        cpp_score += 3
    if 'console.log' in code_lower or 'function' in code_lower:
        js_score += 2
    if 'print(' in code_lower or 'def ' in code_lower:
        python_score += 2
    
    # Handle edge cases
    for line in code.split('\n'):
        line = line.strip()
        if line.startswith('//'):
            cpp_score += 1
            js_score += 1
        elif line.startswith('#') and not line.startswith('#include'):
            python_score += 1
        elif line.endswith(';') and '{' in code:
            if 'main(' in code_lower:
                cpp_score += 2
            else:
                js_score += 1
        if ':' in code and not ';' in code:
            python_score += 1
    
    # Return the language with highest score
    scores = {'cpp': cpp_score, 'js': js_score, 'python': python_score}
    return max(scores, key=scores.get)

# API Routes
@app.route('/api/compile', methods=['POST'])
def api_compile_code():
    """API endpoint to compile and run code using Judge0 API"""
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({
                'success': False,
                'error': 'No code provided'
            }), 400
        
        code = data['code']
        syntax_only = data.get('syntax_only', False)
        timeout = data.get('timeout', 30)
        language = data.get('language', None)
        
        # Auto-detect language if not specified
        if not language:
            language = detect_language(code)
        
        logger.info(f"📝 Compiling {language} code using Judge0 API")
        
        # Check if Judge0 is available
        if not judge0_compiler:
            return jsonify({
                'success': False,
                'error': 'Judge0 compiler not available. Check API configuration.'
            }), 500
        
        # Normalize language for Judge0
        if language in ['js', 'javascript']:
            language = 'javascript'
        elif language in ['cpp', 'c++']:
            language = 'cpp'
        
        # Check if Judge0 supports this language
        supported_languages = judge0_compiler.get_supported_languages()
        if language not in supported_languages:
            return jsonify({
                'success': False,
                'error': f'Language "{language}" not supported. Supported: {", ".join(supported_languages)}'
            }), 400
        
        logger.info(f"🏛️ Executing {language} code via Judge0 API")
        
        # Execute code
        if syntax_only:
            result = judge0_compiler.check_syntax(code, language)
        else:
            result = judge0_compiler.compile_and_run(code, language, timeout)
        
        # Format and return response
        response = format_judge0_output(result, language)
        
        if result.success:
            logger.info(f"✅ Execution successful - {language}")
        else:
            logger.warning(f"⚠️ Execution failed - {language}")
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"❌ Error in compile endpoint: {e}")
        return jsonify({
            'success': False,
            'output': [],
            'errors': [str(e)],
            'exit_code': -1,
            'execution_time': 0.0,
            'language': 'unknown',
            'formatted_output': f"Error: {str(e)}",
            'compiler': 'Judge0 API'
        }), 500

# Legacy endpoint for backward compatibility
@app.route('/compile', methods=['POST'])
def compile_code():
    """Legacy endpoint - redirects to API"""
    return api_compile_code()

@app.route('/api/health')
def api_health_check():
    """Health check endpoint for the API"""
    global judge0_compiler
    
    judge0_status = "available" if judge0_compiler and judge0_compiler.is_available() else "not available"
    
    return jsonify({
        'status': 'healthy',
        'execution_mode': 'judge0',
        'message': 'EduRun AI Code Buddy API is running',
        'compiler': {
            'type': 'Judge0 API',
            'status': judge0_status,
            'platform_compatible': True,
            'languages': judge0_compiler.get_supported_languages() if judge0_compiler else []
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return api_health_check()

@app.route('/api/languages')
def api_supported_languages():
    """Get list of supported languages"""
    global judge0_compiler
    
    if not judge0_compiler:
        return jsonify({
            'error': 'Judge0 compiler not available',
            'languages': [],
            'total': 0
        }), 500
    
    supported_langs = judge0_compiler.get_supported_languages()
    
    languages = [
        {
            'id': 'python',
            'name': 'Python',
            'description': 'Python 3.8.1 (Judge0 API execution)',
            'example': 'print("Hello, Python!")',
            'status': 'available' if 'python' in supported_langs else 'not supported'
        },
        {
            'id': 'cpp',
            'name': 'C++',
            'description': 'C++ (GCC 9.2.0) (Judge0 API execution)',
            'example': '#include <iostream>\nint main() {\n    std::cout << "Hello, C++!" << std::endl;\n    return 0;\n}',
            'status': 'available' if 'cpp' in supported_langs else 'not supported'
        },
        {
            'id': 'javascript',
            'name': 'JavaScript',
            'description': 'JavaScript (Node.js 12.14.0) (Judge0 API execution)',
            'example': 'console.log("Hello, JavaScript!");',
            'status': 'available' if 'javascript' in supported_langs else 'not supported'
        }
    ]
    
    return jsonify({
        'languages': languages,
        'total': len(languages),
        'all_supported': supported_langs,
        'compiler': 'Judge0 API'
    })

if __name__ == '__main__':
    # Production configuration for Railway/Heroku/Render
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    # Initialize Judge0 compiler on startup
    logger.info("🚀 Starting Judge0-Powered Code Execution Backend...")
    
    if init_compilers():
        logger.info("✅ Judge0 compiler initialized successfully")
        if judge0_compiler:
            supported = judge0_compiler.get_supported_languages()
            logger.info(f"📋 Supported languages: {', '.join(supported[:5])}...")
        logger.info(f"🌐 Server starting on port {port}")
        logger.info("🔧 API Base URL: /api")
        logger.info("📖 Available endpoints:")
        logger.info("   POST /api/compile - Compile and run code via Judge0")
        logger.info("   GET  /api/health  - Health check")
        logger.info("   GET  /api/languages - Supported languages")
        logger.info("🏛️ Powered by Judge0 API - Platform Compatible!")
        app.run(debug=debug, host='0.0.0.0', port=port)
    else:
        logger.error("❌ Judge0 compiler initialization failed")
        logger.error("🔑 Check your Judge0 API key and internet connection")
        logger.info("🔄 Starting server anyway for debugging...")
        app.run(debug=debug, host='0.0.0.0', port=port)

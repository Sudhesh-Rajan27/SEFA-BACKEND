"""
Judge0 Code Compiler Module using RapidAPI
This module provides functionality to compile and run code using Judge0 API
for platform-compatible deployment (Railway, Heroku, Vercel, etc.)
"""

import requests
import time
import json
import logging
from typing import NamedTuple, Optional
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompilerResult(NamedTuple):
    """Data class to hold compilation results"""
    success: bool
    output: str
    error: str
    exit_code: int
    execution_time: float

class Judge0Compiler:
    """
    A class to compile and run code using Judge0 API via RapidAPI
    Works on any platform - no Docker required!
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Judge0 compiler with RapidAPI credentials
        
        Args:
            api_key: RapidAPI key for Judge0 CE (from environment or parameter)
        """
        self.api_key = api_key or "f38545accbmshb4e9fc5c29c4434p176d69jsnaccce6804686"
        self.base_url = "https://judge0-ce.p.rapidapi.com"
        
        # Judge0 Language ID mapping
        self.language_map = {
            'python': 71,      # Python 3.8.1
            'javascript': 63,  # JavaScript (Node.js 12.14.0)  
            'js': 63,          # JavaScript alias
            'cpp': 54,         # C++ (GCC 9.2.0)
            'c++': 54,         # C++ alias
            'c': 50,           # C (GCC 9.2.0)
            'java': 62,        # Java (OpenJDK 13.0.1)
            'csharp': 51,      # C# (Mono 6.6.0.161)
            'go': 60,          # Go (1.13.5)
            'rust': 73,        # Rust (1.40.0)
            'php': 68,         # PHP (7.4.1)
            'ruby': 72,        # Ruby (2.7.0)
        }
        
        # RapidAPI headers
        self.headers = {
            'Content-Type': 'application/json',
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': 'judge0-ce.p.rapidapi.com'
        }
        
        logger.info("🏛️ Judge0 RapidAPI compiler initialized")
        
        # Test API connectivity
        try:
            self._test_connection()
        except Exception as e:
            logger.warning(f"⚠️ Judge0 API test failed: {e}")
    
    def _test_connection(self):
        """Test connection to Judge0 API"""
        try:
            response = requests.get(
                f"{self.base_url}/about",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                about_info = response.json()
                logger.info(f"✅ Judge0 API connected - Version: {about_info.get('version', 'Unknown')}")
                return True
            else:
                logger.error(f"❌ Judge0 API connection failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Judge0 API connection error: {e}")
            return False
    
    def compile_and_run(self, code: str, language: str = 'python', timeout: int = 30) -> CompilerResult:
        """
        Compile and execute code using Judge0 API
        
        Args:
            code: Source code to execute
            language: Programming language ('python', 'javascript', 'cpp', etc.)
            timeout: Execution timeout in seconds
            
        Returns:
            CompilerResult with execution details
        """
        start_time = time.time()
        
        try:
            # Normalize language name
            language = language.lower().strip()
            
            # Get Judge0 language ID
            language_id = self.language_map.get(language)
            if not language_id:
                supported = ', '.join(self.language_map.keys())
                return CompilerResult(
                    False, "", 
                    f"Unsupported language: {language}. Supported: {supported}", 
                    1, 0.0
                )
            
            logger.info(f"📤 Submitting {language} code to Judge0 API...")
            
            # Prepare submission data
            submission_data = {
                "source_code": code,
                "language_id": language_id,
                "stdin": "",
                "cpu_time_limit": min(timeout, 15),  # Judge0 free tier limit
                "memory_limit": 128000,  # 128MB
                "wall_time_limit": min(timeout + 5, 20)
            }
            
            # Submit code for execution
            response = requests.post(
                f"{self.base_url}/submissions",
                headers=self.headers,
                json=submission_data,
                timeout=30
            )
            
            if response.status_code != 201:
                error_msg = f"Submission failed: HTTP {response.status_code} - {response.text}"
                logger.error(f"❌ {error_msg}")
                return CompilerResult(
                    False, "", error_msg, 1, time.time() - start_time
                )
            
            submission = response.json()
            token = submission['token']
            logger.info(f"✅ Code submitted successfully - Token: {token}")
            
            # Poll for execution results
            max_polls = 30  # 30 seconds max wait
            poll_interval = 1  # 1 second intervals
            
            for poll_count in range(max_polls):
                time.sleep(poll_interval)
                
                # Get submission status
                result_response = requests.get(
                    f"{self.base_url}/submissions/{token}",
                    headers=self.headers,
                    timeout=10
                )
                
                if result_response.status_code != 200:
                    logger.warning(f"⚠️ Status check failed: {result_response.status_code}")
                    continue
                
                result = result_response.json()
                status_id = result.get('status', {}).get('id')
                status_description = result.get('status', {}).get('description', 'Unknown')
                
                logger.info(f"📊 Poll {poll_count + 1}: Status {status_id} - {status_description}")
                
                # Judge0 Status IDs:
                # 1 = In Queue, 2 = Processing
                # 3 = Accepted (Success)
                # 4 = Wrong Answer, 5 = Time Limit Exceeded
                # 6 = Compilation Error, 11 = Runtime Error, etc.
                
                if status_id in [1, 2]:  # Still processing
                    continue
                
                # Execution completed - extract results
                execution_time = time.time() - start_time
                
                stdout = result.get('stdout') or ""
                stderr = result.get('stderr') or ""
                compile_output = result.get('compile_output') or ""
                exit_code = result.get('exit_code') or 0
                
                # Build error message
                error_parts = []
                if compile_output.strip():
                    error_parts.append(f"Compilation Error:\n{compile_output.strip()}")
                if stderr.strip():
                    error_parts.append(f"Runtime Error:\n{stderr.strip()}")
                
                error_output = "\n\n".join(error_parts)
                
                # Determine success
                success = (status_id == 3)  # Status 3 = Accepted
                
                if success:
                    logger.info(f"🎉 Execution successful - Output: {stdout[:50]}...")
                else:
                    logger.warning(f"⚠️ Execution failed - Status: {status_description}")
                
                return CompilerResult(
                    success=success,
                    output=stdout,
                    error=error_output,
                    exit_code=exit_code,
                    execution_time=execution_time
                )
            
            # Polling timeout
            logger.error("⏰ Polling timeout - execution results not ready")
            return CompilerResult(
                False, "", 
                "Execution timeout - results not available within 30 seconds", 
                124, time.time() - start_time
            )
            
        except requests.RequestException as e:
            logger.error(f"❌ Judge0 API request failed: {e}")
            return CompilerResult(
                False, "", f"API request failed: {str(e)}", 1, 
                time.time() - start_time
            )
        except Exception as e:
            logger.error(f"❌ Unexpected error in Judge0 execution: {e}")
            return CompilerResult(
                False, "", f"Execution error: {str(e)}", 1, 
                time.time() - start_time
            )
    
    def check_syntax(self, code: str, language: str = 'python') -> CompilerResult:
        """
        Check code syntax without full execution
        """
        logger.info(f"🔍 Checking {language} syntax...")
        
        if language.lower() == 'python':
            # Python syntax check using ast.parse
            syntax_check_code = f'''
import ast
import sys

try:
    code = """{code}"""
    ast.parse(code)
    print("✅ Syntax is valid")
except SyntaxError as e:
    print(f"❌ SyntaxError: {{e}}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {{e}}")
    sys.exit(1)
'''
            return self.compile_and_run(syntax_check_code, 'python', 10)
        
        else:
            # For compiled languages, compilation IS syntax checking
            return self.compile_and_run(code, language, 10)
    
    def get_supported_languages(self) -> list:
        """Get list of supported programming languages"""
        return list(self.language_map.keys())
    
    def is_available(self) -> bool:
        """Check if Judge0 API is accessible"""
        try:
            response = requests.get(
                f"{self.base_url}/about",
                headers=self.headers,
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def get_language_info(self) -> dict:
        """Get detailed language information from Judge0"""
        try:
            response = requests.get(
                f"{self.base_url}/languages",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return {}
        except:
            return {}

def format_judge0_output(result: CompilerResult, language: str = 'unknown') -> dict:
    """
    Format Judge0 execution result for consistent API response
    
    Args:
        result: CompilerResult from Judge0 execution
        language: Programming language used
        
    Returns:
        Formatted dictionary for API response
    """
    
    # Split output and errors into lines
    output_lines = result.output.split('\n') if result.output else []
    error_lines = result.error.split('\n') if result.error else []
    
    # Remove empty lines
    output_lines = [line for line in output_lines if line.strip()]
    error_lines = [line for line in error_lines if line.strip()]
    
    # Create status message
    status = "✅ SUCCESS" if result.success else "❌ FAILED"
    
    # Build formatted output for display
    formatted_output = f"""=== JUDGE0 EXECUTION RESULT: {status} ===
Language: {language.upper()}
Exit Code: {result.exit_code}
Execution Time: {result.execution_time:.2f}s

📄 PROGRAM OUTPUT:
{'─' * 50}
{result.output if result.output else '(no output)'}
{'─' * 50}

{f'❌ ERRORS:' if error_lines else ''}
{result.error if result.error else ''}

🏛️ Powered by Judge0 API
═══════════════════════════════════════════════════"""
    
    return {
        'success': result.success,
        'output': output_lines,
        'errors': error_lines,
        'exit_code': result.exit_code,
        'execution_time': result.execution_time,
        'language': language,
        'formatted_output': formatted_output.strip(),
        'compiler': 'Judge0 API',
        'platform_compatible': True
    }

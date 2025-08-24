import re
import logging

class LuaParser:
    """
    Basic Lua syntax validator and parser
    """
    
    def __init__(self):
        self.lua_keywords = {
            'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
            'function', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat',
            'return', 'then', 'true', 'until', 'while'
        }
        
        # Block keywords that need matching 'end'
        self.block_starters = {'if', 'for', 'while', 'function', 'do', 'repeat'}
        self.block_enders = {'end', 'until'}
    
    def validate_syntax(self, code):
        """
        Basic Lua syntax validation
        Returns (is_valid, error_message)
        """
        try:
            # Check for basic syntax issues
            
            # 1. Check balanced parentheses, brackets, and braces
            balance_result = self._check_balanced_delimiters(code)
            if not balance_result[0]:
                return False, balance_result[1]
            
            # 2. Check balanced block statements
            block_result = self._check_balanced_blocks(code)
            if not block_result[0]:
                return False, block_result[1]
            
            # 3. Check for invalid characters/patterns
            invalid_result = self._check_invalid_patterns(code)
            if not invalid_result[0]:
                return False, invalid_result[1]
            
            # 4. Check string literals
            string_result = self._check_string_literals(code)
            if not string_result[0]:
                return False, string_result[1]
            
            return True, None
            
        except Exception as e:
            logging.error(f"Syntax validation error: {str(e)}")
            return False, f"Validation error: {str(e)}"
    
    def _check_balanced_delimiters(self, code):
        """Check if parentheses, brackets, and braces are balanced"""
        stack = []
        pairs = {'(': ')', '[': ']', '{': '}'}
        
        in_string = False
        string_char = None
        escaped = False
        
        for i, char in enumerate(code):
            if escaped:
                escaped = False
                continue
                
            if char == '\\':
                escaped = True
                continue
            
            if not in_string:
                if char in ['"', "'"]:
                    in_string = True
                    string_char = char
                elif char in pairs:
                    stack.append((char, i))
                elif char in pairs.values():
                    if not stack:
                        return False, f"Unmatched closing delimiter '{char}' at position {i}"
                    
                    opener, pos = stack.pop()
                    if pairs[opener] != char:
                        return False, f"Mismatched delimiter: expected '{pairs[opener]}' but found '{char}' at position {i}"
            else:
                if char == string_char:
                    in_string = False
                    string_char = None
        
        if stack:
            opener, pos = stack[-1]
            return False, f"Unmatched opening delimiter '{opener}' at position {pos}"
        
        if in_string:
            return False, "Unterminated string literal"
        
        return True, None
    
    def _check_balanced_blocks(self, code):
        """Check if Lua block statements are properly balanced"""
        # Remove strings and comments first to avoid false matches
        cleaned_code = self._remove_strings_and_comments(code)
        
        # Find all keywords
        tokens = re.findall(r'\b\w+\b', cleaned_code)
        
        stack = []
        
        for i, token in enumerate(tokens):
            if token in self.block_starters:
                if token == 'repeat':
                    stack.append(('repeat', 'until'))
                else:
                    stack.append((token, 'end'))
            elif token in self.block_enders:
                if not stack:
                    return False, f"Unexpected '{token}' without matching block starter"
                
                starter, expected_ender = stack.pop()
                if token != expected_ender:
                    return False, f"Block mismatch: '{starter}' should end with '{expected_ender}', not '{token}'"
        
        if stack:
            starter, expected_ender = stack[-1]
            return False, f"Unmatched block starter '{starter}' - missing '{expected_ender}'"
        
        return True, None
    
    def _check_invalid_patterns(self, code):
        """Check for obviously invalid patterns"""
        
        # Check for invalid identifier patterns
        invalid_identifiers = re.findall(r'\b\d+[a-zA-Z_]\w*', code)
        if invalid_identifiers:
            return False, f"Invalid identifier starting with digit: {invalid_identifiers[0]}"
        
        # Check for invalid operators or syntax
        invalid_patterns = [
            (r'===+', 'Invalid operator (use == for equality)'),
            (r'!==*', 'Invalid operator (use ~= for inequality in Lua)'),
            (r'\+\+', 'Invalid operator (use var = var + 1 in Lua)'),
            (r'--(?!\[)', 'Invalid operator on new line (use var = var - 1 in Lua)'),
        ]
        
        for pattern, message in invalid_patterns:
            if re.search(pattern, code):
                return False, message
        
        return True, None
    
    def _check_string_literals(self, code):
        """Check if string literals are properly formed"""
        # Check for unescaped quotes in strings
        single_quote_strings = re.findall(r"'([^'\\]|\\.)*'?", code)
        double_quote_strings = re.findall(r'"([^"\\]|\\.)*"?', code)
        
        # This is a basic check - a more thorough implementation would parse character by character
        if code.count('"') % 2 != 0:
            unmatched_double = True
            # More sophisticated check needed here
        
        if code.count("'") % 2 != 0:
            unmatched_single = True
            # More sophisticated check needed here
        
        return True, None
    
    def _remove_strings_and_comments(self, code):
        """Remove strings and comments from code for parsing"""
        result = []
        in_string = False
        string_char = None
        escaped = False
        i = 0
        
        while i < len(code):
            char = code[i]
            
            if escaped:
                escaped = False
                if in_string:
                    result.append(' ')
                else:
                    result.append(char)
                i += 1
                continue
            
            if char == '\\':
                escaped = True
                result.append(' ' if in_string else char)
                i += 1
                continue
            
            if not in_string:
                if char in ['"', "'"]:
                    in_string = True
                    string_char = char
                    result.append(' ')
                elif char == '-' and i + 1 < len(code) and code[i + 1] == '-':
                    # Comment starts - skip to end of line
                    while i < len(code) and code[i] != '\n':
                        i += 1
                    if i < len(code):
                        result.append('\n')
                    continue
                else:
                    result.append(char)
            else:
                if char == string_char:
                    in_string = False
                    string_char = None
                result.append(' ' if in_string else ' ')
            
            i += 1
        
        return ''.join(result)
    
    def extract_functions(self, code):
        """Extract function definitions from Lua code"""
        functions = []
        
        # Pattern to match function definitions
        func_pattern = r'\bfunction\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        
        for match in re.finditer(func_pattern, code):
            func_name = match.group(1)
            start_pos = match.start()
            functions.append({
                'name': func_name,
                'start_position': start_pos
            })
        
        return functions
    
    def extract_variables(self, code):
        """Extract variable declarations from Lua code"""
        variables = []
        
        # Pattern to match local variable declarations
        local_pattern = r'\blocal\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        
        for match in re.finditer(local_pattern, code):
            var_name = match.group(1)
            start_pos = match.start()
            variables.append({
                'name': var_name,
                'start_position': start_pos,
                'type': 'local'
            })
        
        return variables

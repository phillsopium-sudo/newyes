import re
import random
import string
import base64
import logging

class LuaObfuscator:
    """
    Lua Code Obfuscator v2.0
    Advanced obfuscation toolkit with multiple protection layers
    """
    
    VERSION = "2.0.0"
    
    def __init__(self):
        self.lua_keywords = {
            'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
            'function', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat',
            'return', 'then', 'true', 'until', 'while'
        }
        
        self.lua_builtins = {
            'print', 'pairs', 'ipairs', 'next', 'type', 'getmetatable',
            'setmetatable', 'rawget', 'rawset', 'tonumber', 'tostring',
            'pcall', 'xpcall', 'error', 'assert', 'select', 'unpack',
            'math', 'string', 'table', 'io', 'os', 'debug', 'coroutine'
        }
    
    def generate_random_name(self, length=8):
        """Generate a random variable name"""
        first_char = random.choice(string.ascii_letters + '_')
        rest_chars = ''.join(random.choices(
            string.ascii_letters + string.digits + '_', 
            k=length-1
        ))
        return first_char + rest_chars
    
    def extract_variables(self, code):
        """Extract user-defined variables from Lua code"""
        variables = set()
        
        # Find local variable declarations
        local_pattern = r'\blocal\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        for match in re.finditer(local_pattern, code):
            var_name = match.group(1)
            if var_name not in self.lua_keywords and var_name not in self.lua_builtins:
                variables.add(var_name)
        
        # Find function declarations
        func_pattern = r'\bfunction\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        for match in re.finditer(func_pattern, code):
            func_name = match.group(1)
            if func_name not in self.lua_keywords and func_name not in self.lua_builtins:
                variables.add(func_name)
        
        # Find assignment patterns (simple heuristic)
        assign_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*='
        for match in re.finditer(assign_pattern, code):
            var_name = match.group(1)
            if var_name not in self.lua_keywords and var_name not in self.lua_builtins:
                variables.add(var_name)
        
        return variables
    
    def rename_variables(self, code):
        """Rename user-defined variables to random names"""
        variables = self.extract_variables(code)
        rename_map = {}
        
        for var in variables:
            new_name = self.generate_random_name()
            # Ensure no collision with existing names
            while new_name in rename_map.values() or new_name in self.lua_keywords:
                new_name = self.generate_random_name()
            rename_map[var] = new_name
        
        # Apply renaming
        result = code
        for old_name, new_name in rename_map.items():
            # Use word boundaries to avoid partial replacements
            pattern = r'\b' + re.escape(old_name) + r'\b'
            result = re.sub(pattern, new_name, result)
        
        logging.debug(f"Renamed variables: {rename_map}")
        return result
    
    def encode_strings(self, code):
        """Encode string literals using base64"""
        def encode_string_match(match):
            quote = match.group(1)
            content = match.group(2)
            
            # Encode the content (without quotes) to base64
            encoded = base64.b64encode(content.encode('utf-8')).decode('ascii')
            
            # Return a Lua expression that decodes the string
            return f'(function() local b64="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"; local function decode(data) local result = ""; local pad = string.len(data) % 4; if pad > 0 then data = data .. string.rep("=", 4 - pad) end; for i = 1, string.len(data), 4 do local a, b, c, d = string.byte(data, i, i + 3); a = string.find(b64, string.char(a)) - 1; b = string.find(b64, string.char(b)) - 1; c = string.find(b64, string.char(c)) - 1; d = string.find(b64, string.char(d)) - 1; result = result .. string.char(bit.bor(bit.lshift(a, 2), bit.rshift(b, 4))); if c ~= 64 then result = result .. string.char(bit.bor(bit.lshift(bit.band(b, 15), 4), bit.rshift(c, 2))) end; if d ~= 64 then result = result .. string.char(bit.bor(bit.lshift(bit.band(c, 3), 6), d)) end end; return result end; return decode("{encoded}") end)()'
        
        # Match both single and double quoted strings
        string_pattern = r'(["\'])([^"\']*?)\1'
        result = re.sub(string_pattern, encode_string_match, code)
        
        return result
    
    def remove_comments(self, code):
        """Remove all comments from Lua code"""
        # Remove single-line comments (but preserve strings)
        lines = code.split('\n')
        result_lines = []
        
        for line in lines:
            # Simple approach: find -- that's not inside a string
            in_string = False
            quote_char = None
            comment_pos = -1
            
            for i, char in enumerate(line):
                if not in_string and char in ['"', "'"]:
                    in_string = True
                    quote_char = char
                elif in_string and char == quote_char:
                    in_string = False
                    quote_char = None
                elif not in_string and char == '-' and i + 1 < len(line) and line[i + 1] == '-':
                    comment_pos = i
                    break
            
            if comment_pos >= 0:
                line = line[:comment_pos].rstrip()
            
            result_lines.append(line)
        
        # Remove multi-line comments --[[ ]]
        result = '\n'.join(result_lines)
        multiline_comment_pattern = r'--\[\[.*?\]\]'
        result = re.sub(multiline_comment_pattern, '', result, flags=re.DOTALL)
        
        return result
    
    def minify_code(self, code):
        """Remove unnecessary whitespace"""
        # Remove leading/trailing whitespace from lines
        lines = [line.strip() for line in code.split('\n')]
        
        # Remove empty lines
        lines = [line for line in lines if line]
        
        # Join with minimal spacing
        result = ' '.join(lines)
        
        # Clean up extra spaces around operators and keywords
        result = re.sub(r'\s+', ' ', result)
        result = re.sub(r'\s*([=+\-*/(){}[\],;])\s*', r'\1', result)
        
        return result
    
    def obfuscate_control_flow(self, code):
        """Add dummy control flow statements to confuse analysis"""
        # Add some dummy conditional blocks
        dummy_conditions = [
            'if true then',
            'if 1 == 1 then', 
            'if math.random() or true then'
        ]
        
        lines = code.split('\n')
        result_lines = []
        
        for i, line in enumerate(lines):
            result_lines.append(line)
            
            # Randomly insert dummy conditions
            if random.random() < 0.1 and line.strip():  # 10% chance
                dummy = random.choice(dummy_conditions)
                result_lines.append(f'  {dummy}')
                # Add some dummy operations
                result_lines.append(f'    local _ = {random.randint(1, 100)}')
                result_lines.append('  end')
        
        return '\n'.join(result_lines)
    
    def obfuscate_with_metatables(self, code):
        """Add metatable obfuscation to make code behavior unpredictable"""
        
        # Generate random metatable names
        meta_var = self.generate_random_name(6)
        proxy_var = self.generate_random_name(6)
        env_var = self.generate_random_name(6)
        
        # Create metatable setup prefix
        metatable_setup = f"""
-- Metatable obfuscation layer
local {meta_var} = {{}}
{meta_var}.__index = function(t, k)
    if type(k) == "string" and string.len(k) > 0 then
        return rawget(t, k) or rawget(_G, k)
    end
    return nil
end
{meta_var}.__newindex = function(t, k, v)
    if type(k) == "string" then
        rawset(t, k, v)
    end
end
{meta_var}.__call = function(t, ...)
    local args = {{...}}
    if #args > 0 and type(args[1]) == "function" then
        return args[1](select(2, ...))
    end
    return t
end
{meta_var}.__tostring = function(t)
    return tostring(rawget(t, "_value") or t)
end

-- Create proxy environment
local {env_var} = setmetatable({{}}, {meta_var})
for k, v in pairs(_G) do
    {env_var}[k] = v
end

-- Proxy table wrapper
local function {proxy_var}(obj)
    if type(obj) == "table" then
        return setmetatable(obj, {meta_var})
    elseif type(obj) == "function" then
        local wrapper = setmetatable({{_value = obj}}, {meta_var})
        wrapper.__call = function(self, ...)
            return self._value(...)
        end
        return wrapper
    else
        return setmetatable({{_value = obj}}, {meta_var})
    end
end

-- Install environment
setfenv(1, {env_var})
"""
        
        # Add metatable wrapping for function calls and variable assignments
        lines = code.split('\n')
        result_lines = [metatable_setup]
        
        for line in lines:
            original_line = line
            
            # Wrap function declarations with metatable
            if re.search(r'\bfunction\s+([a-zA-Z_][a-zA-Z0-9_]*)', line):
                # Keep original function definition
                result_lines.append(original_line)
                # Add metatable wrapper
                func_match = re.search(r'\bfunction\s+([a-zA-Z_][a-zA-Z0-9_]*)', line)
                if func_match:
                    func_name = func_match.group(1)
                    if func_name not in self.lua_keywords and func_name not in self.lua_builtins:
                        result_lines.append(f"{func_name} = {proxy_var}({func_name})")
                continue
            
            # Wrap local variable assignments with random chance
            if re.search(r'\blocal\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=', line) and random.random() < 0.3:
                var_match = re.search(r'\blocal\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)', line)
                if var_match:
                    var_name = var_match.group(1)
                    var_value = var_match.group(2)
                    if var_name not in self.lua_keywords and var_name not in self.lua_builtins:
                        result_lines.append(f"local {var_name} = {proxy_var}({var_value})")
                        continue
            
            # Add dummy metatable operations randomly
            if random.random() < 0.05 and line.strip():
                dummy_ops = [
                    f"local _ = {proxy_var}({{}})",
                    f"local _ = setmetatable({{}}, {meta_var})",
                    f"getmetatable({{}})"
                ]
                result_lines.append(random.choice(dummy_ops))
            
            result_lines.append(original_line)
        
        return '\n'.join(result_lines)
    
    def obfuscate_function_calls(self, code):
        """Obfuscate function calls using indirect invocation"""
        
        # Generate random function invoker
        invoker_var = self.generate_random_name(8)
        
        # Create function call indirection setup
        indirection_setup = f"""
-- Function call obfuscation layer
local {invoker_var} = {{}}
{invoker_var}.invoke = function(fn, ...)
    local args = {{...}}
    if type(fn) == "function" then
        return fn(unpack(args))
    elseif type(fn) == "string" and _G[fn] then
        return _G[fn](unpack(args))
    end
    return nil
end
{invoker_var}.call = function(obj, method, ...)
    if type(obj) == "table" and obj[method] then
        return obj[method](obj, ...)
    end
    return nil
end

"""
        
        lines = code.split('\n')
        result_lines = [indirection_setup]
        
        for line in lines:
            original_line = line
            
            # Obfuscate common function calls with random chance
            if random.random() < 0.2:  # 20% chance
                # Replace print calls
                if 'print(' in line:
                    line = re.sub(r'\bprint\(', f'{invoker_var}.invoke("print", ', line)
                
                # Replace string function calls
                elif 'string.' in line:
                    line = re.sub(r'string\.(\w+)\(', rf'{invoker_var}.call(string, "\1", ', line)
                
                # Replace table function calls
                elif 'table.' in line:
                    line = re.sub(r'table\.(\w+)\(', rf'{invoker_var}.call(table, "\1", ', line)
            
            result_lines.append(line)
        
        return '\n'.join(result_lines)
    
    def add_fake_functions(self, code):
        """Add fake/dummy functions to confuse reverse engineering"""
        
        fake_functions = []
        for i in range(random.randint(3, 7)):
            func_name = self.generate_random_name(8)
            params = [self.generate_random_name(3) for _ in range(random.randint(1, 3))]
            
            fake_body = []
            for j in range(random.randint(2, 5)):
                operations = [
                    f"local {self.generate_random_name(4)} = {random.randint(1, 1000)}",
                    f"if {random.choice(['true', 'false', '1 == 1', 'nil == nil'])} then end",
                    f"for {self.generate_random_name(2)} = 1, {random.randint(1, 10)} do end",
                    f"local {self.generate_random_name(4)} = math.random()",
                ]
                fake_body.append(f"    {random.choice(operations)}")
            
            fake_func = f"""
local function {func_name}({', '.join(params)})
{chr(10).join(fake_body)}
    return {random.choice(params + ['nil', 'true', 'false'])}
end
"""
            fake_functions.append(fake_func)
        
        # Insert fake functions at the beginning
        fake_code = '\n'.join(fake_functions) + '\n-- Real code starts here\n' + code
        return fake_code
    
    def obfuscate_numbers(self, code):
        """Obfuscate numeric literals using mathematical expressions"""
        
        def replace_number(match):
            num = int(match.group(0))
            if num == 0:
                return random.choice(['(1-1)', '(0*5)', '(2-2)'])
            elif num == 1:
                return random.choice(['(2-1)', '(3-2)', '(5-4)'])
            elif num > 1 and num < 100:
                # Create mathematical expression
                base = random.randint(1, 10)
                if num > base:
                    return f'({base}+{num-base})'
                elif num < base:
                    return f'({base}-{base-num})'
                else:
                    return f'({base}*1)'
            return str(num)
        
        # Replace standalone numbers (not in strings or comments)
        result = re.sub(r'\b\d+\b', replace_number, code)
        return result
    
    def extreme_obfuscation(self, code, options=None):
        """Apply extreme obfuscation techniques for maximum protection"""
        if options is None:
            options = {
                'rename_variables': True,
                'remove_comments': True,
                'encode_strings': True,
                'minify': True,
                'obfuscate_control_flow': True,
                'obfuscate_metatables': True,
                'obfuscate_function_calls': True,
                'add_fake_functions': True,
                'obfuscate_numbers': True
            }
        
        result = self.advanced_obfuscation(code, options)
        
        if options.get('add_fake_functions', True):
            result = self.add_fake_functions(result)
            
        if options.get('obfuscate_function_calls', True):
            result = self.obfuscate_function_calls(result)
            
        if options.get('obfuscate_numbers', True):
            result = self.obfuscate_numbers(result)
        
        return result
    
    def basic_obfuscation(self, code, options=None):
        """Apply basic obfuscation techniques"""
        if options is None:
            options = {'rename_variables': True, 'remove_comments': True}
        
        result = code
        
        if options.get('remove_comments', True):
            result = self.remove_comments(result)
        
        if options.get('rename_variables', True):
            result = self.rename_variables(result)
        
        return result
    
    def medium_obfuscation(self, code, options=None):
        """Apply medium obfuscation techniques"""
        if options is None:
            options = {
                'rename_variables': True,
                'remove_comments': True,
                'encode_strings': True,
                'minify': True
            }
        
        result = self.basic_obfuscation(code, options)
        
        if options.get('encode_strings', True):
            result = self.encode_strings(result)
        
        if options.get('minify', True):
            result = self.minify_code(result)
        
        return result
    
    def advanced_obfuscation(self, code, options=None):
        """Apply advanced obfuscation techniques"""
        if options is None:
            options = {
                'rename_variables': True,
                'remove_comments': True,
                'encode_strings': True,
                'minify': True,
                'obfuscate_control_flow': True,
                'obfuscate_metatables': True
            }
        
        result = self.medium_obfuscation(code, options)
        
        if options.get('obfuscate_control_flow', True):
            result = self.obfuscate_control_flow(result)
            
        if options.get('obfuscate_metatables', True):
            result = self.obfuscate_with_metatables(result)
        
        return result

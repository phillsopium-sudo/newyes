// Lua Obfuscator Frontend JavaScript

class LuaObfuscatorApp {
    constructor() {
        this.initializeElements();
        this.attachEventListeners();
        this.updateStats();
    }

    initializeElements() {
        // Form elements
        this.form = document.getElementById('obfuscationForm');
        this.luaCodeTextarea = document.getElementById('luaCode');
        this.obfuscatedCodeTextarea = document.getElementById('obfuscatedCode');
        this.obfuscationLevelSelect = document.getElementById('obfuscationLevel');
        
        // Option checkboxes
        this.renameVariablesCheckbox = document.getElementById('renameVariables');
        this.encodeStringsCheckbox = document.getElementById('encodeStrings');
        this.removeCommentsCheckbox = document.getElementById('removeComments');
        this.minifyCheckbox = document.getElementById('minify');
        this.obfuscateControlFlowCheckbox = document.getElementById('obfuscateControlFlow');
        this.obfuscateMetatablesCheckbox = document.getElementById('obfuscateMetatables');
        this.obfuscateFunctionCallsCheckbox = document.getElementById('obfuscateFunctionCalls');
        this.addFakeFunctionsCheckbox = document.getElementById('addFakeFunctions');
        this.obfuscateNumbersCheckbox = document.getElementById('obfuscateNumbers');
        
        // Buttons
        this.obfuscateBtn = document.getElementById('obfuscateBtn');
        this.validateBtn = document.getElementById('validateBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.copyBtn = document.getElementById('copyBtn');
        
        // Stats elements
        this.originalStats = document.getElementById('originalStats');
        this.obfuscatedStats = document.getElementById('obfuscatedStats');
        
        // Alert container
        this.alertContainer = document.getElementById('alertContainer');
    }

    attachEventListeners() {
        // Form submission
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.obfuscateCode();
        });

        // Button clicks
        this.validateBtn.addEventListener('click', () => this.validateSyntax());
        this.clearBtn.addEventListener('click', () => this.clearAll());
        this.copyBtn.addEventListener('click', () => this.copyResult());

        // Text area changes
        this.luaCodeTextarea.addEventListener('input', () => this.updateStats());
        this.obfuscatedCodeTextarea.addEventListener('input', () => this.updateStats());

        // Level change updates options
        this.obfuscationLevelSelect.addEventListener('change', () => this.updateOptionsForLevel());
    }

    updateOptionsForLevel() {
        const level = this.obfuscationLevelSelect.value;
        
        // Reset all options first
        this.renameVariablesCheckbox.checked = false;
        this.encodeStringsCheckbox.checked = false;
        this.removeCommentsCheckbox.checked = false;
        this.minifyCheckbox.checked = false;
        this.obfuscateControlFlowCheckbox.checked = false;
        this.obfuscateMetatablesCheckbox.checked = false;
        this.obfuscateFunctionCallsCheckbox.checked = false;
        this.addFakeFunctionsCheckbox.checked = false;
        this.obfuscateNumbersCheckbox.checked = false;

        // Set options based on level
        switch (level) {
            case 'basic':
                this.renameVariablesCheckbox.checked = true;
                this.removeCommentsCheckbox.checked = true;
                break;
            case 'medium':
                this.renameVariablesCheckbox.checked = true;
                this.removeCommentsCheckbox.checked = true;
                this.encodeStringsCheckbox.checked = true;
                this.minifyCheckbox.checked = true;
                break;
            case 'advanced':
                this.renameVariablesCheckbox.checked = true;
                this.removeCommentsCheckbox.checked = true;
                this.encodeStringsCheckbox.checked = true;
                this.minifyCheckbox.checked = true;
                this.obfuscateControlFlowCheckbox.checked = true;
                this.obfuscateMetatablesCheckbox.checked = true;
                break;
            case 'extreme':
                this.renameVariablesCheckbox.checked = true;
                this.removeCommentsCheckbox.checked = true;
                this.encodeStringsCheckbox.checked = true;
                this.minifyCheckbox.checked = true;
                this.obfuscateControlFlowCheckbox.checked = true;
                this.obfuscateMetatablesCheckbox.checked = true;
                this.obfuscateFunctionCallsCheckbox.checked = true;
                this.addFakeFunctionsCheckbox.checked = true;
                this.obfuscateNumbersCheckbox.checked = true;
                break;
        }
    }

    updateStats() {
        const originalCode = this.luaCodeTextarea.value;
        const obfuscatedCode = this.obfuscatedCodeTextarea.value;

        const originalLines = originalCode.split('\n').length;
        const originalChars = originalCode.length;
        const obfuscatedLines = obfuscatedCode.split('\n').length;
        const obfuscatedChars = obfuscatedCode.length;

        this.originalStats.textContent = `${originalLines} lines, ${originalChars} characters`;
        
        if (obfuscatedCode.trim()) {
            const reduction = originalChars > 0 ? ((originalChars - obfuscatedChars) / originalChars * 100).toFixed(1) : 0;
            this.obfuscatedStats.textContent = `${obfuscatedLines} lines, ${obfuscatedChars} characters (${reduction > 0 ? '-' : '+'}${Math.abs(reduction)}%)`;
        } else {
            this.obfuscatedStats.textContent = '';
        }
    }

    getObfuscationOptions() {
        return {
            rename_variables: this.renameVariablesCheckbox.checked,
            encode_strings: this.encodeStringsCheckbox.checked,
            remove_comments: this.removeCommentsCheckbox.checked,
            minify: this.minifyCheckbox.checked,
            obfuscate_control_flow: this.obfuscateControlFlowCheckbox.checked,
            obfuscate_metatables: this.obfuscateMetatablesCheckbox.checked,
            obfuscate_function_calls: this.obfuscateFunctionCallsCheckbox.checked,
            add_fake_functions: this.addFakeFunctionsCheckbox.checked,
            obfuscate_numbers: this.obfuscateNumbersCheckbox.checked
        };
    }

    setButtonLoading(button, loading) {
        if (loading) {
            button.disabled = true;
            button.classList.add('btn-loading');
            const icon = button.querySelector('i');
            if (icon) {
                icon.className = 'fas fa-spinner spinning me-1';
            }
        } else {
            button.disabled = false;
            button.classList.remove('btn-loading');
            const icon = button.querySelector('i');
            if (icon) {
                // Restore original icon based on button
                if (button === this.obfuscateBtn) {
                    icon.className = 'fas fa-magic me-1';
                } else if (button === this.validateBtn) {
                    icon.className = 'fas fa-check-circle me-1';
                }
            }
        }
    }

    showAlert(message, type = 'danger') {
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'warning' ? 'exclamation-triangle' : 'exclamation-circle'} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        this.alertContainer.innerHTML = alertHtml;
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alert = this.alertContainer.querySelector('.alert');
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    }

    async obfuscateCode() {
        const code = this.luaCodeTextarea.value.trim();
        
        if (!code) {
            this.showAlert('Please enter some Lua code to obfuscate.', 'warning');
            return;
        }

        this.setButtonLoading(this.obfuscateBtn, true);
        this.clearAlerts();

        try {
            const response = await fetch('/api/obfuscate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    code: code,
                    level: this.obfuscationLevelSelect.value,
                    options: this.getObfuscationOptions()
                })
            });

            const data = await response.json();

            if (data.success) {
                this.obfuscatedCodeTextarea.value = data.obfuscated_code;
                this.copyBtn.disabled = false;
                this.updateStats();
                this.showAlert(
                    `Code obfuscated successfully! Level: ${data.level}. Size changed from ${data.original_size} to ${data.obfuscated_size} characters.`,
                    'success'
                );
            } else {
                this.showAlert(`Obfuscation failed: ${data.error}`, 'danger');
            }
        } catch (error) {
            this.showAlert(`Network error: ${error.message}`, 'danger');
        } finally {
            this.setButtonLoading(this.obfuscateBtn, false);
        }
    }

    async validateSyntax() {
        const code = this.luaCodeTextarea.value.trim();
        
        if (!code) {
            this.showAlert('Please enter some Lua code to validate.', 'warning');
            return;
        }

        this.setButtonLoading(this.validateBtn, true);
        this.clearAlerts();

        try {
            const response = await fetch('/api/validate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    code: code
                })
            });

            const data = await response.json();

            if (data.success) {
                if (data.valid) {
                    this.showAlert('✓ Lua syntax is valid!', 'success');
                } else {
                    this.showAlert(`Syntax error: ${data.error_message}`, 'danger');
                }
            } else {
                this.showAlert(`Validation failed: ${data.error}`, 'danger');
            }
        } catch (error) {
            this.showAlert(`Network error: ${error.message}`, 'danger');
        } finally {
            this.setButtonLoading(this.validateBtn, false);
        }
    }

    clearAll() {
        this.luaCodeTextarea.value = '';
        this.obfuscatedCodeTextarea.value = '';
        this.copyBtn.disabled = true;
        this.updateStats();
        this.clearAlerts();
    }

    clearAlerts() {
        this.alertContainer.innerHTML = '';
    }

    async copyResult() {
        const obfuscatedCode = this.obfuscatedCodeTextarea.value;
        
        if (!obfuscatedCode.trim()) {
            this.showAlert('No obfuscated code to copy.', 'warning');
            return;
        }

        try {
            await navigator.clipboard.writeText(obfuscatedCode);
            
            // Visual feedback
            const originalText = this.copyBtn.innerHTML;
            this.copyBtn.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
            this.copyBtn.classList.remove('btn-outline-secondary');
            this.copyBtn.classList.add('btn-copy-success');
            
            setTimeout(() => {
                this.copyBtn.innerHTML = originalText;
                this.copyBtn.classList.remove('btn-copy-success');
                this.copyBtn.classList.add('btn-outline-secondary');
            }, 2000);
            
        } catch (error) {
            this.showAlert('Failed to copy to clipboard. Please select and copy manually.', 'warning');
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new LuaObfuscatorApp();
});

// Smooth scrolling for anchor links in documentation
document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Update active link in navigation
                links.forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            }
        });
    });
});

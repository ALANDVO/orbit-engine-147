"""SMS OTP authentication module with WebOTP API support.

This module provides SMS OTP functionality with support for literal newlines
in templates to comply with the WebOTP API specification.
See: https://wicg.github.io/sms-one-time-codes/#origin-bound-one-time-code-message
"""

import re
import secrets
import time
from dataclasses import dataclass, field
from typing import Optional, Dict, Tuple


@dataclass
class SmsOtpConfig:
    """Configuration for SMS OTP service."""
    # Template with {{code}} and {{origin}} placeholders.
    # Supports literal newlines for WebOTP API compliance.
    template: str = "Your code is {{code}}\n{{origin}}"
    code_length: int = 6
    expiry_seconds: int = 300
    # Regex to validate phone numbers (E.164 format)
    phone_regex: str = r"^\+[1-9]\d{1,14}$"


@dataclass
class SmsOtpCode:
    """Represents a generated OTP code with metadata."""
    code: str
    phone: str
    created_at: float = field(default_factory=time.time)
    expires_at: float = field(default_factory=lambda: time.time() + 300)


class SmsOtpService:
    """SMS OTP service with WebOTP-compatible template rendering."""
    
    def __init__(self, config: Optional[SmsOtpConfig] = None):
        self.config = config or SmsOtpConfig()
        self._codes: Dict[str, SmsOtpCode] = {}
    
    def generate_code(self) -> str:
        """Generate a secure random numeric code."""
        return "".join(str(secrets.randbelow(10)) for _ in range(self.config.code_length))
    
    def validate_phone(self, phone: str) -> bool:
        """Validate phone number format."""
        return bool(re.match(self.config.phone_regex, phone))
    
    def render_sms(self, code: str, origin: str) -> str:
        """Render SMS template with code and origin.
        
        Supports literal newlines in template for WebOTP API compliance.
        The template uses {{code}} and {{origin}} placeholders.
        """
        # Replace placeholders - template may contain literal newlines
        rendered = self.config.template.replace("{{code}}", code).replace("{{origin}}", origin)
        return rendered
    
    def send_otp(self, phone: str, origin: str) -> Tuple[bool, Optional[str]]:
        """Generate and store OTP for a phone number.
        
        Returns (success, error_message). In production, this would
        integrate with an SMS provider (Twilio, etc.).
        """
        if not self.validate_phone(phone):
            return False, "Invalid phone number format. Use E.164 format (e.g., +15551234567)"
        
        code = self.generate_code()
        expires_at = time.time() + self.config.expiry_seconds
        
        self._codes[phone] = SmsOtpCode(
            code=code,
            phone=phone,
            created_at=time.time(),
            expires_at=expires_at
        )
        
        # In production, send SMS here using provider
        # sms_provider.send(phone, self.render_sms(code, origin))
        
        return True, None
    
    def verify_otp(self, phone: str, code: str) -> Tuple[bool, Optional[str]]:
        """Verify OTP code for a phone number.
        
        Returns (success, error_message).
        """
        if phone not in self._codes:
            return False, "No OTP code found for this phone number"
        
        otp = self._codes[phone]
        
        if time.time() > otp.expires_at:
            del self._codes[phone]
            return False, "OTP code has expired"
        
        if otp.code != code:
            return False, "Invalid OTP code"
        
        # Success - remove used code
        del self._codes[phone]
        return True, None
    
    def get_rendered_sms(self, phone: str, origin: str) -> Optional[str]:
        """Get the rendered SMS for a phone (for testing/preview)."""
        if phone not in self._codes:
            return None
        return self.render_sms(self._codes[phone].code, origin)


def create_sms_otp_service(template: Optional[str] = None, 
                           code_length: int = 6, 
                           expiry_seconds: int = 300) -> SmsOtpService:
    """Factory function to create SMS OTP service with custom template."""
    config = SmsOtpConfig(
        template=template or "Your code is {{code}}\n{{origin}}",
        code_length=code_length,
        expiry_seconds=expiry_seconds
    )
    return SmsOtpService(config)


"""Tests for SMS OTP authentication module."""

import pytest
from app.auth import (
    SmsOtpConfig,
    SmsOtpService,
    SmsOtpCode,
    create_sms_otp_service,
)


class TestSmsOtpConfig:
    """Tests for SmsOtpConfig dataclass."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = SmsOtpConfig()
        assert config.template == "Your code is {{code}}\n{{origin}}"
        assert config.code_length == 6
        assert config.expiry_seconds == 300
        assert config.phone_regex == r"^\+[1-9]\d{1,14}$"
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = SmsOtpConfig(
            template="Code: {{code}}\n{{origin}}",
            code_length=4,
            expiry_seconds=600,
            phone_regex=r"^\+1\d{10}$"
        )
        assert config.template == "Code: {{code}}\n{{origin}}"
        assert config.code_length == 4
        assert config.expiry_seconds == 600
        assert config.phone_regex == r"^\+1\d{10}$"


class TestSmsOtpCode:
    """Tests for SmsOtpCode dataclass."""
    
    def test_code_creation(self):
        """Test OTP code creation with timestamps."""
        code = SmsOtpCode(code="123456", phone="+15551234567")
        assert code.code == "123456"
        assert code.phone == "+15551234567"
        assert code.created_at > 0
        assert code.expires_at > code.created_at


class TestSmsOtpService:
    """Tests for SmsOtpService."""
    
    def test_generate_code_length(self):
        """Test code generation produces correct length."""
        service = SmsOtpService()
        code = service.generate_code()
        assert len(code) == 6
        assert code.isdigit()
    
    def test_generate_code_custom_length(self):
        """Test code generation with custom length."""
        config = SmsOtpConfig(code_length=4)
        service = SmsOtpService(config)
        code = service.generate_code()
        assert len(code) == 4
        assert code.isdigit()
    
    def test_validate_phone_valid(self):
        """Test phone validation with valid numbers."""
        service = SmsOtpService()
        assert service.validate_phone("+15551234567") is True
        assert service.validate_phone("+447911123456") is True
        assert service.validate_phone("+819012345678") is True
    
    def test_validate_phone_invalid(self):
        """Test phone validation with invalid numbers."""
        service = SmsOtpService()
        assert service.validate_phone("5551234567") is False  # missing +
        assert service.validate_phone("+05551234567") is False  # leading 0
        assert service.validate_phone("++15551234567") is False  # double +
        assert service.validate_phone("") is False
        assert service.validate_phone("not-a-phone") is False
    
    def test_render_sms_with_newline(self):
        """Test SMS rendering with literal newline for WebOTP."""
        service = SmsOtpService()
        rendered = service.render_sms("123456", "example.com")
        assert "123456" in rendered
        assert "example.com" in rendered
        assert "\n" in rendered  # WebOTP requires newline
    
    def test_render_sms_custom_template(self):
        """Test SMS rendering with custom template."""
        config = SmsOtpConfig(template="Code: {{code}} from {{origin}}")
        service = SmsOtpService(config)
        rendered = service.render_sms("123456", "example.com")
        assert rendered == "Code: 123456 from example.com"
    
    def test_render_sms_multiline_template(self):
        """Test SMS rendering with multiline template."""
        template = "Your verification code:\n{{code}}\n\nDomain: {{origin}}"
        config = SmsOtpConfig(template=template)
        service = SmsOtpService(config)
        rendered = service.render_sms("123456", "example.com")
        assert rendered == "Your verification code:\n123456\n\nDomain: example.com"
        assert rendered.count("\n") == 3
    
    def test_send_otp_valid_phone(self):
        """Test sending OTP to valid phone number."""
        service = SmsOtpService()
        success, error = service.send_otp("+15551234567", "example.com")
        assert success is True
        assert error is None
        assert "+15551234567" in service._codes
    
    def test_send_otp_invalid_phone(self):
        """Test sending OTP to invalid phone number."""
        service = SmsOtpService()
        success, error = service.send_otp("5551234567", "example.com")
        assert success is False
        assert error is not None
        assert "Invalid phone number" in error
    
    def test_verify_otp_success(self):
        """Test successful OTP verification."""
        service = SmsOtpService()
        service.send_otp("+15551234567", "example.com")
        code = service._codes["+15551234567"].code
        
        success, error = service.verify_otp("+15551234567", code)
        assert success is True
        assert error is None
        assert "+15551234567" not in service._codes  # code consumed
    
    def test_verify_otp_wrong_code(self):
        """Test OTP verification with wrong code."""
        service = SmsOtpService()
        service.send_otp("+15551234567", "example.com")
        
        success, error = service.verify_otp("+15551234567", "000000")
        assert success is False
        assert error == "Invalid OTP code"
        assert "+15551234567" in service._codes  # code not consumed
    
    def test_verify_otp_expired(self):
        """Test OTP verification with expired code."""
        config = SmsOtpConfig(expiry_seconds=-1)  # already expired
        service = SmsOtpService(config)
        service.send_otp("+15551234567", "example.com")
        code = service._codes["+15551234567"].code
        
        success, error = service.verify_otp("+15551234567", code)
        assert success is False
        assert error == "OTP code has expired"
        assert "+15551234567" not in service._codes
    
    def test_verify_otp_not_found(self):
        """Test OTP verification for non-existent phone."""
        service = SmsOtpService()
        success, error = service.verify_otp("+15551234567", "123456")
        assert success is False
        assert error == "No OTP code found for this phone number"
    
    def test_get_rendered_sms(self):
        """Test getting rendered SMS for preview."""
        service = SmsOtpService()
        service.send_otp("+15551234567", "example.com")
        rendered = service.get_rendered_sms("+15551234567", "example.com")
        assert rendered is not None
        assert "123456" not in rendered  # actual code, not literal
        assert "example.com" in rendered
        assert "\n" in rendered
    
    def test_get_rendered_sms_not_found(self):
        """Test getting rendered SMS for non-existent phone."""
        service = SmsOtpService()
        rendered = service.get_rendered_sms("+15551234567", "example.com")
        assert rendered is None


class TestCreateSmsOtpService:
    """Tests for factory function."""
    
    def test_factory_default(self):
        """Test factory with defaults."""
        service = create_sms_otp_service()
        assert isinstance(service, SmsOtpService)
        assert service.config.code_length == 6
        assert "\n" in service.config.template
    
    def test_factory_custom(self):
        """Test factory with custom parameters."""
        service = create_sms_otp_service(
            template="Custom {{code}} for {{origin}}",
            code_length=8,
            expiry_seconds=600
        )
        assert service.config.template == "Custom {{code}} for {{origin}}"
        assert service.config.code_length == 8
        assert service.config.expiry_seconds == 600


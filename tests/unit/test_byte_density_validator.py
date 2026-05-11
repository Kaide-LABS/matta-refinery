import pytest

def test_byte_density_validator():
    class MockValidationError(Exception): pass
    
    def validate_ratio(ratio, actual_ratio):
        if actual_ratio < 0.60:
            raise MockValidationError("byte-density gate")
            
    with pytest.raises(MockValidationError, match="byte-density gate"):
        validate_ratio(0.95, 0.30)

"""
Utility Helper Functions
Common utility functions used across the application
"""
import re
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import hashlib
import secrets
import string

def generate_unique_id() -> str:
    """Generate a unique ID"""
    return str(uuid.uuid4())

def generate_random_string(length: int = 32) -> str:
    """Generate a random string of specified length"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    # Check if it's a valid length (10-15 digits)
    return 10 <= len(digits_only) <= 15

def format_phone(phone: str) -> str:
    """Format phone number to standard format"""
    digits_only = re.sub(r'\D', '', phone)
    if len(digits_only) == 10:
        return f"({digits_only[:3]}) {digits_only[3:6]}-{digits_only[6:]}"
    elif len(digits_only) == 11 and digits_only[0] == '1':
        return f"+1 ({digits_only[1:4]}) {digits_only[4:7]}-{digits_only[7:]}"
    else:
        return phone

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove or replace unsafe characters
    filename = re.sub(r'[^\w\s.-]', '', filename)
    # Replace spaces with underscores
    filename = re.sub(r'\s+', '_', filename)
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:255-len(ext)-1] + '.' + ext if ext else name[:255]
    
    return filename

def calculate_age(birth_date: str) -> int:
    """Calculate age from birth date string (YYYY-MM-DD)"""
    try:
        birth = datetime.strptime(birth_date, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - birth.year
        
        # Adjust if birthday hasn't occurred this year
        if today.month < birth.month or (today.month == birth.month and today.day < birth.day):
            age -= 1
        
        return age
    except ValueError:
        return 0

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency amount"""
    if currency.upper() == "USD":
        return f"${amount:.2f}"
    else:
        return f"{amount:.2f} {currency}"

def parse_date(date_string: str) -> Optional[datetime]:
    """Parse date string to datetime object"""
    formats = [
        '%Y-%m-%d',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%m/%d/%Y',
        '%d/%m/%Y'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    return None

def format_date(date: datetime, format_string: str = '%Y-%m-%d') -> str:
    """Format datetime object to string"""
    return date.strftime(format_string)

def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return filename.split('.')[-1].lower() if '.' in filename else ''

def is_valid_file_type(filename: str, allowed_types: List[str]) -> bool:
    """Check if file type is allowed"""
    extension = get_file_extension(filename)
    return extension in [t.lower() for t in allowed_types]

def calculate_file_hash(file_content: bytes) -> str:
    """Calculate MD5 hash of file content"""
    return hashlib.md5(file_content).hexdigest()

def paginate_results(results: List[Any], page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """Paginate list of results"""
    total = len(results)
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        'data': results[start:end],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'has_next': end < total,
            'has_prev': page > 1
        }
    }

def mask_sensitive_data(data: str, mask_char: str = '*', visible_chars: int = 4) -> str:
    """Mask sensitive data like email or phone"""
    if len(data) <= visible_chars:
        return mask_char * len(data)
    
    if '@' in data:  # Email
        username, domain = data.split('@', 1)
        masked_username = username[:2] + mask_char * (len(username) - 2)
        return f"{masked_username}@{domain}"
    else:  # Phone or other
        return data[:visible_chars] + mask_char * (len(data) - visible_chars)

def generate_appointment_id() -> str:
    """Generate unique appointment ID"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_suffix = generate_random_string(6)
    return f"APT-{timestamp}-{random_suffix}"

def generate_record_id() -> str:
    """Generate unique medical record ID"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_suffix = generate_random_string(6)
    return f"REC-{timestamp}-{random_suffix}"

def time_ago(date: datetime) -> str:
    """Get human-readable time difference"""
    now = datetime.now()
    diff = now - date
    
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "Just now"

def validate_appointment_time(date: str, time: str) -> bool:
    """Validate if appointment date and time are in the future"""
    try:
        appointment_datetime = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M')
        return appointment_datetime > datetime.now()
    except ValueError:
        return False

def get_business_hours() -> Dict[str, str]:
    """Get business hours configuration"""
    return {
        'monday': '09:00-17:00',
        'tuesday': '09:00-17:00',
        'wednesday': '09:00-17:00',
        'thursday': '09:00-17:00',
        'friday': '09:00-17:00',
        'saturday': '09:00-13:00',
        'sunday': 'closed'
    }

def is_business_hours(date: str, time: str) -> bool:
    """Check if appointment is within business hours"""
    try:
        appointment_date = datetime.strptime(date, '%Y-%m-%d')
        day_name = appointment_date.strftime('%A').lower()
        
        business_hours = get_business_hours()
        if day_name not in business_hours or business_hours[day_name] == 'closed':
            return False
        
        hours_range = business_hours[day_name]
        start_time, end_time = hours_range.split('-')
        
        appointment_time = datetime.strptime(time, '%H:%M').time()
        start = datetime.strptime(start_time, '%H:%M').time()
        end = datetime.strptime(end_time, '%H:%M').time()
        
        return start <= appointment_time <= end
    
    except ValueError:
        return False
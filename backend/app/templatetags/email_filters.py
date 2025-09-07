from django import template
register = template.Library()

@register.filter
def smart_email(email):
    if not email:
        return "unknown@cropleaf.com"
    
    if len(email) <= 25:
        return email

    try:
        user_part, domain = email.split('@')
        suffix = f"...@{domain}"
        total_length = 25

        if len(suffix) > total_length:
            return suffix[-25:]

        prefix_length = total_length - len(suffix)
        prefix = user_part[:prefix_length]
        return f"{prefix}{suffix}"
    except ValueError:
        return email

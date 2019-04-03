from app import bcrypt


def hashpw(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


def matches(attempted_password, correct_password):
    return bcrypt.check_password_hash(correct_password, attempted_password)

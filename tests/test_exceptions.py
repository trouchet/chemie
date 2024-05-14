from fastapi import HTTPException

from backend.app.exceptions import (  # Replace with the actual path to your file
    CredentialsException,
    WrongCredentialsException,
    OpenRegistrationForbiddenException,
    InsufficientPrivilegesException,
    WeakPasswordException,
    NonMatchingPasswordsException,
    SamePreviousPasswordException,
    UserNotFoundException,
    InactiveUserException,
    UserAlreadyExistsByUsernameException,
    UserAlreadyExistsByEMailException,
    InvalidEmailException,
    UserRegistrationException,
    InexistentUserException,
    InexistentUserByUsernameException,
    InexistentUserByIDException,
    InexistentUserByEmailException,
    SuperUserForbiddenException,
    InvalidTokenException,
    WrongPasswordException,
)


# Helper function for some repetitive assertions
def assert_exception_attributes(exception: HTTPException, status_code: int, detail: str):
    assert exception.status_code == status_code
    assert exception.detail == detail


def test_credentials_exception():
    exception = CredentialsException()
    assert_exception_attributes(exception, 401, "Could not validate credentials")


def test_wrong_credentials_exception():
    exception = WrongCredentialsException()
    assert_exception_attributes(exception, 400, "Incorrect username or password")


def test_open_registration_forbidden_exception():
    exception = OpenRegistrationForbiddenException()
    assert_exception_attributes(exception, 403, "Open user registration is forbidden on this server")


def test_insufficient_privileges_exception():
    exception = InsufficientPrivilegesException()
    assert_exception_attributes(exception, 403, "The user doesn't have enough privileges")


def test_weak_password_exception():
    weak_password = "password123"
    exception = WeakPasswordException(weak_password)

    # You might need to adjust this assertion based on your password validation logic
    assert "Password does not meet security requirements" in exception.detail


def test_non_matching_passwords_exception():
    exception = NonMatchingPasswordsException()
    assert_exception_attributes(exception, 400, "Provided password does not match the user's password.")


def test_same_previous_password_exception():
    exception = SamePreviousPasswordException()
    assert_exception_attributes(exception, 400, "New password cannot be the same as the current one")


def test_user_not_found_exception():
    username = "test_user"
    exception = UserNotFoundException(username)
    assert_exception_attributes(exception, 403, f"User {username} not found")


def test_inactive_user_exception():
    exception = InactiveUserException()
    assert_exception_attributes(exception, 400, "Inactive user")


def test_user_already_exists_by_username_exception():
    exception = UserAlreadyExistsByUsernameException()
    assert_exception_attributes(exception, 400, "User with this username already exists in the system.")


def test_user_already_exists_by_email_exception():
    exception = UserAlreadyExistsByEMailException()
    assert_exception_attributes(exception, 409, "User with this email already exists in the system.")

def test_invalid_email_exception():
    invalid_email = "invalid_email"
    exception = InvalidEmailException(invalid_email)
    assert_exception_attributes(exception, 400, f"Invalid email: {invalid_email}.")


def test_user_registration_exception():
    inner_exception = Exception("Registration failed")
    exception = UserRegistrationException(inner_exception)
    assert_exception_attributes(exception, 500, f"Failed to register user: {inner_exception}")


def test_inexistent_user_exception():
    exception = InexistentUserException()
    assert_exception_attributes(exception, 404, "User not found")


def test_wrong_password_exception():
    exception = WrongPasswordException()
    assert_exception_attributes(exception, 400, "Incorrect password")


def test_inexistent_user_by_id_exception():
    exception = InexistentUserByIDException()
    assert_exception_attributes(exception, 404, "The user with this id does not exist in the system")
    
    
def test_inexistent_user_by_email_exception():
    exception = InexistentUserByEmailException()
    assert_exception_attributes(exception, 404, "The user with email does not exist in the system.")


def test_inexistent_user_by_username_exception():
    exception = InexistentUserByUsernameException()
    assert_exception_attributes(exception, 404, "The user with this id does not exist in the system")


def test_super_user_forbidden_exception():
    exception = SuperUserForbiddenException()
    assert_exception_attributes(exception, 403, "Super users are not allowed to delete themselves")


def test_invalid_token_exception():
    exception = InvalidTokenException()
    assert_exception_attributes(exception, 400, "Invalid token")

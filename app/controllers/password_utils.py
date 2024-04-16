from passlib.context import CryptContext

# Create a CryptContext object for password hashing and verification
# We will be using the bcrypt algorithm as it is secure and widely used for this purpose
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to hash the password and return it
def hash(password: str):
    return pwd_context.hash(password)


# Function to verify if the password that is passed in and the hashed password match
# Since it is a one way hash, we hash the input password and check with hashed password in DB
def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
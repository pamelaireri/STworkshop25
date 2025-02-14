import streamlit_authenticator as stauth

# List of passwords to hash
passwords = ['abc', 'def']

# Hash each password separately
hashed_passwords = [stauth.Hasher(password).hash(password) for password in passwords]

# Write both hashed passwords to a file, each on a new line
with open("hashed_passwords.txt", "w") as file:
    file.write("\n".join(hashed_passwords) + "\n")  # Join hashed passwords with newline

print("Hashed passwords saved to hashed_passwords.txt")
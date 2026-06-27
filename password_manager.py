# -----------------------------
# Import required libraries
# -----------------------------
from cryptography.fernet import Fernet
import json
import os
import hashlib
import pyperclip
import random
import string
# -----------------------------
# Load Secret Key for Encryption/Decryption
# -----------------------------
def load_key():
    with open("secret.key", "rb") as key_file:
        return key_file.read()

# Initialize Fernet encryption using the secret key
key = load_key()
fernet = Fernet(key)

# -----------------------------
# Load Saved Passwords from JSON file
# -----------------------------
def load_passwords():

    # If file doesn't exist, return empty dictionary
    if not os.path.exists("passwords.json"):
        return {}

    # Read JSON file safely
    with open("passwords.json", "r") as file:
        try:
            return json.load(file)
        except:
            return {}

# -----------------------------
# Save Passwords to JSON file
# -----------------------------
def save_passwords(data):

    with open("passwords.json", "w") as file:
        json.dump(data, file, indent=4)

# -----------------------------
# Add a new password (Encrypt and store)
# -----------------------------
def add_password():

    # Take user input
    website = input("Enter Website: ")
    password = input("Enter Password: ")

    # Encrypt password
    encrypted = fernet.encrypt(password.encode()).decode()

    # Load existing data
    data = load_passwords()

    # Store encrypted password with website as key
    data[website] = encrypted

    # Save updated data
    save_passwords(data)

    print("\n✅ Password Saved Successfully!\n")

# -----------------------------
# View all saved passwords (Decrypt and display)
# -----------------------------

def view_passwords():

    data = load_passwords()

    if not data:
        print("\nNo passwords saved.\n")
        return

    print("\nSaved Passwords")
    print("-" * 40)

    for website, encrypted in data.items():

        decrypted = fernet.decrypt(encrypted.encode()).decode()

        print(f"Website : {website}")
        print(f"Password: {decrypted}")

        # Auto copy to clipboard
        pyperclip.copy(decrypted)
        print("📋 Password copied to clipboard!")

        print("-" * 40)

# -----------------------------
# Search Password
# -----------------------------
def search_password():

    # Ask user for website name
    website = input("Enter website to search: ").strip().lower()

    # Load saved passwords
    data = load_passwords()

    # Check if any passwords are saved
    if not data:
        print("\n❌ No passwords saved.\n")
        return

    # Search for website (case-insensitive)
    for stored_website, encrypted in data.items():

        if stored_website.lower() == website:

            # Decrypt password
            decrypted = fernet.decrypt(encrypted.encode()).decode()

            print("\n" + "=" * 35)
            print("      PASSWORD FOUND")
            print("=" * 35)
            print(f"Website : {stored_website}")
            print(f"Password: {decrypted}")

            # Copy password to clipboard
            pyperclip.copy(decrypted)
            print("\n📋 Password copied to clipboard!")
            print("=" * 35 + "\n")

            return

    # Website not found
    print("\n❌ Website not found!\n")

# -----------------------------
# Delete Password
# -----------------------------
def delete_password():

    # Take website input and clean it
    website = input("Enter website to delete: ").strip().lower()

    # Load saved data
    data = load_passwords()

    # Flag to check if found
    found = False

    # Search and delete (case-insensitive)
    for stored_website in list(data.keys()):

        if stored_website.lower() == website:

            # Delete entry
            del data[stored_website]
            found = True
            break

    # Save updated data if deleted
    if found:
        save_passwords(data)
        print("\n🗑️ Password deleted successfully!\n")
    else:
        print("\n❌ Website not found.\n")

# -----------------------------
# Password Generator (Strong Random Password)
# -----------------------------

def generate_password():

    # Define character sets
    letters = string.ascii_letters      # a-z + A-Z
    digits = string.digits              # 0-9
    symbols = "!@#$%^&*()-_=+[]{}<>?"

    # Combine all characters
    all_chars = letters + digits + symbols

    # Ask user desired password length
    length = int(input("Enter password length (e.g. 8-16): "))

    # Generate random password
    password = ""

    for i in range(length):
        password += random.choice(all_chars)
 
    # Display generated password

    print("\n🔐 Generated Password:", password)
    print()
    
    # Copy to clipboard
    pyperclip.copy(password)
    print("📋 Password copied to clipboard!\n")
    

# -----------------------------
# Convert password into secure hash
# -----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -----------------------------
# Master Password Login System
# -----------------------------
def master_login():

    # First time setup
    if not os.path.exists("master.key"):

        print("\n🔐 Create Master Password (First Time Only)")
        password = input("Enter new master password: ")

        with open("master.key", "w") as file:
            file.write(hash_password(password))

        print("✅ Master password created!\n")
        return True

    # Login check
    else:

        password = input("Enter master password: ")

        with open("master.key", "r") as file:
            saved_password = file.read()

        if hash_password(password) == saved_password:
            print("\n✅ Login successful!\n")
            return True
        else:
            print("\n❌ Wrong password. Exiting...\n")
            return False

# -----------------------------
# Main Menu (User Interface)
# -----------------------------

if not master_login():
    exit()

while True:

    print("=" * 35)
    print("      PASSWORD MANAGER")
    print("=" * 35)

    print("1. Add Password")
    print("2. View Passwords")
    print("3. Search Password")
    print("4. Delete Password")
    print("5. Generate Password")
    print("6. Exit")

    # Take user choice
    choice = input("\nEnter your choice: ")

    # -------------------------
    # Menu Options Handling
    # -------------------------
    if choice == "1":
        add_password()

    elif choice == "2":
        view_passwords()

    elif choice == "3":
        search_password()

    elif choice == "4":
        delete_password()

    elif choice == "5":
        generate_password()

    elif choice == "6":
        print("Goodbye!")
        break

else:
    print("Invalid choice! Try again.\n")
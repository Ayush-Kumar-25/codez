# Password Generator

A secure and customizable password generator desktop application developed using Python and Tkinter. This project was completed as a personal project during college to learn GUI development, file handling, and secure password generation techniques.

The goal of the project is to generate strong, medium, or weak passwords, check their strength, save them for future use, and provide easy copy-to-clipboard functionality through a simple GUI.

---

## Project Type

**Personal Project**

---

## Features

* Wordlist-based password generation for more memorable passwords
* Customizable password length, strength, and number of passwords
* Avoids duplicate passwords
* Save passwords in generated_passwords.txt and generated_passwords.csv
* Copy the last generated password to clipboard with a single click
* View previously saved passwords in a scrollable window
* Strength evaluation: Weak, Medium, Strong

---

## Tech Stack

* Python 3.x
* Tkinter
* pyperclip
* CSV & File Handling
* random & string

---

## Project Structure

```
PasswordGenerator/
│── password_generator.py
│── file.txt               # Wordlist for password generation
│── generated_passwords.txt
│── generated_passwords.csv
│── requirements.txt
│── README.md
```

---

## How to Run the Project Locally

1. Clone the repository
   
```bash
git clone https://github.com/your-username/PasswordGenerator.git
```

2. Navigate to the project directory
   
```bash
cd PasswordGenerator
```

3. Install dependencies
   
```bash
pip install -r requirements.txt
```

4. Run the application
   
```bash
python password_generator.py
```

The GUI will open for interactive password generation.

---

## Notes

* This project was developed for learning purposes during college.
* It is not intended as a production-grade security tool.
* Future improvements may include advanced entropy-based generation and password history encryption.

---

## License

This project follows personal/educational guidelines.
It is intended solely for learning and demonstration purposes.

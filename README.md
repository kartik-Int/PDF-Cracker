PDF Password Cracker

A powerful Python tool for cracking password-protected PDF files using:

- Common dictionary attacks
- Custom wordlists
- Brute-force password generation
- Fast multithreaded execution

Built with **pikepdf**, **tqdm**, and **ThreadPoolExecutor** for speed and clarity.



Requirements

Install the required Python packages:

`pip install pikepdf tqdm`

Basic Usage:  `python3 pdf_cracker.py --pdf secret.pdf`

With custom wordlist: `python3 pdf_cracker.py --pdf secret.pdf --wordlist rockyou.txt`

With custom password: `python3 pdf_cracker.py --pdf secret.pdf --wordlist password123 letmein secretkey`

With specific length: `python3 pdf_cracker.py --pdf secret.pdf --range 3 5`

With specific worker in thread: `python3 pdf_cracker.py --pdf secret.pdf --workers 8`


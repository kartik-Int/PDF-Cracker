import hashlib 
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import itertools
import argparse
import shutil
import os
import sys
import pikepdf

common_wordlist = "wordlist.txt"
input_wordlist = "input_wordlist.txt"
# chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789!@#$&-_"
chars ="abcdefghijklmnopqrstuvwxyz"

def check_pass(pdf_file, password):
    try:
        with pikepdf.open(pdf_file, password=password) as pdf:
            # print(f"\nOpened {pdf_file} with {len(pdf.pages)} pages")
            return 1
    except pikepdf._core.PasswordError:
        # print(f"Password '{password}' failed for {pdf_file}")
        return 0


def generate_passwords(chars, length):
    for combo in itertools.product(chars, repeat=length):
        yield''.join(combo)

def threaded_bruteforce_attempt(pdf_file, length, max_workers):   #To be changed
    flag = [False]
    result = [None]

    def try_password(pwd):
        if flag[0]:
            return
        if check_pass(pdf_file,pwd):
            flag[0] = True
            result[0] = pwd

    with ThreadPoolExecutor(max_workers) as executor:
        futures = []
        for pwd in generate_passwords(chars, length):
            if flag[0]:
                break
            futures.append(executor.submit(try_password, pwd))
        for future in as_completed(futures):
            if flag[0]:
                break
            

    return result[0]

def threaded_dictionary(pdf_file,wordlist, max_workers,length = 20):
    flag =[False]
    result = [None]

    def try_password(pwd):
        if flag[0]:
            return
        if check_pass(pdf_file, pwd):
            flag[0] = True
            result[0] = pwd

    with open(wordlist) as f:
        passwords = [line.strip() for line in f.readlines() if len(line.strip()) <= length]

    with ThreadPoolExecutor(max_workers) as executor:
        futures = [executor.submit(try_password,pwd) for pwd in passwords]
        for future in tqdm(as_completed(futures),total=len(passwords),desc="Starting Dictionary Attack"):
            if flag[0]:
                break
    print("\n")
    return result[0]   


def crack_pdf(pdf_file, ipt, min_len, max_len, max_workers):
    global cracked_password

    if ipt == "wordlist":
        cracked_password = threaded_dictionary(pdf_file,input_wordlist, max_workers)
    elif ipt == "none":
        cracked_password = threaded_dictionary(pdf_file,common_wordlist,max_workers)
        if cracked_password:
            pass
        else:
            for length in tqdm(range(min_len,max_len+1),desc="Starting Bruteforce"):
                cracked_password = threaded_bruteforce_attempt(pdf_file, length , max_workers)
                if cracked_password:
                    break
    elif ipt=="range":
        cracked_password = threaded_dictionary(pdf_file,common_wordlist, max_workers, length=(max_len - min_len +1))
        if cracked_password:
            pass
        else:
            for length in tqdm(range(min_len,max_len+1),desc="Starting Bruteforce"):
                cracked_password = threaded_bruteforce_attempt(pdf_file, length , max_workers)
                if cracked_password:
                    break
        
    
    if cracked_password:
        print(f"\nPassword Cracked: {cracked_password}")
    else:
        print("\nPassword could not be cracked.")

def parse_args():
    parser = argparse.ArgumentParser(description="PDF Cracker")
    parser.add_argument("--pdf",required=True, help="Input PDF File")
    parser.add_argument("--wordlist",nargs ="*" ,help="Words or file path starting with @ sign. Usage: --wordlist @rockyou.txt or --wordlist pass1 pass2 ...")
    parser.add_argument("--range",nargs=2 ,type=int, default=[1, 4], help="Password length range. Usage: range 4 6. Length range by default is range 1 4")
    parser.add_argument("--workers",type=int, default=3, help="Worker use for threading")
    return parser.parse_args()


# Use if __name__ == "__main__": to parse args and run crack_hash().

if __name__ == "__main__":
    args = parse_args()
    ipt = 'none'
    
    if args.wordlist:
        ipt='wordlist'
        wordlist_input = args.wordlist
        if len(wordlist_input) == 1 and os.path.isfile(wordlist_input[0]):
            shutil.copy(wordlist_input[0], "input_wordlist.txt")
            # print("Wordlist file copied to input_wordlist.txt") #for my reference only

        # Case 2: it's a list of words
        else:
            with open("input_wordlist.txt", "w") as f:
                for word in wordlist_input:
                    f.write(word.strip() + "\n")
            # print("Words written to input_wordlist.txt") #for my reference only



    elif '--range' in sys.argv:
        ipt = 'range'
    else:
        ipt='none'

    crack_pdf(args.pdf, ipt, min_len=args.range[0], max_len=args.range[1],max_workers=args.workers)

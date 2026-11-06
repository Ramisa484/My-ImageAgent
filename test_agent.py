import ollama

def ask_agent(prompt):
    print("در حال فکر کردن...")
    # اتصال به مدل llava که نصب کردیم
    response = ollama.chat(model='llava', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    
    # چاپ جواب
    print("\n--- جواب ایجنت ---")
    print(response['message']['content'])
    print("------------------\n")

if __name__ == "__main__":
    print("سلام! من ایجنت تو هستم. (برای خروج بنویس exit)")
    while True:
        user_input = input("شما: ")
        if user_input.lower() == 'exit':
            break
        ask_agent(user_input)
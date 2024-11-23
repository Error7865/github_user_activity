from app import get_git_activity

def get():
    print(' >> Enter "e" to exit.')
    while True:
        username=input(' > Enter your github username: ')
        if username == 'e' or username == 'exit' or username == "quit" or username == "q":
            print('Bye!')
            break
        get_git_activity(url=f"https://api.github.com/users/{username}/events")

if __name__ == "__main__":
    get()
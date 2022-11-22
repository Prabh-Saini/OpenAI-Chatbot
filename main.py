import sys
from datetime import datetime
from inspect import currentframe
from json import load, JSONDecodeError
from time import sleep
import colorama
import openai


logo = \
    " █████╗ ██╗     ██████╗██╗  ██╗ █████╗ ████████╗                                                              \n" \
    "██╔══██╗██║    ██╔════╝██║  ██║██╔══██╗╚══██╔══╝                                                              \n" \
    "███████║██║    ██║     ███████║███████║   ██║                                                                 \n" \
    "██╔══██║██║    ██║     ██╔══██║██╔══██║   ██║                                                                 \n" \
    "██║  ██║██║    ╚██████╗██║  ██║██║  ██║   ██║                                                                 \n" \
    "╚═╝  ╚═╝╚═╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝                                                                   "


try:
    # change settings to where your settings.json is located in
    file_path = r"C:\Users\psaini25\OneDrive - St Francis Xavier College\Year 10\Computing\AI Chat Bot\settings.json"
    settings = load(open(file_path))
except JSONDecodeError:
    print("Unable to run script, error with settings.json")


def main() -> None:
    colorama.init()  # fix ascii escape characters bug in windows python console
    oobe()

    while True:
        response = get_api_data(get_user_input())
        if response.startswith("?"):
            response = response.split("? ")[1]
        response = remove_inject_start_text(response)
        loadingbar(f"AI: {response}\n", delay=0.05)


def oobe() -> None:
    #     print(f"\033[92m\n\n  █████╗ ██╗     ██████╗██╗  ██╗ █████╗ ████████╗\n ██╔══██╗██║    ██╔════╝██║  ██║██╔══██╗╚══██╔══╝\n ███████║██║    ██║     ███████║███████║   ██║   \n ██╔══██║██║    ██║     ██╔══██║██╔══██║   ██║   \n ██║  ██║██║    ╚██████╗██║  ██║██║  ██║   ██║   \n ╚═╝  ╚═╝╚═╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝\033[00m")
    print(f"\033[92m\n\n{logo}\033[00m")
    print(f"\033[94mBy Prabh - to exit press ctrl+c, or type exit.\033[00m")
    print(f"\033[93mMaximum character limit is set to ~{int(settings['config']['max_tokens']) * 4} characters. "
          f"Creativity is set to {settings['config']['temperature']}%.\033[00m\n")


def get_user_input() -> str:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        try:
            print(f"\033[91mAI Chat bot turning off in five seconds...\033[00m")
            sleep(5)
            exit(0)
        except KeyboardInterrupt:
            print(f"\033[91mForce exit\033[00m")
    return user_input.strip()


def get_api_data(user_input: str) -> str:
    openai.api_key = settings["api_key"]
    config = settings["config"]

    try:
        response = openai.Completion.create(
            model=config["model"],
            prompt=f"Human: {user_input}",
            temperature=config["temperature"] / 100,
            max_tokens=config["max_tokens"],
            top_p=config["top_p"],
            frequency_penalty=config["frequency_penalty"],
            presence_penalty=config["presence_penalty"]
        )

        return response.get("choices")[0]["text"].replace("\n\n", " ").strip().replace("Computer: ", "").replace(
            "Robot: ", "").replace("Animal: ", "").replace("Bot: ", "").replace("Chatbot: ", "")
    except Exception as exception_:
        error(f"Error occured whilst getting API data: {exception_}", finishprocess=True)


def loadingbar(newtext: str, size: int = 25, delay: float = 0.05):
    for i in range(size):
        sys.stdout.write("Loading response... [{0}]   \r".format('#' * (i + 1) + ' ' * ((size - 1) - i)))
        sys.stdout.flush()
        sleep(delay)
    print(end='\x1b[2K')
    sys.stdout.write(newtext)


def remove_inject_start_text(string) -> str:
    for i in range(0, len(string)):
        if string[i].istitle():
            return string[i:]
    return string


def error(text, show_time: bool = True, showlinenumber: bool = True, finishprocess: bool = False, exit_code: int = 1):
    result: str = f'Error: {text}'

    if showlinenumber:
        result += f"\n  -> Line Number: {currentframe().f_back.f_lineno}"

    if show_time:
        result += f"\n  -> Current Time: {datetime.now().strftime('%H:%M:%S')}"

    print(f"\033[91m{result}\033[00m")

    if finishprocess:
        try:
            print(f"\033[91mAI Chat bot turning off in five seconds...\033[00m")
            sleep(5)
            exit(exit_code)
        except KeyboardInterrupt:
            print(f"\033[91mForce exit\033[00m")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            print(f"\033[91mAI Chat bot turning off in five seconds...\033[00m")
            sleep(5)
            exit(0)
        except KeyboardInterrupt:
            print(f"\033[91mForce exit\033[00m")

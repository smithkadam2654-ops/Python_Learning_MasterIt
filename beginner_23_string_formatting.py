def main():
    name = "Alice"
    age = 30
    language = "Python"

    # 1. f-strings (Introduced in Python 3.6, highly recommended)
    f_string = f"My name is {name}, I am {age} years old, and I love {language}."
    print("f-string:    ", f_string)

    # 2. .format() method
    format_method = "My name is {}, I am {} years old, and I love {}.".format(name, age, language)
    print(".format():   ", format_method)

    # 3. % formatting (older style, similar to C's printf)
    percent_style = "My name is %s, I am %d years old, and I love %s." % (name, age, language)
    print("% style:     ", percent_style)

if __name__ == "__main__":
    main()

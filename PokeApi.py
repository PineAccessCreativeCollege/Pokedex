# Lambda to print each character on a new line
text_input = "wooper"
(lambda text: [print(char) for char in text])(text_input)

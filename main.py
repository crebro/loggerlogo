from interpreter.interpreter import make_token_grammar, LogoInterpreter, parse_tokens
import interpreter.logturtle as logturtle
import interpreter.errors as errors
import sys


def main():
    """
    Parse Logo
    """
    grammar = make_token_grammar()
    interpreter = LogoInterpreter.create_interpreter()
    interpreter.turtle_backend_args = dict(input_handler=interpreter.receive_input)

    interpreter.grammar = grammar
    script_folders = []
    interpreter.script_folders = script_folders

    interpreter.turtle_backend = logturtle.LogTurtleEnv.create_turtle_env()

    script = """
        make "a 10
        repeat 4 [fd (100 + :a) rt 90 make "a (:a + 10)]
    """
    tokens = parse_tokens(grammar, script)

    try:
        result = interpreter.process_commands(tokens)
    except Exception as ex:
        print("Processed tokens: {}".format(tokens.processed), file=sys.stderr)
        raise ex
    if result is not None:
        raise errors.LogoError("You don't say what to do with `{}`.".format(result))

    if interpreter.is_turtle_active():
        interpreter.turtle_backend.wait_complete()

    print(interpreter._turtle.getHistory())


if __name__ == "__main__":
    main()

import setuptools._distutils as distutils
import language_tool_python
from enchant import Dict
from nltk import word_tokenize, sent_tokenize, download

download('punkt')

def grammar_and_spelling_checker(text):
    # Tokenize the text into sentences and words
    sentences = sent_tokenize(text)
    words = [word_tokenize(sentence) for sentence in sentences]

    # Load the English language dictionary for spelling checking
    english_dict = Dict("en_UK")

    # Initialize language_tool_python for grammar checking
    tool = language_tool_python.LanguageTool('en-UK')

    spelling_errors = 0
    grammar_errors = 0
    error_messages = []
    corrected_sentences = []

    # Check grammar and spelling for each word
    for sentence in words:
        corrected_sentence = []

        for word in sentence:
            # Check for spelling errors
            if not english_dict.check(word):
                spelling_errors += 1
                suggestions = english_dict.suggest(word)
                error_messages.append(f"Spelling error: {word}, Suggestions: {', '.join(suggestions)}")
                # Use the first suggestion if available, otherwise keep the original word
                corrected_sentence.append(suggestions[0] if suggestions else word)
            else:
                corrected_sentence.append(word)

        # Join the words back into a sentence for grammar checking
        sentence_text = ' '.join(corrected_sentence)

        # Check for grammar errors
        matches = tool.check(sentence_text)
        grammar_errors += len(matches)

        for match in matches:
            error_messages.append(f"Grammar error: {match.ruleId} - {match.message}")

        # Append the corrected sentence
        corrected_sentences.append(sentence_text)

    # Calculate accuracy
    accuracy = calculate_accuracy(text, ' '.join(corrected_sentences))

    return spelling_errors, grammar_errors, error_messages, corrected_sentences, accuracy

def calculate_accuracy(original_text, corrected_text):
    original_tokens = word_tokenize(original_text)
    corrected_tokens = word_tokenize(corrected_text)
    correct_count = sum(1 for orig, corr in zip(original_tokens, corrected_tokens) if orig == corr)
    accuracy = (correct_count / len(original_tokens)) * 100
    return accuracy

def count_words(text):
    words = word_tokenize(text)
    return len(words)

if __name__ == "__main__":
    while True:
        # Get user input
        user_input = input("Enter the text you want to check (or 'exit' to quit): ")

        if user_input.lower() == 'exit':
            break

        # Run the grammar and spelling checker
        spelling_errors, grammar_errors, errors, corrected_sentences, accuracy = grammar_and_spelling_checker(user_input)

        # Print the errors and counts
        if errors:
            print(f"Spelling errors found: {spelling_errors}")
            print(f"Grammar errors found: {grammar_errors}")
            print("Error messages:")
            for error in errors:
                print(error)
        else:
            print("No errors found.")

        # Print corrected sentences
        print("Corrected Sentences:")
        for corrected_sentence in corrected_sentences:
            print(corrected_sentence)

        # Print accuracy
        print(f"Accuracy: {accuracy:.2f}%")

        # Print word count
        print(f"Word count: {count_words(user_input)}")

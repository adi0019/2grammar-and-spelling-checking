from flask import Flask, request, jsonify
import language_tool_python
import enchant
from nltk import word_tokenize, sent_tokenize

app = Flask(__name__)

def grammar_and_spelling_checker(text):
    # Tokenize the text into sentences and words
    sentences = sent_tokenize(text)
    words = [word_tokenize(sentence) for sentence in sentences]

    # Load the English language dictionary for spelling checking
    english_dict = enchant.Dict("en_US")

    # Initialize language_tool_python for grammar checking
    tool = language_tool_python.LanguageTool('en-US')

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

@app.route('/check_spelling_and_grammar', methods=['POST'])
def check_spelling_and_grammar():
    data = request.json
    text = data.get('text', '')
    spelling_errors, grammar_errors, errors, corrected_sentences, accuracy = grammar_and_spelling_checker(text)
    response = {
        "spelling_errors": spelling_errors,
        "grammar_errors": grammar_errors,
        "errors": errors,
        "corrected_sentences": corrected_sentences,
        "accuracy": accuracy,
    }
    return jsonify(response)

@app.route('/count_words', methods=['POST'])
def count_words_endpoint():
    data = request.json
    text = data.get('text', '')
    word_count = count_words(text)
    response = {
        "word_count": word_count
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)


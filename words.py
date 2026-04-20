import random
import urllib.request

def get_word_list():
	# Download a list of common English words
	try:
		url = "https://www.mit.edu/~ecprice/wordlist.10000"
		response = urllib.request.urlopen(url)
		long_txt = response.read().decode()
		word_list = long_txt.splitlines()
		# Filter out very short words for better test quality
		word_list = [w for w in word_list if len(w) > 2]
		return word_list
	except Exception:
		# Fallback to a small built-in list if download fails
		return [
			"example", "typing", "speed", "test", "python", "keyboard", "window", "canvas", "display", "random",
			"words", "sentence", "challenge", "practice", "accuracy", "result", "timer", "input", "output", "score",
			"letter", "space", "correct", "mistake", "repeat", "focus", "improve", "record", "finish", "start"
		]


# Simple bigram-based generator for natural word sequences (compact version)
def generate_typing_text(word_list, num_words=30):
	bigrams = {
		'the': ['cat', 'dog', 'man', 'woman', 'child', 'car', 'house', 'boy', 'girl'],
		'cat': ['sat', 'ran', 'jumped', 'slept'],
		'dog': ['barked', 'ran', 'jumped', 'slept'],
		'man': ['walked', 'ran', 'slept', 'drove'],
		'woman': ['walked', 'ran', 'slept', 'drove'],
		'boy': ['ran', 'jumped', 'slept'],
		'girl': ['ran', 'jumped', 'slept'],
		'car': ['drove', 'stopped', 'started'],
		'house': ['stood', 'was'],
		'sat': ['on', 'by', 'under'],
		'ran': ['to', 'from', 'with'],
		'jumped': ['over', 'on'],
		'walked': ['to', 'from'],
		'slept': ['in', 'on'],
		'drove': ['to', 'from'],
		'on': ['the'],
		'by': ['the'],
		'under': ['the'],
		'to': ['the'],
		'from': ['the'],
		'with': ['the'],
		'over': ['the'],
		'in': ['the'],
		'was': ['big', 'small'],
		'stood': ['by', 'under'],
		'stopped': ['by', 'at'],
		'started': ['quickly', 'slowly'],
		'big': ['cat', 'dog', 'house'],
		'small': ['cat', 'dog', 'house'],
		'quickly': ['ran', 'jumped'],
		'slowly': ['walked', 'ran'],
		'at': ['the'],
	}
	first_words = list(bigrams.keys())
	word = random.choice(first_words)
	result = [word]
	for i in range(num_words - 1):
		next_words = bigrams.get(word, first_words)
		word = random.choice(next_words)
		result.append(word)
	# Capitalize the first word and add punctuation every 7-10 words
	for i in range(0, len(result), random.randint(7, 10)):
		result[i] = result[i].capitalize()
		if i > 0:
			result[i-1] += random.choice(['.', '!', '?'])
	# Ensure the last word ends with punctuation
	if result[-1][-1] not in '.!?':
		result[-1] += random.choice(['.', '!', '?'])
	return ' '.join(result)
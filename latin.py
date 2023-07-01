from secrets import token_urlsafe
from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.latin.declension import CollatinusDecliner
from cltk.lemmatize.latin.backoff import BackoffLatinLemmatizer
from cltk.prosody.latin.macronizer import Macronizer
from cltk.tokenize.line import LineTokenizer
from cltk.tokenize.latin.sentence import SentenceTokenizer
from cltk.corpus.utils.formatter import remove_non_latin
from cltk.tokenize.word import WordTokenizer
import re
import linecache


##==========================if user option is 2=========================#
def formatter(declined):
	words=[]
	for _, value in declined.items():
		words = value
	for pair in words:
		word_1, word_2 = pair
		print(word_1 + ", " + word_2)

def jvtext(user_input):
  j = JVReplacer()
  user_input = j.replace(user_input)
  return (user_input)

def clean(text, lower = False):
  cleaned = re.sub(r"[\(\[].*?[\)\]]", "", text)
  cleaned = cleaned.replace("   ", " ").replace("  ", " ")
  if lower == True:
    lower_cleaned = cleaned.lower()
    return(cleaned, lower_cleaned)
  return(cleaned)

def decline(words): #assuming input is a lilst of words
  decliner = CollatinusDecliner()
  declined_words = {}
  try:
    for word in words:
      declined_word = decliner.decline(word)
      declined_words[word] = declined_word  #original word is the key and the declined word is the value
      #print(dec_word)
  except:
    Exception
  return(declined_words)

def lemma(tokens):
  lemmatizer = BackoffLatinLemmatizer()
  tokens = lemmatizer.lemmatize(tokens)
  return(tokens)

def macron(text):
  macronizer = Macronizer("tag_ngram_123_backoff")
  text = macronizer.macronize_text(text)
  return (text)

def line_tokenization(text):
  tokenizer = LineTokenizer("latin")
  text = tokenizer.tokenize(text)
  return (text)

def sentence_tokenization(text, punct=True):
  sent_tokenizer = SentenceTokenizer()
  sentences = sent_tokenizer.tokenize(text)
  updated_sentences = []
  if punct == True:
    for word in sentences:
      word = remove_non_latin(word)
      word = word.lower()
      updated_sentences.append(word)
      #print(sent)
    return(updated_sentences)
  return(sentences)


def word_tokenization(text):
  word_tokenizer = WordTokenizer("latin")
  words = word_tokenizer.tokenize(text)
  return (words)

def returns_based_on_options(option):
  sentences_list = sentence_tokenization(user_input, punct = True)
  sentence = sentences_list[0]
  words = word_tokenization(sentence)
  l_words = lemma(words)
  def lemma_function(lemmatized_words):
    lemma_list = []
    for word in l_words:
      lemma_list.append(word[1])
    return lemma_list
  lemma_list = lemma_function(l_words) 
  if option == '3' or option == '1' :
    declined = decline(lemma_list)
    word_dictionary_form = list(declined)[0]
    print('\n')
    print("Dictionary form: ", word_dictionary_form)
    dictionary = open("latin_to_english.txt")
    latin_to_english_dict = dictionary.read()
    dictionary.seek(0)
    arr = []
    line = 1
    for word in latin_to_english_dict:
        if word == '\n':
            line += 1
    
    for i in range(line):
        arr.append(dictionary.readline())

    def findline(word):
        for i in range(len(arr)):
            if word in arr[i]:
                print("Dictionary line", i+1, end=": ")
                line = linecache.getline(r"latin_to_english.txt", i+1)
                print(line)
    
    findline(word_dictionary_form)
  if option == '2' or option == '3':
    if(option == '2') :
      print("Dictionary form: ", lemma_list)
    print("                 ------------------DECLENSION/CONJUGATION TABLE---------------")
    declined = decline(lemma_list)
    formatter(declined)
    #print(declined)
  
#=========================Getting user input==========================#
print("*************************************************\n")
print("    Welcome to Daria's Latin Dictionary!\n")
print("*************************************************")
print("You can press the numbers associated with each option:")

while (1):
  print('\n')
  print("                 Menu:\n")
  print("1 -- only translate Latin -> English")
  print("2 -- only decline/conjuagete the Latin term")
  print("3 -- translate Latin -> English AND decline/conjuagete the Latin term")
  print("0 -- quit the program\n")
  user_menu_option = input("Please enter your option: ")
  if (int(user_menu_option) == 0):
    quit()
  if (int(user_menu_option) > 3) or (int(user_menu_option) < 1):
    user_menu_option = input("Please enter option 1, 2, or 3: ")
  user_input = input("Latin term: ")

  if user_menu_option == '2' :
    returns_based_on_options('2')

  ##=======================if user option is 1==========================#
  if user_menu_option == '1' :
    returns_based_on_options('1')
  #==============================if user option is 3===============================
  #first key is the dictionary form we will search for in the dictionary.txt
  if user_menu_option == '3' :
    returns_based_on_options('3')


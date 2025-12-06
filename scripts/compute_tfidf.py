"""
This file computes tf-idf scores from a dataset.

Arguments:
    input: The input CSV file (dataset).
    output: The output CSV file containing tf-idf scores.

Returns:
    A CSV file containing the tf-idf scores for all topics, with columns being the tokens/terms.

Usage: 
    python compute_tfidf.py -i <input> -o <output>

Example:
    python compute_tfidf.py -i 'dataset.csv' -o 'output_tfidf.csv'
"""

import pandas as pd
import numpy as np
import argparse
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer as wnl
from collections import Counter, defaultdict
import string
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger_eng')


def compute_tfidf(sorted_data, document_list):
    ''' Takes in a dictionary mapping each topic to its document 
        (i.e. a list of all associated headlines and snippets).
        Returns a dataframe containing the tf-idf scores of all terms for all topics.
    '''
    # Extract all the terms/tokens in the corpus 
    vocabulary = set()
    topic_tokens = defaultdict(list)

    for topic in document_list:
        # Extract list of all headlines and snippets for the topic
        topic_segments = sorted_data[topic] 

        for segment in topic_segments:
            words = word_tokenize(segment)
            cleaned_words = clean_word_tokens(words)

            for word, tag in pos_tag(cleaned_words):
                # Remove punctuation at the beginning and end of words
                while word and word[0] in string.punctuation:
                    word = word[1:]
                
                while word and word[-1] in string.punctuation:
                    word = word[:-1]

                if word in string.punctuation or word == "":    # ignore punctuation
                    continue
                
                lemma = custom_lemmatize(word, tag)             # convert term to its lemma
                vocabulary.add(lemma)
                topic_tokens[topic].append(lemma)

    # Compute document frequency for all topics
    doc_freq = Counter()
    for topic in document_list:
        doc_freq.update(set(topic_tokens[topic]))

    # Compute tf-idf scores
    tfidf_matrix = []
    for topic in document_list:
        tfidf_matrix.append(defaultdict(float))

        # Get term frequencies for the topic
        topic_word_counter = Counter(topic_tokens[topic])

        for word in sorted(vocabulary):
            tf = topic_word_counter[word]/topic_word_counter.total()   
            N = len(document_list)
            d = doc_freq[word]
            idf = np.log10(N/d) 
            tfidf_matrix[-1][word] = tf * idf
    
    # Turn into dataframe
    tfidf_df = pd.DataFrame(tfidf_matrix, index=document_list).sort_index(axis=1)

    return tfidf_df


def custom_lemmatize(word, tag): 
    ''' Perform a customized lemmatization of the word based on its tag. We include some edge cases. '''
    # Edge cases
    if word == 'Dodgers' or word == 'Oilers':
        return word.lower()
    
    # Ideally, we would do this for all adjectival/demonymic forms for countries.
    elif word == "Ukrainian":   
        return "ukraine"
    elif word == "Chinese":
        return "china"

    # General case
    wntag = tag[0].lower()
    word = word.lower().strip()
        
    # Ignore all words that are not nouns, verbs, adjectives, or adverbs
    # Source: https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk
    if wntag in ['c', 'd', 'e', 'i', 'l', 'p', 't', 'w']:
        wntag = None
    elif wntag == 'j':                          # Change adjective tag 
        wntag = 'r'
    elif wntag not in ['a', 'r', 'n', 'v']:     # If wntag is here, keep wntag as is
        wntag = None
    
    if not wntag:
        lemma = word
    else:
        lemma = wnl().lemmatize(word, wntag)
    
    # Fix situation in which does (verb) gets converted to doe (noun); no article contained the lemma "doe".
    if lemma == "doe":
        lemma = wnl().lemmatize("does", 'v')
    
    return lemma


def clean_word_tokens(words):
    ''' Returns a list of cleaned tokens. 
        Some tokens are merged to better adapt word_tokenize's tokenization to our context. 
    '''
    cleaned_words = []

    for i in range(len(words)):
        word = words[i]

        if word == "US":
            word = "U.S."

        elif i > 0:
            try:
                # Canada and US
                if word == 'Office' and words[i-1] == 'Oval':
                    cleaned_words.pop()
                    word = 'Oval Office'

                # Canada Governance
                elif word == 'Smith' and words[i-1] == 'Danielle':
                    cleaned_words.pop()
                    word = 'Danielle Smith'

                elif word == 'Eby' and words[i-1] == 'David':
                    cleaned_words.pop()        # only keep as Eby
                    word = 'Eby'
                
                # Elections
                elif word[:4].lower() == 'bank' and words[i-1] == 'central':
                    cleaned_words.pop()
                    word = 'central ' + word
                
                # International Relations
                elif word == 'Korea' and (words[i-1] == 'South' or words[i-1] == 'North'):
                    prev_word = cleaned_words.pop()
                    word = prev_word + ' ' + word
                
                elif word == 'Africa' and words[i-1] == 'South':
                    prev_word = cleaned_words.pop()
                    word = 'South Africa'

                elif word == 'Emirates' and words[i-1] == 'Arab' and words[i-2] == 'United':
                    cleaned_words.pop()
                    cleaned_words.pop()
                    word = 'UAE'
                
                elif word == 'Macron' and words[i-1] == 'Emmanuel':
                    cleaned_words.pop()     # remove Emmanuel, only keep Macron
                    word = "Macron"
                
                elif word == 'Trump' and words[i-1] == 'Donald':
                    cleaned_words.pop()     # remove Donald, only keep Trump
                    word = "Trump"

                elif word == 'Jinping' and words[i-1] == 'Xi':
                    continue                # ignore Jinping, keep Xi as is

                # Culture
                elif word == 'Jays' and words[i-1] == 'Blue':
                    cleaned_words.pop()
                    word = 'Blue Jays'
                
                elif word == 'Series' and words[i-1] == 'World':
                    cleaned_words.pop()
                    word = 'World Series'

                elif word == 'Day' and words[i-1] == "'s" and words[i-2] == 'Patrick' and words[i-3] == 'St.':
                    cleaned_words.pop()
                    cleaned_words.pop()
                    cleaned_words.pop()
                    word = "St. Patrick's Day"
                
                elif word == 'Cup' and words[i-1] == 'Grey':
                    cleaned_words.pop()
                    word = 'Grey Cup'

                elif word == 'rail' and words[i-1] == 'light':
                    cleaned_words.pop()
                    word = 'light rail'
                
                elif word == 'Angeles' and words[i-1] == 'Los':
                    cleaned_words.pop()
                    word = 'Los Angeles'

                # Opinion editorials
                elif word == 'tracks' and words[i-1] == 'fast':
                    cleaned_words.pop()
                    word = 'fast track'
                
                elif word == 'News' and words[i-1] == 'Fox':
                    cleaned_words.pop()
                    word = 'Fox News'

                elif word == 'Hannity' and words[i-1] == 'Sean':
                    cleaned_words.pop()
                    word = 'Sean Hannity'

                elif word == 'Sarkonak' and words[i-1] == 'Jamie':
                    cleaned_words.pop()
                    word = 'Jamie Sarkonak'
                
                elif word == 'Higgins' and words[i-1] == 'Michael':
                    cleaned_words.pop()
                    word = 'Michael Higgins'
                
                elif word == 'Taube' and words[i-1] == 'Michael':
                    cleaned_words.pop()
                    word = 'Michael Taube'
                
                elif word == 'Newman' and words[i-1] == 'Terry':
                    cleaned_words.pop()
                    word = 'Terry Newman'

                elif word == 'Glavin' and words[i-1] == 'Terry':
                    cleaned_words.pop()
                    word = 'Terry Glavin'

                elif word == 'Selley' and words[i-1] == 'Chris':
                    cleaned_words.pop()
                    word = 'Chris Selley'

                elif word == 'Jerema' and words[i-1] == 'Carson':
                    cleaned_words.pop()
                    word = 'Carson Jerema'

                elif word == 'Black' and words[i-1] == 'Conrad':
                    cleaned_words.pop()
                    word = 'Conrad Black'    

                elif word == 'Russ' and words[i-1] == 'Geoff':
                    cleaned_words.pop()
                    word = 'Geoff Russ' 

                elif word == 'Hamm' and words[i-1] == 'Amy':
                    cleaned_words.pop()
                    word = 'Amy Hamm'
                
            except:
                word = word
        
        if word == 'Eby':               # replace Eby by David Eby, after parsing
            word = 'David Eby'
        
        # Ignore characters
        elif len(word) == 1:  
            continue

        cleaned_words.append(word)
    
    return cleaned_words


def main():
    parser = argparse.ArgumentParser(description="Compute tf-idf scores")
    parser.add_argument('-i','--input', type=str, help="The input CSV file")
    parser.add_argument('-o','--output', type=str, default="output_tfidf.csv", help="The output CSV file containing tf-idf scores")
    parser.add_argument('-c','--country', type=str, default=None, help="The country for which we filter, either 'US' or 'Canada'")
    
    args = parser.parse_args()

    # Load CSV into dataframe
    df = pd.read_csv(args.input)
    topic_list = list(df['open coding/categories'].unique())

    # Clean NaN in headlines, snippets
    df['headline'] = df['headline'].fillna('')
    df['snippet'] = df['snippet'].fillna('')

    # Group all articles headlines and snippets by topic
    sorted_df = {}
    for topic in topic_list:
        topic_rows = df.loc[df['open coding/categories'] == topic]
        if args.country is not None:
            try:
                topic_rows = topic_rows.loc[topic_rows['Country'] == args.country]
            except:
                if args.country not in ['US', 'Canada']:
                    print("ERROR: Please input either 'US' or 'Canada' in the 'country' argument.")

        # Collect headlines, snippets for that topic 
        topic_headlines = topic_rows['headline'] # a "list" of all headlines
        topic_snippets = topic_rows['snippet'] 

        sorted_df[topic] = list(topic_headlines)
        sorted_df[topic].extend(list(topic_snippets))

    # Compute tf-idf scores over the corpus
    print("Computing tf-idf scores...")
    tfidf_matrix = compute_tfidf(sorted_df, topic_list)               

    print(f"Saving tf-idf scores to file {args.output}...")
    tfidf_matrix.to_csv(args.output, index=True)
    
    # Load tf-idf scores
    tfidf_matrix = pd.read_csv(args.output, index_col=0)

    print("Top ten tf-idf scores are...")
    for topic in topic_list:
        print(f'\n=========={topic}==========')
        topic_row = tfidf_matrix.loc[topic].sort_values(ascending=False)
        tenth_tfidf = topic_row.iloc[9]
        s = pd.Series(topic_row[topic_row >= tenth_tfidf])
        print(s)

    return


if __name__ == "__main__":
    main()

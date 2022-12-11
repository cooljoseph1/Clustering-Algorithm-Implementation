#!/bin/bash

mkdir -p data

echo "Downloading words..."
curl https://raw.githubusercontent.com/taikuukaits/SimpleWordlists/master/Wordlist-Adjectives-All.txt -o data/words.txt
curl https://raw.githubusercontent.com/taikuukaits/SimpleWordlists/master/Wordlist-Adverbs-All.txt >> data/words.txt
curl https://raw.githubusercontent.com/taikuukaits/SimpleWordlists/master/Wordlist-Nouns-All.txt >> data/words.txt
curl https://raw.githubusercontent.com/taikuukaits/SimpleWordlists/master/Wordlist-Verbs-All.txt >> data/words.txt

echo "Sorting words..."
sort -o data/words.txt{,}

echo "Downloading antonyms..."
curl https://raw.githubusercontent.com/taikuukaits/SimpleWordlists/master/Thesaurus-Antonyms-All.txt -o data/antonyms.txt
sed -i '1d' data/antonyms.txt

echo "Downloading synonyms..."
curl https://raw.githubusercontent.com/taikuukaits/SimpleWordlists/master/Thesaurus-Synonyms-All.txt -o data/synonyms.txt
sed -i '1d' data/synonyms.txt

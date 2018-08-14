# spell-corrector-pl

Spelling corrector based on the idea of [Peter Norvig](https://norvig.com/spell-correct.html). Repository consists of three independent parts:

### 1) Fixing scripts

I decided to use N-grams (1-grams and 2-grams) extracted from balanced [National Corpus of Polish](http://zil.ipipan.waw.pl/NKJPNGrams), but these files required some fixes.

* *UnigramsFixer.py* removes words containing non-letter characters 
* *UnigramsSplitter.py* splits one big file into the set of files corresponding to the first letters of the words (*1grams_a*, *1grams_b*, ..., *1grams_z*)
* *BigramsSplitter.py* splits one really big file of 2-grams (1.9 GB) into set of files corresponding to the first two letters of bigrams (*2grams_aa*, *2grams_ab*, ..., *2grams_zz*)

### 2) Corrector for Polish language

Corrector (in Python) adapted to the Polish language. In addition to the standard implementation of Norvig's spell corrector, it also corrects the most popular typos in Polish - 'a' instead of 'ą', 's' instead of 'ś' etc.

#### How to run
Download *1grams.gz* from [here](http://zil.ipipan.waw.pl/NKJPNGrams), fix using *UnigramsFixer.py* and put into *n-grams* directory. Then go to `python/` and run *./InteractiveCorrector.py*. help. 

#### Usage

InteractiveCorrector.py [-h] [-b] [-w WORD] [-t TYPE]  

optional arguments:  

* *-h, --help* - show help message and exit
* *-b, --bigrams* - turn on using 2-grams to spell correction
* *-w WORD, --word WORD* - non-interactive mode, correct specified word(s)  
* *-t TYPE, --type TYPE* - type of unigrams provider  RAM/BigFile/MultipleFiles RAM is used by default

#### Examples

    ./InteractiveCorrector.py -w "slon i zaba pija wode"
    słoń i żaba piją wodę 

    ./InteractiveCorrector.py -w "wieszac ptanie"
    wieszać panie 

    ./InteractiveCorrector.py -b -w "wieszac ptanie"
    wieszać pranie 

#### Different WordsProvider to compare performance
There are implemented three KnownWordsProviders (responsible for reading n-grams from file(s) and checking if specified word is known). Results of selected tests:


| Word               | WordsProvider | Time  |
| -------------        |:-----------------:| ------------|
| zaba                | RAM              | 0m1.941s |
| zaba                | MultipleFiles  | 0m0.251s |
| zaba                | BigFile           | 0m2.926s |
| pogramowanie | RAM              | 0m1.970s |
| pogramowanie | MultipleFiles  | 0m2.218s |
| pogramowanie | BigFile           | 0m5.186s |


### 3) OCaml implementation

In order to improve my OCaml skills I implemented spelling corrector in this language. It uses unigrams (fixed by previously described script) and it's not yet adapted to the Polish. 

#### Compilation
    ocamlfind ocamlc str.cma -package core_extended -thread -linkpkg corrector.ml -o corrector


#### Usage:

* *./corector -i* to run in interactive mode
* *./corrector "phrase to correct"* or *./corrector word* to use non-interactive mode

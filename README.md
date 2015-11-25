# library-of-words

## Synopsis
Base engine for the website: libraryofwords.info
More info: libraryofwords.info/faq.html

## Usage:
  $ base.py [-s][-pt] [STRING]
  
## Examples:
  $ base.py -st 'Hello World!' #Output page containing just the Hello World string 
  $ base.py -sp 'abcde123' #Output text in page at location abcde123
  $ base.py -t 'Hello World!' #Output page containing the Hello World string and other random words from the vocabulary
  $ base.py -p 'abcde123' #Output text in page at location abcde123 and fills the rest of the page with other random words from the vocabulary
  
## Help:
  $ base.py -h

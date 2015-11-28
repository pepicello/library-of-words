# library-of-words

## Synopsis
Base engine for the website: http://libraryofwords.info  
More info: http://libraryofwords.info/faq.html  

## Usage:
```
  $ base.py [-s][-pt] [STRING]
  ```
## Examples:
  Outputs page containing just the "Hello World" string:
```
  $ base.py -st 'Hello World!' 
  ```
  Output text in page at location "abcde123":
  ```
  $ base.py -sp 'abcde123' 
  ```
  Output page containing the "Hello World" string and other random words from the vocabulary:
  ```
  $ base.py -t 'Hello World!'
  ```
  Output text in page at location "abcde123" and fills the rest of the page with other random words from the vocabulary:
  ```
  $ base.py -p 'abcde123' 
  ```
  
## Help:
```
  $ base.py -h
```

# wikitrendz
### Introduction
This project aims to analyze and visualize correlations between search frequency and revision frequency of wikipedia articles for given keywords.

### Usage
To run the tool simply clone the repository and make sure that you have all the needed python libraries installed.  
Then execute.  
The appearing window asks for how many titles should be loaded. The reason is that for test cases using all the titles could be - depending on your hardware - quite resource intensive. (In testing all 16+ mio titles took up roughly 37gb of RAM)  
If your machine does not hav a lot of hardware we would advise going with lower numbers.

Then, after loading the Trie / prefix tree you can enter the Keyword you want to search for, for example Larry Page and click on the matching suggestion.  
The Tool will then gather the data for your request and show the result.
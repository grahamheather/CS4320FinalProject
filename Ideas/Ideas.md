# Ideas
Resources:
- https://www.computersciencezone.org/50-most-useful-apis-for-developers/

## Google Translate + Weather Data
- API list says that YR.NO is "the largest weather database in the world", but it's in Norwegian
- YR.NO appears very easy to use, no sign-up required

Google Translate Cloud API:
https://cloud.google.com/translate/

YR.NO API:
http://www.yr.no/artikkel/information-about-the-free-data-1.6810075

Problems:
- Google Translate Cloud API isn't free (providing a credit card gets $300 of use, good for 12 months, but I couldn't find detailed documentation on how much their billing is for API use or how long $300 would likely last)
- yr.no documentation is in Norwegian (but surfing through Google Translate is pretty effective, translation appears accurate)

##### Apertium + Weather Data
Possible solution to problems:
- use Apertium which is free and open-source instead of Google Translate
- https://www.apertium.org/

## Tool to help learning the pronunciation of another language
The goal would be to take another language's writing system, and to produce a description of the sound of each letter using comparisons to sounds in the speaker's native language.
There are two possible ways of doing this:
1. Only compare sound systems (without working with writing systems).
  - http://phoible.org/
    - provides sound inventories of many of the world's languages
    - no online API but the entire database is freely available for download
  - Example:
    - An English speaker wants to learn French
    - French has the vowel ø which is not in English
    - The program describes this vowel as like e in English, but with the lips rounded
2. Compare writing systems and their corresponding sounds.
  - http://omniglot.com/writing/languages.htm
    - has the information but a little hard to work with
    - see omniglot.com/charts/LANG_NAME_HERE.xls
    - e.g. http://omniglot.com/charts/avar.xls
  - Or maybe the Wikipedia IPA help pages?
    - https://en.wikipedia.org/wiki/Help:IPA/English
  - Example:
    - A English speaker wants to learn French
    - French has the sound 'eu' which is pronounced ø (this is the phonetic transcription), which is not in English.
    - The program describes this vowel as like the vowel in 'face', but with the lips rounded.

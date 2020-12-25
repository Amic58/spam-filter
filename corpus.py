"""
    Author: David Otta
    Created for: B4B33RPH
    Created on 26. 10. 2020
    Last change on 02. 11. 2020
"""
 
 
class Corpus():
    def __init__(self, path):
        self.path = path
 
    def emails(self):
        import os
        file_names = os.listdir(self.path)
        for name in file_names:
            if name[0] == '!':  # special files
                continue
            body = ''
            with open(self.path + os.sep + name, 'r', encoding='utf-8') as fr:
                body = fr.read()
            yield name, body
 
 
if __name__ == "__main__":
    # Create corpus from a directory
    corpus = Corpus('spam-data-12-s75-h25/1/')
    count = 0
    # Go through all emails and print the filename and the message body
    for mname, mbody in corpus.emails():
        print(mname)
        print(mbody.encode('utf-8'))
        print('-------------------------')
        count += 1
    print('Finished: ', count, 'files processed.')

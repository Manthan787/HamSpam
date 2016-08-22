from config import DATA_PATH
import email
from bs4 import BeautifulSoup
import os
import sys
import splitter


class BatchParser(object):

    def __init__(self, data_path, labels):
        """
        :param data_path: Full path of the directory where the data resides
        :param labels: Dictionary to identify whether an email is spam or ham
        :return: Void
        """
        self.data_path = data_path
        self.labels = labels


    def parse(self):
        """
        :return: parsed files with all the Elasticsearch properties
        """
        files = os.listdir(self.data_path)
        parsed_files = {}
        i = 0
        for file in files:
            parsed_files[file] = {'text' : self.__parseEmail(file),
                                  'label' : self.labels[file],
                                  'split': splitter.get_split(),
                                  'docno': file}
            i += 1
            sys.stdout.write("Emails Parsed: %d \r" %i)
            sys.stdout.flush()

        return parsed_files


    def __parseEmail(self, file):
        """
        :param file: the name of the file containing the email contents
        :return: Parsed email
        """
        email_path = os.path.join(self.data_path, file)
        with open(email_path, 'r') as e:
            message = email.message_from_file(e)
        try:
            body = message['subject'].strip().decode('utf-8', 'ignore')
        except:
            body = u''

        if message.is_multipart():
            for payload in message.walk():
                ctype = payload.get_content_type()
                cdispo = str(payload.get('Content-Disposition'))
                if ctype in ['text/plain', 'text/html'] and 'attachment' not in cdispo:
                    text = payload.get_payload(decode=True).decode('utf-8', 'ignore').strip()
                    if ctype == 'text/html':
                        text = self.__parseHTML(text)
                    body += text
        else:
            ctype = message.get_content_type()
            text = message.get_payload(decode=True).decode('utf-8', 'ignore').strip()
            if ctype == 'text/html':
                text = self.__parseHTML(text)

            body += text

        return body


    def __parseHTML(self, html):
        """
        :param html: HTML document
        :return: Extract text from it after stripping of all scripts and style
                 markup
        """
        soup = BeautifulSoup(html, 'lxml')
        for elem in soup.findAll(['script', 'style']):
            elem.extract()

        text = soup.get_text()
        return text.strip().encode('utf-8')


if __name__ == "__main__":
    import Feedback
    labels = Feedback.load_labels()
    parser = BatchParser(DATA_PATH, labels)
    parser.parse()

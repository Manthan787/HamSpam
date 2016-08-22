from config import FEEDBACK_PATH


def load_labels():
    """
        Load labels from the file labels file
    """
    print "Loading labels!"
    with open(FEEDBACK_PATH, 'r') as f:
        lines = f.readlines()

    labels = {}
    for line in lines:
        label_email = line.split()
        label = label_email[0].strip().lower()
        email = label_email[1]
        email_no = email.split('/')[-1].strip()
        labels[email_no] = label

    return labels

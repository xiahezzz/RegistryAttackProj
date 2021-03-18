import os
import sys

def write_log(log_text):
    try:
        fp = open(os.path.dirname(sys.argv[0]) + '/run.log', 'a+')
        fp.write(log_text)
    except FileNotFoundError:
        fp = open(os.path.dirname(sys.argv[0]) + '/run.log', 'w')
        fp.write(log_text)
    fp.close()

if __name__ == '__main__':
    print(os.path.dirname(sys.argv[0]) + '/run.log')

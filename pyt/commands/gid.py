"""The gid command."""
from .base import Base


class Gid(Base):
    """Generate automate id for each test case!"""

    def run(self):

        in_f = self.options['<file>']
        prefix = self.options['<pattern>']
        is_append = self.options['--append']
        out_f = self.options['--output']
        catcount = {}

        out_f = out_f or in_f
        content = []

        if is_append:
            # get max existing id
            with open(in_f) as f:
                lines = f.readlines()
                sum_rno = len(lines)
                while sum_rno >= 0:
                    sum_rno -= 1
                    line = lines[sum_rno].strip()
                    if line and line.startswith('{') and line.endswith('}'):
                        catcount = eval(line)
                        break
        else:
            sum_rno = -1

        with open(in_f) as f:
            for idx, line in enumerate(f):
                word = line.split(' ')[0]
                if word.find(prefix) in [0, 1]:
                    word_wo_nnn = word[:-4]
                    worduc = word_wo_nnn.replace('#', '')
                    # print word_wo_nnn, worduc
                    if worduc in catcount:
                        if not is_append or not word[-3:].isdigit():
                            catcount[worduc] += 1
                            content.append(line.replace(word, word_wo_nnn + '.%03d' % catcount[worduc]).rstrip())
                        else:
                            content.append(line.rstrip())
                    else:
                        catcount[worduc] = 1
                        content.append(line.replace(word, word_wo_nnn + '.%03d' % catcount[worduc]).rstrip())
                    content.append('\n')
                else:
                    if idx != sum_rno:
                        content.append(line.rstrip())
                        content.append('\n')
                    else:
                        content.append(str(catcount))
                        content.append('\n')
        if not is_append:
            content.append('\n\n')
            content.append(str(catcount))
            content.append('\n')
        with open(out_f, "w") as f:
            f.writelines(content)
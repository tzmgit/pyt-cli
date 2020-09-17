"""The gid command."""
import re

from .base import Base


class Gid(Base):
    """Generate automate id for each test case!"""

    def read_summary(self, in_f):
        """Read summary info and return index of summary line in test file."""
        sum_rno = 0
        summary = {}
        with open(in_f) as f:
            lines = f.readlines()
            sum_rno = len(lines)
            while sum_rno >= 0:
                sum_rno -= 1
                line = lines[sum_rno].strip()
                if line and line.startswith('{') and line.endswith('}'):
                    summary = eval(line)
                    break
        return summary, sum_rno

    def verify(self, in_f, summary, pattern):
        """Verify test id in test file."""
        print 'verifying test ids...'
        ids = set()
        with open(in_f) as f:
            for line in f:
                test_id = line.split(' ')[0]
                if re.match(pattern, test_id):
                    if test_id in ids:
                        print 'duplicate test id: {}'.format(test_id)
                    else:
                        ids.add(test_id)
                    id_base, _, id_num = test_id.rpartition('.')
                    if id_base not in summary:
                        print 'test case id base {} not found in summary'.format(id_base)
                    if not id_num.isdigit():
                        print 'test case id number is not a number'
                    else:
                        id_num = int(id_num)
                        if id_num <= 0:
                            print 'ivalid test case id: {}'.format(test_id)
                        elif id_base in summary and id_num > summary[id_base]:
                            print 'test case id {} does not match summary: {}: {}'.format(test_id, id_base, summary[id_base])
        print 'done'

    def run(self):
        """Update test id in test file and verify."""
        print 'updating test ids...'

        in_f = self.options['<file>']

        pattern = self.options['--pattern'] or '^(\w+\.)+(\w+)?$'
        is_append = self.options['--append']
        out_f = self.options['--output']

        out_f = out_f or in_f
        content = []

        if is_append:
            summary, sum_rno = self.read_summary(in_f)
        else:
            summary, sum_rno = {}, -1

        with open(in_f) as f:
            for idx, line in enumerate(f):
                col1 = line.split(' ')[0]
                if re.match(pattern, col1):
                    id_base = col1.rpartition('.')[0]
                    if id_base in summary:
                        if not is_append or not col1[-3:].isdigit():
                            summary[id_base] += 1
                            content.append(line.replace(col1, id_base + '.%03d' % summary[id_base]).rstrip())
                        else:
                            content.append(line.rstrip())
                    else:
                        summary[id_base] = 1
                        content.append(line.replace(col1, id_base + '.%03d' % summary[id_base]).rstrip())
                    content.append('\n')
                else:
                    if idx != sum_rno:
                        content.append(line.rstrip())
                        content.append('\n')
                    else:
                        # idx == sum_rno, only happens when is_append=True, so here is to replace existing summary
                        content.append(str(summary))
                        content.append('\n')
        if not is_append:
            # not append, to add a new line of summary
            content.append('\n\n')
            content.append(str(summary))
            content.append('\n')
        with open(out_f, "w") as f:
            f.writelines(content)
        print 'done'
        self.verify(in_f, summary, pattern)

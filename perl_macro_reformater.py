import re 
from pathlib import Path

class PerlMacroReformater:
    def __init__(self, file_path = 'xd'):
        self.file_path = Path(file_path)
        self.file_content = []

    def read_file(self):
        print(f"INFO: Reading file {self.file_path}")
        lines = []
        try:
            with open(self.file_path, 'r') as f:
                for line in f:
                    lines.append(line)
            return lines
        except Exception as e:
            print(f"Error: Can't read file {self.file_path}: {e}")
            return []
        
    def save_file(self):
        try:
            fixed_file_path = self.file_path.with_stem(self.file_path.stem + '_reformated')
            with open(fixed_file_path, 'w') as f:
                f.write(''.join(self.file_content))
            print(f"INFO: Changes saved to file {fixed_file_path}")
        except Exception as e:
            print(f"Error: Can't save file {fixed_file_path}: {e}")

    def run_reformater(self):
        print("")
        print(49 * "=" + "Perl Macro Reformater" + 50 * "=")
        self.file_content = self.read_file()  
        self.file_content = self.fix_indentation()
        self.save_file()
        print(120 * "=")
         
    def fix_indentation(self):
        if not self.file_content:
            print("Error: Can't fix indentation in non existing file")
            return []

        # Go through file from the end. If END is found, increment the indentation counter by one. 
        # This will result in additional indents in lines above this END
        # In case when IF or FOREACH is found, decreent the indentation counter.

        file_lines_reversed = self.file_content[::-1]
        fixed_file_lines_reversed = []
        current_indentation = 0

        # Simple syntax checker
        if_foreach_count = 0
        end_count = 0 

        for line in file_lines_reversed:
            if re.search(r'\[%\s*?END\s*?-%\]', line):
                line = self.insert_indentation(line, current_indentation) 
                current_indentation += 1
                end_count += 1
            elif re.search(r'\[%\s*?(ELSE|ELSIF.*?)\s*?-%\]', line):
                line = self.insert_indentation(line, current_indentation - 1) 
            elif re.search(r'\[%.*?(IF|FOREACH).*?-%\]', line):
                if current_indentation > 0:
                    current_indentation -= 1
                line = self.insert_indentation(line, current_indentation)
                if_foreach_count += 1 
            else:
                line = self.insert_indentation(line, current_indentation)

            fixed_file_lines_reversed.insert(0, line) # insert at the beginning
        
        # Simple syntax checker
        if if_foreach_count > end_count:
            print(f"WARNING: Missing [% END -%] closing IF/FOREACH statement detected in file {self.file_path}")
            print(f"WARNING: Due to syntax errors indentation is fixed partially in file {self.file_path}")
        elif if_foreach_count < end_count:
            print(f"WARNING: Unnecessary [% END -%] detected in file {self.file_path}")
            print(f"WARNING: Due to syntax errors indentation is fixed partially in file {self.file_path}")
        else:
            print(f"INFO: Fixed indentation in file {self.file_path}")

        return fixed_file_lines_reversed

    def insert_indentation(self, line, current_indentation_index):
        indent = '    '
        return current_indentation_index * indent + line

if __name__ == '__main__':
    file_path = '/nfs/site/disks/zsc11_avs_00049/porszuli/ace-master/tools/collage/assemble/templates/adhoc_connection.txt.siphdas'
    # file_path = '/nfs/site/disks/zsc11_avs_00049/porszuli/ace-master/tools/collage/assemble/templates/par.txt.siphdas'
    reformater = PerlMacroReformater(file_path)
    reformater.run_reformater()
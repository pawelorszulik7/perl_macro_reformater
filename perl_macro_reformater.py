import re 

class PerlMacroReformater:
    def __init__(self, file_path = 'xd'):
        self.file_path = file_path
        self.file_content = []

    def read_file(self):
        lines = []
        try:
            with open(self.file_path, 'r') as f:
                for line in f:
                    lines.append(line)
            return lines
        except Exception as e:
            print(f"Error: Can't read file {self.file_path}: {e}")
            return []
        
    def fix_identation(self):
        self.file_content = self.read_file()

        if not self.file_content:
            print("Error: Can't fix indentation in non existing file")
            return

        file_lines_reversed = self.file_content[-1]

        # Go through file from the end. If END is found, increment the indentation counter by one. 
        # This will result in additional indents in lines above this END
        # In case when IF or FOREACH is found, decreent the indentation counter.

        current_indentation = 0
        indent = '    '

        for line in file_lines_reversed:
            if re.search(r'\[%\s*?END\s*?-%\]', line):
                current_indentation += 1
            elif re.search(r'\[%.*?(IF|FOREACH).*?-%\]', line):
                current_indentation -= 1

            line = current_indentation * indent + line     
         


if __name__ == '__main__':
    file_path = '/nfs/site/disks/zsc11_avs_00049/porszuli/ace-master/tools/collage/assemble/templates/par.txt.siphdas'
    reformater = PerlMacroReformater(file_path)
    reformater.fix_indentation()
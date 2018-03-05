# an attempt to de-mystify the evo parser

# i => codeline
# x => rawline
# s => start
# e => end
# put => output.append
# % formatting => f"" formatting

    def parse(self, codefile, ob, req):
        "evo => python parser "
        # create a simple stack
        stack = []

        def push(code, indent, kind='tag',stack=stack):
            stack.append((code, indent, kind))

        def pop(stack=stack):
            top = stack[-1]
            del stack[-1]
            return top

        # fetch the code from the file, and de-tab it
        code = open(codefile, 'r').read().expandtabs(8)
        # use a list to gather the output
        output = []
        # init the other vars we will need..
        indent = 0
        line_number = 0
        continuation = ''
        # start parsing
        for codeline in [l.rstrip() for l in code.split("\n")] + ["end.of.file"]:
            line_number += 1
            # handle continuation (pass code to next line via `continue`)
            codeline = continuation + codeline
            if codeline.endswith('\\'): 
                continuation = codeline[:-1]
                continue
            continuation = ''
            rawline = codeline.lstrip()
            if rawline and not rawline.startswith('#'):  #ignore comments
                xindent = indent
                if rawline == "end.of.file":
                    indent = stack[0][1]  #dedent to first indent
                    rawline = ''
                else:
                    indent = len(codeline) - len(rawline)
                if stack and indent <= xindent:
                    while True:
                        xxindent = xindent
                        end, xindent, kind = pop()
                        if (end is not None):
                            if kind == 'logic':
                                output.append(end)
                            else:
                                comma = "," if (end and (output[-1][-1] != "(")) else ""
                                output.append(f"{comma}{end}).out({len(stack)})")
                        if stack and stack[0][1] != 0:
                            raise EvoParseError("STACK WRONG", line_number, self.path,
                                                rawline)
#              print(f"STACK WRONG line {line_number} in {self.path,rawline} : {stack}"
                        if indent >= xindent or not stack:
                            if indent > xindent:
                                raise EvoParseError("INVALID DEDENT", line_number,
                                                    self.path, rawline)
#              print(f"INVALID DEDENT line {line_number} in {self.path} : {rawline}", xindent,indent)
                            elif not stack and indent < xindent:
                                raise EvoParseError("STACK EMPTY", line_number,
                                                    self.path, rawline)
#              print(f"STACK EMPTY line {line_number} in {self.path} : {rawline}", xindent,indent)
                            break
                if rawline:
                    kind = 'logic'
                    if rawline.startswith("'") or rawline.startswith('"'):  #raw text
                        start = rawline
                        end = None
                        kind = 'raw'
                    elif rawline.startswith('('):  #expression
                        start = rawline
                        end = None
                        kind = 'expr'
                    elif rawline.find(":") > -1:
                        start, end = rawline.split(":", 1)
                        if start[:4] == 'for ':
                            # set end and start
                            end = f') {start}))'
                            start = '("\\n".join(('
                        elif start[:3] == 'if ':
                            # set end and start
                            end = ') or " ")'  #this makes sure that the whole if-elif-else clause is True
                            start = f'(({start[3:]}) and ('
                        elif start[:4] == 'elif':
                            end = output[-1] + ')'
                            #drop the end from the previous if or elif
                            del output[-1]
                            #reset xindent
                            xindent = xxindent
                            #set start
                            start = f' or " ") or (({start[5:]}) and ('
                        elif start[:4] == 'else':
                            end = output[-1]
                            #drop the end from the previous if or elif
                            del output[-1]
                            #reset xindent
                            xindent = xxindent
                            #set start
                            start = ' or " ") or ('
                        else:  #standard tag
                            start += '('
                            kind = 'tag'
                    elif rawline.find("=") > -1:  #we have a let
                        # get let arguements
                        start, end = rawline.split("=", 1)
                        # remove any whitespace
                        start = start.strip()
                        end = end.strip()
                        #error check
                        f = start.find(' ')
                        if f > -1:
                            raise EvoSyntaxError(line, self.path, x[:f], x[f:])
                        #expand start and end, ready for output
                        start = f'let(globals(),{start}='
                        end = f'{end})'
                    elif rawline.endswith('.evo'):
                        parts = rawline.rsplit('.', 2)
                        start = f'include("{parts[-2]}.evo",{parts[0] if len(parts) == 3 else "self"},req)'
                        end = None
                        kind = 'include'
                    elif rawline == 'content.here':  #wrapper include
                        start = 'content(self,req)'
                        end = None
                        kind = 'include'
                    else:
                        start = rawline
                        end = None
                        kind = 'expr'

                    # check syntax of expressions
                    if kind == 'expr': 
                        try:  #this will break if there are any globals - we are just looking for syntax errors
                            eval(rawline)
                        except SyntaxError as inst:
                            # send_error(inst, sys.exc_info())
                            raise EvoSyntaxError(line_number, self.path,
                                                 rawline[:inst.offset],
                                                 rawline[inst.offset:])
                        except:  #ok
                            pass

                    # push the end, and output the start
                    push(end, indent, kind)
                    prefix="+'\\n'+" if (output and (xindent == indent)) else ""
                    output.append(f'{prefix}{start}')

        # annotate the output with codefile start/stop messages
        if output and not sparse:
            if output[0].find("<!DOCTYPE") >= 0:
                output.insert(1, f"+'\\n<!-- start of {codefile} -->\\n'")
            else:
                output.insert(0, f"'\\n<!-- start of {codefile} -->\\n'+")
            output.append(f"+'\\n<!-- end of (codefile} -->\\n'")

        # glue together and return
        py = "".join(output)
        if debug:
            print("PYTHON:", py)
        return py



def exec_cmd(cmd_buff):
    cmd = re.sub(' +',' ',cmd_buff).strip().split(' ')
    resp = ''
    if len(cmd) == 0:
        resp = ''
    else:
        if cmd[0] == 'p':
            resp = '<p></p>\n'
            if len(cmd) > 1:
                resp = resp*int(cmd[1])
        elif cmd[0] == 'div':
            resp = '<div id="" class=""></div>\n'
            if len(cmd) > 1:
                resp = resp*int(cmd[1])
        elif cmd[0] == 'span':
            resp = '<span></span>\n'
            if len(cmd) > 1:
                resp = resp*int(cmd[1])
        elif cmd[0] == 'js':
            resp = '<script src="_file_url.js"></script>\n'
            if len(cmd) > 1:
                resp = resp*int(cmd[1])
        elif cmd[0] == 'p':
            resp = '<link rel="stylesheet" href="_file_url.css"></link>\n'
            if len(cmd) > 1:
                resp = resp*int(cmd[1])
        elif cmd[0] == 'a':
            resp = '<a href="_url"></a>\n'
            if len(cmd) > 1:
                resp = resp*int(cmd[1])
        elif cmd[0] == 'img':
            resp = '<img src="_img_url.jpg" alt="_alt_text"></img>\n'
            if len(cmd) > 1:
                resp = resp*int(cmd[1])
        elif cmd[0] == 'table':
            resp = '<table>'
            if len(cmd) == 1:
                resp += '</table>\n'
            elif len(cmd) == 2:
                resp += '</table>\n'
                resp = resp*int(cmd[1])
            else:
                resp += '\n'
                resp += ('<tr>\n' + ('<td></td>\n'*int(cmd[2])) + '</tr>\n')*int(cmd[1])
                resp += '</table>\n'
        elif cmd[0] == '//':
            resp = '<!-- _comment -->\n'
            if len(cmd) > 1:
                resp = resp*int(cmd[1])
        elif cmd[0] == 'list':
            resp = '<ul>'
            if len(cmd) == 1:
                resp += '</ul>\n'
            else:
                resp += '\n'
                resp += '<li></li>\n'*int(cmd[1])
                resp += '</ul>\n'
        elif cmd[0] == 'head':
            resp = '<head>\n'
            resp += '<meta charset="UTF-8">\n'
            resp += '<meta name="description" content="_content_of_website">\n'
            resp += '<meta name="keywords" content="_keyword1,_keyword2">\n'
            resp += '<meta name="author" content="_authorname">\n'
            resp += '</head>\n'
        elif cmd[0] == 'html':
            resp = '<!DOCTYPE html>\n'
            resp += '<html>\n'
            resp += cmd_extend_html('head')
            resp += '<body></body>\n'
            resp += '</html>\n'
        elif cmd[0] == 'form':
            resp = '<form action="/action_page.php">\n'
            resp += '<fieldset>\n'
            resp += '<legend>_form_title</legend>\n'
            resp += '<input type="text" name="_name" value="_default_value"><br>\n'
            resp += '<input type="submit" value="_showtext">\n'
            resp += '</fieldset>\n'
            resp += '</form>\n'
        else:
            resp = ''
    return resp

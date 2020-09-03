import sublime_plugin

from sublime import set_clipboard
from Default.paragraph import expand_to_paragraph


class Base(object):
    def process(self, func):
        t = self.getText()
        set_clipboard(func(t))
        self.view.window().status_message('data copied to clipboard')

    def getText(self):
        view = self.view
        text = []
        if view.sel():
            for region in view.sel():
                if region.empty():
                    # text is not selected, expand to the current paragraph
                    text.append(view.substr(expand_to_paragraph(view, region.b)))
                else:
                    # there is some text already selected, use that only
                    text.append(view.substr(region))
        text = text[0].split('\n')
        return text

    def parseText(self, paragraphs, quote=False, suffix=''):

        parsed_text = []
        for par in paragraphs:
            if len(par) > 0:
                parsed_text.append(str(par) + suffix)

        if quote:
            # parsed text should should be enclosed in double quotes, and
            # separated by commas and space
            string = ', '.join(['"' + item + '"' for item in parsed_text])
        else:
            # create a space delimited list of the parsed text
            string = ' '.join(parsed_text)
        return string


class PlainCommand(sublime_plugin.TextCommand, Base):
    def run(self, edit):
        self.process(self.plain)

    def plain(self, text):
        return self.parseText(text, quote=False, suffix='')


class DrawingCommand(sublime_plugin.TextCommand, Base):
    def run(self, edit):
        self.process(self.drawing)

    def drawing(self, text):
        return self.parseText(text, quote=False, suffix='.SLDDRW')


class IndesignCommand(sublime_plugin.TextCommand, Base):
    def run(self, edit):
        self.process(self.in_design)

    def in_design(self, text):
        return self.parseText(text, quote=False, suffix='.INDD')


class IsoCommand(sublime_plugin.TextCommand, Base):
    def run(self, edit):
        self.process(self.iso)

    def iso(self, text):
        return self.parseText(text, quote=False, suffix='.ISO')


class EpsCommand(sublime_plugin.TextCommand, Base):
    def run(self, edit):
        self.process(self.eps)

    def iso(self, text):
        return self.parseText(text, quote=False, suffix='.EPS')


class PartCommand(sublime_plugin.TextCommand, Base):
    def run(self, edit):
        self.process(self.part)

    def part(self, text):
        return self.parseText(text, quote=False, suffix='.SLDPRT')


class AssemblyCommand(sublime_plugin.TextCommand, Base):
    def run(self, edit):
        self.process(self.assembly)

    def assembly(self, text):
        return self.parseText(text, quote=False, suffix='.SLDASM')


class TcmCommand(sublime_plugin.TextCommand, Base):
    def run(self, edit):
        self.process(self.TCM)

    def TCM(self, text):
        return self.parseText(text, quote=True, suffix='')


class CommaCommand(sublime_plugin.TextCommand, Base):
    def run(self, edit):
        self.process(self.comma)

    def comma(self, text):
        return self.parseText(text)

    def parseText(self, paragraphs):
        parsed_text = []
        for par in paragraphs:
            if len(par) > 0:
                parsed_text.append(str(par))
            string = ', '.join(parsed_text)
        return string

from sphinx.util.compat import make_admonition
from sphinx.roles import XRefRole
from sphinx.locale import _
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.tables import ListTable
from docutils.statemachine import ViewList


#class ParRefRole(XRefRole):
#    
#    def process_link(self, env, refnode, has_explicit_title, title, target):
#        refnode['reftype'] = 'ref'
#        refnode['reftarget'] = 'partable-%s' % target
#        refnode['refexplicit'] = True
#
#        if not has_explicit_title:
#            title = target
#
#        return super(ParRefRole, self).process_link(env, refnode, True, title, 'partable-%s' % target)


class ParTableDirective(ListTable):
    
    option_spec = {
        'widths': directives.positive_int_list,
        'class': directives.class_option,
        'name': directives.unchanged
    }
    
    def run(self):
        if not self.content:
            error = self.state_machine.reporter.error(
                'The "%s" directive is empty; content required.' % self.name,
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            return [error]

        self.ad = make_admonition(partable, self.name, [_('ParTable')], self.options,
                                  self.content, self.lineno, self.content_offset,
                                  self.block_text, self.state, self.state_machine)

        title, messages = self.make_title()

        columns = ['parameter', 'description', 'default', 'range', 'units']
        
        table_data = []

        header = []
        for column in columns:
            p = nodes.paragraph()
            self.state.nested_parse(ViewList([column], source=column), 0, p)
            header.append(p)
        table_data.append(header)

        targets = []
        for item in self.ad[0][1:]:
            for info in item:
                row = []
                
                atts = {}
                for key, val in info[1][0]:
                    atts[key.astext()] = val.astext()

                p = nodes.paragraph()
                par = info[0].astext()

                targets.append('partable-%s' % par)

                if atts.has_key('advanced'):
                    par += '+'
                if atts.has_key('required'):
                    par += '*'

                self.state.nested_parse(ViewList([par], source=par), 0, p)
                row.append(p)

                for column in columns[1:]:
                    p = nodes.paragraph()
                    col_value = atts[column] if atts.has_key(column) else ''
                    col_value = '\-' if col_value == '-' else col_value
                    self.state.nested_parse(ViewList([col_value], source=col_value), 0, p)
                    row.append(p)

                table_data.append(row)

        col_widths = self.get_column_widths(table_data)
        table_node = self.build_table_from_list(table_data, col_widths, 1, 0)
        table_node['classes'] += self.options.get('class', [])
        
        self.add_name(table_node)
        
        if title:
            table_node.insert(0, title)

        target_node = nodes.target('', '', ids=targets)

        return [target_node, table_node] + messages

    
    def get_column_widths(self, table_data):
        col_widths = None
        for row in table_data:
            if not col_widths:
                col_widths = [0] * len(row)
            for i, (w, v) in enumerate(zip(col_widths, row)):
                if type(v) is list:
                    col_widths[i] = max(w, len(v[1].astext()))
                else:
                    col_widths[i] = max(w, len(v.astext()))
        return col_widths


class partable(nodes.Admonition, nodes.Element):
    pass


def partable_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    '''Create emphesized reference to partable directive'''
    
    ref = '#partable-%s' % text
    node = nodes.reference('', '', refuri=ref, **options)
    innernode = nodes.emphasis(_(text), _(text))
    node.append(innernode)
            
    return [node], []

    
def setup(app):
    app.add_directive('partable', ParTableDirective)
    app.add_role('par', partable_role)

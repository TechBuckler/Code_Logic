# Fix imports for reorganized codebase



def export_to_python(ir_model):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('export_python.j2')
    return template.render(model=ir_model)

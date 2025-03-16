import re

def process_function_body(body):
    body = body.strip()
    if not body:
        return "return 0"
    lines = [line.rstrip() for line in body.split('\n') if line.strip()]
    if not lines:
        return "return 0"
    last_line = lines[-1]
    if not last_line.startswith('return'):
        body += "\nreturn 0"
    return body

def generate_array(items, quote='"'):
    lines = []
    for i in range(len(items)):
        comma = "," if i < len(items) - 1 else ""
        lines.append(f'    {quote}{items[i]}{quote}{comma}')
    return "\n".join(lines)

def generate_file_content(pkgname, pkgver, deps, sources, md5sums, functions_dict):
    content = f"""pkgname={pkgname}
pkgver={pkgver}

dependencies=(
{generate_array(deps)}
)

sources=(
{generate_array(sources)}
)

md5sums=(
{generate_array(md5sums, quote="'")}
)
"""
    functions_order = ['prepare', 'build', 'test', 'install', 'preinstall', 'postinstall', 'remove']
    for key in functions_order:
        text = functions_dict.get(key, "")
        if key == "prepare" and sources:
            first_source = sources[0]
            match = re.search(r'(\.tar\.[^."\']+)', first_source)
            if match:
                ext = match.group(1)
            else:
                ext = ".tar.xz"
            text = re.sub(r'\.tar\.[^."\']+', ext, text)
        func_body = process_function_body(text)
        content += f"\nkraken_{key}() {{\n{func_body}\n}}\n"
    return content


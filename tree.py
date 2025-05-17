import os

exclude = {
    'node_modules', '.git', '.idea', '__pycache__', 'avatar', 'public'
}


def generate_tree(path, prefix='', exclude_dirs=exclude):
    entries = sorted(os.listdir(path))
    entries = [e for e in entries if e not in exclude_dirs]

    output_lines = []
    for index, entry in enumerate(entries):
        full_path = os.path.join(path, entry)
        connector = '└── ' if index == len(entries) - 1 else '├── '

        output_lines.append(prefix + connector + entry)

        if os.path.isdir(full_path):
            extension = '    ' if index == len(entries) - 1 else '│   '
            output_lines.extend(generate_tree(full_path, prefix + extension, exclude_dirs))

    return output_lines


def export_tree(root_dir='.', output_file='structure.txt'):
    tree_lines = [os.path.basename(os.path.abspath(root_dir)) + '/']
    tree_lines += generate_tree(root_dir)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(tree_lines))
    print(f"📁 结构已导出为 Markdown 树状图：{output_file}")


if __name__ == '__main__':
    export_tree()

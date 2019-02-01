import os
import os.path as op

root_dir = os.path.realpath(os.path.curdir)
package_dir = op.join(root_dir, 'src', '{{ cookiecutter.package_name }}')


if __name__ == '__main__':
    if '{{ cookiecutter.use_cli }}' != 'y':
        os.unlink(op.join(package_dir, 'cli.py'))
        os.unlink(op.join(package_dir, '__main__.py'))

    if '{{ cookiecutter.use_bitbucket_pipeline }}' != 'y':
        os.unlink(op.join(root_dir, 'bitbucket-pipelines.yml'))

    if '{{ cookiecutter.license }}' == 'No license':
        os.unlink(op.join(root_dir, 'LICENSE'))

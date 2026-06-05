import os

root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),"..",".."
    )
)

def join_path(*args):
    return os.path.join(root,*args)

def get_root(): return root
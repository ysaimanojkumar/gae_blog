
import os
import sys
import unittest

try:
    import dev_appserver
except ImportError, e:
    raise ImportError, "App Engine must be in PYTHONPATH."
    sys.exit()

os.environ["SERVER_SOFTWARE"] = "DevelopmentTesting"

test_path = sys.argv[0]

dev_appserver.fix_sys_path()

# fix_sys_path removes the current working directory, so we add it back in
sys.path.append('.')

# needed to be able to import the third party libraries

#BLOG_PATH = os.path.dirname(os.path.join(os.path.abspath(__file__), os.path.pardir))
BLOG_PATH = '/home/saimanoj/appEngineProjects/blog-ysaimanojkumar/gae_blog'
print BLOG_PATH
sys.path.append(os.path.dirname(BLOG_PATH))
sys.path.append(os.path.join(BLOG_PATH, 'lib', 'webtest'))

suite = unittest.loader.TestLoader().discover(test_path)
unittest.TextTestRunner(verbosity=2).run(suite)

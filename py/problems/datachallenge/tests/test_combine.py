from orchestrator import merge
from prettyprint_mapper import format_connections
from .util import tabify

'''
          |3| - |6|
         / 
|1| - |2|
         \
          |4| - |5|
'''
def should_combine():
    n2 = tabify('''1 2 # 3 4
2 1 3 4 # 5 6
3 2 6 # 1 4
4 2 5 # 1 3
5 4 # 2
6 3 # 2
''').split('\n')
    n1 = tabify('''1 2 #
2 1 3 4 #
3 2 6 #
4 2 5 #
5 4 #
6 3 #
''').split('\n')
    n3 = list(format_connections(merge(n2, n1)))
    assert n3 == tabify(
'''1 2 3 4 5 6
2 1 3 4 5 6
3 1 2 4 5 6
4 1 2 3 5 6
5 1 2 3 4
6 1 2 3 4''').split('\n')
    
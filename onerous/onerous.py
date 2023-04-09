# Imports ====================================================================

from pprint import PrettyPrinter
from psutil import Process
from psutil import process_iter


# Functions ==================================================================

def get_eligible_processes(
    username: str = 'postgres',  # Operating system user name
    name: str = 'postgres',  # Process name
) -> list:

    '''
    Function to filter eligible processes based on operating system user and
    process name.
    It returns a list of eligible process.
    '''

    # Iterate over processes considering id, name and user
    for p in process_iter(['pid', 'name', 'username']):
        pid = p.info['pid']  # Process id (pid)
        p_name = p.info['name']  # Process name
        p_username = p.info['username']  # Operating system user name

        # If process name and process user match with respective parameters
        # it will be a list element of eligible processes.
        if p_name == name and p_username == username:
            yield pid

# ----------------------------------------------------------------------------


def get_onerous_processes(
    username: str = 'postgres',  # Operating system user name
    name: str = 'postgres',  # Process name
    cpu_percent: float = 0,  # CPU percentage to be considered
    memory_percent: float = 0,  # Memory percentage to be considered
    order_by: str = 'cpu',  # Order by percentage of CPU or memory
    reverse: bool = True,  # Descending order
    
) -> list:

    '''
    Function that returns a list of onerous process according to criteria
    provided by parameters.
    '''

    # Order process by CPU or memory?
    if order_by == 'cpu':
        order_by = 'cpu_percent'
    elif order_by == 'mem':
        order_by = 'mem_percent'
    else:
        msg = ('The "order_by" parameter only accpets the following values:'
               ' "cpu" and "mem"')
        raise Exception(msg)

    # Empty process list
    processes = []

    # Eligible processes list
    ep = get_eligible_processes(username=username, name=name)

    # Iterate over eligible processes
    for pid in ep:
        proc = Process(pid)
        cpu_p = proc.cpu_percent(.03)
        mem_p = proc.memory_percent()
        exe = proc.exe()

        d = {
             'pid': pid,
             'cpu_percent': cpu_p,
             'memory_percent': mem_p
             }
              
        if cpu_p >= cpu_percent and mem_p >= memory_percent:
            processes.append(d)

    sorted_processes = sorted(
        processes,
        key=lambda k: k[order_by],
        reverse=reverse,
        )
    
    pids = [i['pid'] for i in sorted_processes]

    return tuple(pids)

# ------------------------------------------------------------------------------

def get_rows_to_json(
    pids: tuple,
    host: str=None,
    port: int=5432,
    db: str='postgres',
    user: str='postgres',
    pw: str=None,
    ) -> str:

    '''
    if host is None:
        s_conn = f'port={port} dbname={db} user={user} password={pw}'
    else:
        s_conn = (f'host={host} port={port} dbname={db} user={user}'
            f' password={pw}')
    '''
        
    print(locals().keys())
        



x = get_onerous_processes(cpu_percent=5)

pp = PrettyPrinter(indent=4)

pp.pprint(x)

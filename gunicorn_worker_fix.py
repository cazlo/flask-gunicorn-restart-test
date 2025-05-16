# fix from https://github.com/benoitc/gunicorn/issues/3038#issuecomment-2639932104
import errno

from gunicorn import SERVER_SOFTWARE, version_info
from gunicorn.workers.gthread import TConn, ThreadWorker

COMPATIBLE = False

if (21, 0, 0) <= version_info <= (23, 0, 0):
    COMPATIBLE = True

if not COMPATIBLE:
    raise RuntimeError(f'{SERVER_SOFTWARE} is not supported')


class TConnSync(TConn):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initialized = True


class ThreadWorkerSync(ThreadWorker):

    def accept(self, server, listener):
        try:
            sock, client = listener.accept()
            # initialize the connection object
            conn = TConnSync(self.cfg, sock, client, server)

            self.nr_conns += 1
            # wait until socket is readable
            self.enqueue_req(conn)

        except OSError as e:
            if e.errno not in (
                errno.EAGAIN,
                errno.ECONNABORTED,
                errno.EWOULDBLOCK,
            ):
                raise
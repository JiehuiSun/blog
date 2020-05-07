#! /bin/sh

HOST_NAME=`hostname`
if [[ $HOST_NAME =~ 'blog-backend'* ]]; then
    BASE_PATH=/workspace/py3-dj2/bin
else
    BASE_PATH=/root/project/Blog/blog_backend/.venv/bin
fi

PATH=$BASE_PATH/python
CONFIGURE=uwsgi.ini
PID_FILE=uwsgi.pid
UWSGI_CMD=$BASE_PATH/uwsgi

case   "$@"   in
    start)
        $UWSGI_CMD --ini $CONFIGURE
        echo "start uwsgi ok.."
        ;;
    stop)
        $UWSGI_CMD --stop $PID_FILE
        echo "stop uwsgi ok.."
        ;;
    reload)
        $UWSGI_CMD --reload $PID_FILE
        echo "reload uwsgi ok.."
        ;;
    restart)
        $UWSGI_CMD --stop $PID_FILE
        sleep 1
        $UWSGI_CMD --ini $CONFIGURE
        ;;
    *)
        echo 'unknown arguments (start|stop|reload|restart)'
        exit 1
        ;;
esac



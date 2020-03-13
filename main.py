from infra.message_manager import MessageManager
import multiprocessing


def write_process():
    for i in range(100):
        MessageManager.write_msg('My Message #: ' + str(i+1))


def read_process():
    for i in range(100):
        print(MessageManager.read_msg(i))


def main():
    wp = multiprocessing.Process(target=write_process)
    rp = multiprocessing.Process(target=read_process)
    wp.start()
    rp.start()
    wp.join()
    rp.join()


if __name__ == "__main__":
    main()

from infra.read_write_process import ReadWriteProcess, Action


def main():
    wp = ReadWriteProcess(action=Action.Write, messages_number=100)
    rp = ReadWriteProcess(action=Action.Read, messages_number=200)
    wp.run()
    rp.run()
    wp.wait_for_other()
    rp.wait_for_other()


if __name__ == "__main__":
    main()

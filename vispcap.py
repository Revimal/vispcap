from async_worker import AsyncWorker
from flow_canvas import FlowCanvas
from pcap_parser import PcapParser

def main():
    AsyncWorker.instance().add_async(FlowCanvas.identifier(), FlowCanvas.instance('test', 400, 400, 0.01, True).render())
    AsyncWorker.instance().add_async(PcapParser.identifier(), PcapParser('/home/hhseo/Desktop/syslog').parse())
    AsyncWorker.instance().do_async()

if __name__ == '__main__':
    main()
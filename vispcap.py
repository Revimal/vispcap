from async_worker import AsyncWorker
from file_logger import FileLogger
from flow_canvas import FlowCanvas
from pcap_parser import PcapParser

def main():
    AsyncWorker.instance().add_async(FileLogger.identifier(), FileLogger.instance(logpath = "/home/hhseo/vispcap.log").sync())
    AsyncWorker.instance().add_async(FlowCanvas.identifier(), FlowCanvas.instance().render())
    AsyncWorker.instance().add_async(PcapParser.identifier(), PcapParser("/home/hhseo/Desktop/port0.pcap").parse())
    AsyncWorker.instance().do_async()

if __name__ == '__main__':
    main()
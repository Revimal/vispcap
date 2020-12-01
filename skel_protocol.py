import abc
import typing

class SkelProtocol(metaclass=abc.ABCMeta):
    _succesor_list = typing.Tuple(str, typing.Any)

    def __init__(self, protname, protdef: typing.Tuple(typing.Any, str)):
        self.__class__._succesor_list[protname] = self

    @abc.abstractmethod
    def process(self, bytebuf) -> typing.Tuple(str, int):
        pass

    def handle(self, bytebuf):
        protname, hdrbytes = self.process(bytebuf)

        if not protname:
            return hdrbytes

        payload = bytebuf[hdrbytes:]
        nextproto = self.__class__._succesor_list[protname]

        return hdrbytes + nextproto.handle(payload)

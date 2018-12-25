"""
Prometheus Service
"""


class Prometheus():

    __metrics = []

    def __init__(self, metrics=[]):
        self.__metrics = metrics

    def set_metrics(self, metrics):
        self.__metrics = metrics

    def push_to_metrics(self, record):
        self.__metrics.append(record)

    def get_plain_metrics(self):
        data = ""
        for metric in self.__metrics:
            if "type" in metric and metric["type"] == "count":
                data += self.__get_count_metric(metric)

        return data

    def __get_count_metric(self, item):
        data = ""
        if "comment" in item:
            data += "# %s\n" % item["comment"]
        data += "%s %d\n" % (item["record"], item["count"])
        return data

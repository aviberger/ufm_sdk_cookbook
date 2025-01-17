"""
@copyright:
    Copyright (C) Mellanox Technologies Ltd. 2014-2020.  ALL RIGHTS RESERVED.

    This software product is a proprietary product of Mellanox Technologies
    Ltd. (the "Company") and all right, title, and interest in and to the
    software product, including all associated intellectual property rights,
    are and shall remain exclusively with the Company.

    This software product is governed by the End User License Agreement
    provided with the software product.

@author: Anan Al-Aghbar
@date:   Jan 25, 2022
"""
import os
import sys
sys.path.append(os.getcwd())

import logging

from utils.args_parser import ArgsParser
from utils.logger import Logger

from ufm_telemetry_stream_to_fluentd.src.web_service import UFMTelemetryFluentdStreamingServer
from ufm_telemetry_stream_to_fluentd.src.streamer import \
    UFMTelemetryStreaming,\
    UFMTelemetryStreamingConfigParser,\
    UFMTelemetryConstants
from ufm_telemetry_stream_to_fluentd.src.streaming_scheduler import StreamingScheduler

def _init_logs(config_parser):
    # init logs configs
    # this path for debugging
    # default_file_name = 'tfs.log'
    default_file_name = '/log/tfs.log' # this path on docker
    logs_file_name = config_parser.get_logs_file_name(default_file_name=default_file_name)
    logs_level = config_parser.get_logs_level()
    Logger.init_logs_config(logs_file_name, logs_level)

if __name__ == '__main__':

    # init app config parser & load config files
    args = ArgsParser.parse_args("UFM Telemetry Streaming to fluentd", UFMTelemetryConstants.args_list)
    config_parser = UFMTelemetryStreamingConfigParser(args)

    _init_logs(config_parser)

    try:
        if config_parser.get_enable_streaming_flag():
            streamer = UFMTelemetryStreaming(config_parser=config_parser)
            scheduler = StreamingScheduler.getInstance()
            job_id = scheduler.start_streaming(streamer.stream_data,
                                            streamer.streaming_interval)
            logging.info("Streaming has been started successfully")
        else:
            logging.warning("Streaming was not started, need to enable the streaming & set the required configurations")

    except ValueError as ex:
        logging.warning("Streaming was not started, need to enable the streaming & set the required configurations")

    server = UFMTelemetryFluentdStreamingServer(config_parser)
    server.run()

# coding=utf-8
# Copyright 2018-2020 EVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio

from src.utils.logging_manager import LoggingManager


@asyncio.coroutine
def handle_request(transport, request_message):
    """
        Reads a request from a client and processes it

        If user inputs 'quit' stops the event loop
        otherwise just echoes user input
    """

    response_message = "foo"

    LoggingManager().log('Response to client: --|' +
                         str(response_message) +
                         '|--')

    data = response_message.encode('ascii')
    transport.write(data)

    return response_message

#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import openai
import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "392a0ccd-a65b-4aa3-8650-1aa89383e11e")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "O5G8Q~Zk.Aff~GAM3xRKowVY~4PitjaF0cx_tcB~")
    openai.api_key = "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"
    # openai.api_key = "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"
    # f = open("models.txt", "w")
    # f.write(str(openai.Model.list()))
    # f.close()
#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import openai
import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    # # # draven bot
    # APP_ID = os.environ.get("MicrosoftAppId", "392a0ccd-a65b-4aa3-8650-1aa89383e11e")
    # APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "OSQ8Q~b7tuitEil_LNmz9A_OqtNz9Dwx08dnYaqF")

    # # vcb bot
    # APP_ID = os.environ.get("MicrosoftAppId", "db93d848-66f9-417b-8979-d4390557b5f0")
    # APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "Y3n8Q~6ZnrddS0p~lIUgOJyA_ud5VIweQ5z9Wdh5")

    # dac biet tuot
    # APP_ID = os.environ.get("MicrosoftAppId", "aeb7e1b7-6143-40ea-ad35-8daae4973ca2")
    # APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "ohV8Q~HDEg2ZFVHA7V0l1.yesJpv2XiX6jyO~atD")

    # dac biet tuot
    APP_ID = os.environ.get("MicrosoftAppId", "ab1baa59-ef10-41fc-9f84-3e808f3c99f4")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "2BH8Q~Au6HWKTIbsifx-0McqVnQtKqW_GdB1ub4u")

    # openai.api_key = "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"
    openai.api_key = "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"
    # f = open("models.txt", "w")
    # f.write(str(openai.Model.list()))
    # f.close()
#!/usr/bin/env python

import os
from super_draft.utils import generate_token_pickle


def main():
    generate_token_pickle(os.getcwd() + "/credentials.json", os.getcwd() + "/token.pickle")


if __name__ == '__main__':
    main()


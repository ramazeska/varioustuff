#!/usr/bin/env python3

import os
import sys
import traceback




if __name__ == "__main__":
    try:

        # get general config
        self_path = os.path.dirname(os.path.abspath(__file__))
        self_root = os.path.dirname(self_path)
        scr_name = os.path.split(self_path)[-1]

        shared_libs = os.path.join(self_root, 'shared_libs')
        sys.path.insert(0, shared_libs)

        modules = os.path.join(self_path, 'modules')
        sys.path.insert(0, modules)

        try:
            from main import main
        except ImportError as e:
            raise Exception('failed to import the main with: {}\ncheck the module path: {}'.format(e, modules))


        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        print(traceback.print_exc())
        sys.exit(2)

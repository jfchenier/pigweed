# Pigweed

Pigweed is an open source collection of embedded-targeted libraries–or as we
like to call them, modules. These modules are building blocks and infrastructure
that enable faster and more reliable development on small-footprint MMU-less
32-bit microcontrollers like the STMicroelectronics STM32L452 or the Nordic
nRF52832.

For more information please see our website: https://pigweed.dev/.

## Links

<!-- TODO(b/256680603) Remove query string from issue tracker link. -->

- [Documentation](https://pigweed.dev/)
- [Source Code](https://cs.pigweed.dev/pigweed)
- [Code Reviews](https://pigweed-review.googlesource.com)
- [Mailing List](https://groups.google.com/forum/#!forum/pigweed)
- [Chat Room](https://discord.gg/M9NSeTA)
- [Issue Tracker](https://issues.pigweed.dev/issues?q=status:open)


## Getting started for RPC test

To get setup:

#. Make sure you have Git and Python installed and on your path.

#. Clone Pigweed and bootstrap the environment (compiler setup & more). **Be
   patient, this step downloads ~1GB of LLVM, GCC, and other tooling**.

   .. code:: bash

     $ cd ~
     $ git clone https://gitlab.sparkmicro.ca/jfchenier/pigweed-test.git
     ...
     $ cd pigweed-test
     $ source ./bootstrap.sh (On Linux & Mac)
     $ bootstrap.bat         (On Windows)
     ...

**Note:** After running bootstrap once, use ``source ./activate.sh`` (or
``activate.bat`` on Windows) to re-activate the environment without
re-bootstrapping.

#. Install nanopb dependency to the virtual environnement.

   .. code:: bash

     $ pw package install nanopb

#. Install teensy core.

    .. code:: bash

     $ arduino_builder install-core --prefix ./third_party/arduino/cores/ --core-name teensy

#. Configure the GN build. (Replace "user" and "repo path")

   .. code:: bash

     $ gn gen out --args='
          pw_arduino_build_CORE_PATH="//third_party/arduino/cores"
          pw_arduino_build_CORE_NAME="teensy"
          pw_arduino_build_PACKAGE_NAME="teensy/avr"
          pw_arduino_build_BOARD="teensy40"
          pw_arduino_build_MENU_OPTIONS=["menu.usb.serial", "menu.speed.150", "menu.keys.en-us"]
          dir_pw_third_party_nanopb = "/home/"user"/"repo path"/pigweed-test/environment/packages/nanopb"'

Start the watcher. The watcher will invoke Ninja to build all the targets

   .. code:: bash

     $ pw watch arduino

      ▒█████▄   █▓  ▄███▒  ▒█    ▒█ ░▓████▒ ░▓████▒ ▒▓████▄
       ▒█░  █░ ░█▒ ██▒ ▀█▒ ▒█░ █ ▒█  ▒█   ▀  ▒█   ▀  ▒█  ▀█▌
       ▒█▄▄▄█░ ░█▒ █▓░ ▄▄░ ▒█░ █ ▒█  ▒███    ▒███    ░█   █▌
       ▒█▀     ░█░ ▓█   █▓ ░█░ █ ▒█  ▒█   ▄  ▒█   ▄  ░█  ▄█▌
       ▒█      ░█░ ░▓███▀   ▒█▓▀▓█░ ░▓████▒ ░▓████▒ ▒▓████▀

     20200707 17:24:06 INF Starting Pigweed build watcher
     20200707 17:24:06 INF Will build [1/1]: out
     20200707 17:24:06 INF Attaching filesystem watcher to $HOME/wrk/pigweed/...
     20200707 17:24:06 INF Triggering initial build...
     ...

Flash the binary.

   .. code:: bash

     $ arduino_unit_test_runner --verbose --config out/arduino_debug/gen/arduino_builder_config.json --upload-tool teensyloader --flash-only out/arduino_speed_optimized/obj/pw_hdlc/rpc_example/bin/rpc_example.elf

Run the python test.

   .. code:: bash

    $ pw_hdlc/rpc_example/example_script.py --device /dev/ttyACM0

Reference : https://pigweed.dev/pw_hdlc/rpc_example/?highlight=hdlc
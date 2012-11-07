#/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################
#     Printer Manager
#     Version 1.0.10
#     by Joaquin de la Zerda
#     joaquindelazerda@gmail.com
###############################################

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4


import os
import cupsext
import sys


def list_printers(q):

    "List printers"
    printers = cupsext.getPrinters()
    for printer in printers:
        printer_state = printer.state
        printer_state_info = ""

        if printer_state == 3:
            printer_state_info = "The destination is idle"
        elif printer_state == 4:
            printer_state_info = "The destination is printing a job"
        elif printer_state == 5:
            printer_state_info = "The destination is stopped"
        else:
            printer_state_info = "State undefined"

        if len(q) > 0:
            if (printer.name.find(q) != -1 or printer.info.find(q) != -1 or
                printer.device_uri.find(q) != -1):
                print   "ID: %s\n \tDescription: %s \n \tLocate: %s " \
                        "\n \tState: %s\n" % (printer.name, printer.info,
                        printer.device_uri, printer_state_info)
            else:
                print   "ID: %s\n \tDescription: %s \n \tLocate: %s " \
                        "\n \tState: %s\n" % (printer.name, printer.info,
                        printer.device_uri, printer_state_info)


def clear_queue(printer_id):
    # if not root...exit with error
    if not os.geteuid() == 0:
        sys.exit("ERROR: Esta opción puede ejecutar el usuario root, o " \
                 "usuario nominal con sudo. Por ej. $sudo printman -c [ID " \
                 "IMPRESORA]\n")
        os.system("/usr/sbin/cupsdisable -c " + printer_id)
        os.system("/usr/sbin/cupsenable -c " + printer_id)


def list_jobs():
    os.system("lpstat -o")


def list_printer_jobs(printer_id):
    os.system("/usr/bin/lpq -P " + printer_id)


def printer_info(printer_id):
    os.system("/usr/bin/lpstat -l -p " + printer_id)

def print_help():
    print "-----------------------------------------------------------------" \
          "-----------------------"
    print "PRINTER MANAGER SCRIPT"
    print "-----------------------------------------------------------------" \
          "-----------------------"
    print "Modo de uso: "
    print " -l: Lista las impresoras con su ID, descripcion y URI."
    print " -q [patron]: Busca impresoras segun el patron ingresado."
    print " -c [ID impresora]: Cancela los trabajos pendientes de la " \
          "impresora dada y la reinicia."
    print " -j: Lista todos los trabajos en cola de impresion."
    print " -j [ID impresora]: Lista todos los trabajos en cola de " \
          "impresion de la impresora especificada."
    print " -i [ID impresora]: Muestra informacion detallada de la " \
          "impresora especificada."
    print "-----------------------------------------------------------------" \
          "-----------------------"


def main():

    if len(sys.argv) > 1:
        if sys.argv[1] == "-l":
            list_printers("")

        elif sys.argv[1] == "-q" and len(sys.argv) == 3:
            q = sys.argv[2]
            list_printers(q)

        elif sys.argv[1] == "-c" and len(sys.argv) == 3:
            printer_id = sys.argv[2]
            clear_queue(printer_id)

        elif sys.argv[1] == "-j" and len(sys.argv) == 3:
            printer_id = sys.argv[2]
            list_printer_jobs(printer_id)

        elif sys.argv[1] == "-j" and len(sys.argv) == 2:
            list_jobs()

        elif sys.argv[1] == "-i" and len(sys.argv) == 3:
            printer_id = sys.argv[2]
            printer_info(printer_id)

        else:
            print_help()
    else:
        print_help()


if __name__ == "__main__":
    main()

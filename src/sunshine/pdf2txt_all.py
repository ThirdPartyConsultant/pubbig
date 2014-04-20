
import os
import commands

cmd = "pdf2txt "
for pdf_file in os.listdir("."):
    if pdf_file[-3:] == "pdf":
        transfer_cmd = cmd+ " -o "+ pdf_file+".txt "+ pdf_file
        if os.path.isfile(pdf_file+".txt"):
            print "ignore existing..."+pdf_file+".txt "
        else:
            print transfer_cmd
            commands.getoutput(transfer_cmd)

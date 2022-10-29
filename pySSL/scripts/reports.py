import os
import matplotlib.pyplot as plt
from fpdf import FPDF
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import conf

class Reports():
    """
    The purpose of this class is to create KPI graphics.
    """
    def __init__(self):
        self.report_data()
        self.craft_graphic()
        self.craft_pdf()
        try:
            self.craft_email()
        except:
            print("Error sending email")

    def report_data(self):
        with open(conf.LOG, "r") as f:
            self.date = f.readlines()[-1].split(" ")[0].replace("/","-").strip("[")
            f = open(conf.LOG_ERR).readlines() 
            self.pass_err, self.usr_err, self.ssl_err = (int(f[i].split(":")[1].strip()) for i in range(3))
            self.accesses = len(open(conf.LOG, "r").readlines())-1
            self.accesses_na = self.accesses - (self.pass_err+self.usr_err+self.ssl_err)

    def craft_graphic(self):
        values = [self.accesses_na, self.pass_err, self.usr_err, self.ssl_err]
        legend = ["Valid Connections", "Incorrect Password incidences", "Invalid user incidences", "SSL Errors"]
        f1 = {"family": "Arial","color": "black", "size": 20, "fontweight": "roman"}
        colors = ["lightskyblue", "lightcoral", "gold", "darkorchid"]
        explode = [0, 0.2, 0.2, 0.2]
        percentages = list()
        for i in values: percentages.append(100.*float(i)/sum(values))
        labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(legend, percentages)]
        plt.figure(figsize=(7,3))
        plt.pie(values,startangle=90,shadow=True,explode=explode,colors=colors)
        plt.title("Connections\n",fontdict=f1)
        plt.legend(labels,loc="upper left",fontsize="x-small")
        plt.axis("equal")
        plt.savefig(os.path.join(conf.GRAPHS_FOLDER,"graphic"+self.date+".png"),bbox_inches='tight',dpi=300)

    def craft_pdf(self):
        percentage = self.accesses_na / self.accesses
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Times', 'B', 40)
        pdf.cell(200, 10, txt = "",ln = 1, align = 'C')
        pdf.cell(200, 10, txt = "INSEGUS",ln = 1, align = 'C')
        pdf.set_font('Times', 'B', 1)
        pdf.cell(200, 10, txt = "",ln = 1, align = 'C')
        pdf.set_font('Times', 'B', 40)
        pdf.cell(200, 10, txt = "SSL SERVER CHECK",ln = 1, align = 'C')
        pdf.set_font('Times', 'B', 16)
        pdf.cell(200, 10, txt = self.date+" report\n" ,ln = 1, align = 'C') 
        pdf.image(os.path.join(conf.GRAPHS_FOLDER, "graphic"+self.date+".png"), 20, 70, h=100,w=180)
        pdf.cell(200, 100, txt = "",ln = 1, align = 'L')
        pdf.set_left_margin(32)
        pdf.set_font("Times",style="")
        pdf.cell(200, 35, txt = "",ln = 1, align = 'C')
        pdf.cell(200, 10, txt = "· Incorrect passsword errors: "+str(self.pass_err),ln = 1, align = 'L')
        pdf.cell(200, 10, txt = "· Invalid user errors: "+str(self.usr_err),ln = 1, align = 'L')
        pdf.cell(200, 10, txt = "· SSL Errors: "+str(self.ssl_err),ln = 1, align = 'L')
        pdf.cell(200, 10, txt = "· Total connections: "+str(self.accesses),ln = 1, align = 'L')
        #pdf.cell(200, 10, txt = "· KPI = (transmissions w/o attacks) / total transmissions",ln = 1, align = 'L')
        pdf.cell(200, 10, txt = "· Percentage of Valid Connections: "+str("{:%}".format(percentage)),ln = 1, align = 'L')
        pdf.output(os.path.join(conf.PDFS_FOLDER,"report-"+self.date+".pdf"), "F")

    def craft_email(self):
        message = MIMEMultipart()
        message["From"]= "mail@ssl.pai"
        message["To"]= "sysadmin@ssl_server.com"
        message["Subject"]= "SSL server Report "+self.date
        text_message = MIMEText("The pdf file with the SSL server report is attached. \n Best regards.")
        message.attach(text_message)

        pdfname= "report-"+self.date+".pdf"
        pdf = open(os.path.join(conf.PDFS_FOLDER,"report-"+self.date+".pdf"), "rb")
        payload = MIMEBase("application","octate-stream",Name = pdfname )
        payload.set_payload(pdf.read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
        message.attach(payload)

        connection = smtplib.SMTP(host="localhost",port= 2500)
        connection.sendmail(from_addr="mail@attacks.pai", to_addrs="sysadmin@attacks.com",msg=message.as_string())

        connection.quit()
        
Reports()
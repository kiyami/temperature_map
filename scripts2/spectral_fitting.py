import xspec
import os
import sys

i = 2
n = 5

def fit(i,n):
    while(i<n+1):
        xspec.AllData.clear()
        s1 = xspec.Spectrum("reg-"+str(i)+"_grp.pi")

        m1 = xspec.Model("phabs*apec")
        m1.phabs.nH = "0.0197"
        m1.phabs.nH.frozen = True
        m1.apec.Abundanc = "0.35"
        m1.apec.Abundanc.frozen = True
        m1.apec.Redshift = "0.1427"

        #xspec.Plot.device = "/xs"
        #xspec.Plot.xAxis = "keV"
        #xspec.Plot.xLog = True
        #xspec.Plot.yLog = True

        s1.ignore("0.0-0.5,7.0-**")

        xspec.Fit.statMethod = "cstat"
        xspec.Fit.query = "yes"
        xspec.Fit.perform()
        xspec.Fit.perform()

        m1.apec.Abundanc.frozen = False
        xspec.Fit.perform()
        xspec.Fit.perform()

        #m1.phabs.nH.frozen = False
        #xspec.Fit.perform()

        #xspec.Plot.device = "/xs"
        #xspec.Plot.xAxis = "keV"
        #xspec.Plot.xLog = True
        #xspec.Plot.yLog = True
        #xspec.Plot("data delchi")
        try:
            xspec.Fit.error("1.0 2")
            statistic = xspec.Fit.statistic
            dof = xspec.Fit.dof
            chi = statistic / dof
            note = "  Nice"
            if chi > 1.5:
                note = "  Attention!!!"
        except:
            chi = 0
            note = "  Can't fit!!!"

        kt = m1.apec.kT.values[0]
        kt_err_n = kt-m1.apec.kT.error[0]
        kt_err_p = m1.apec.kT.error[1]-kt

        kt = str(kt)
        kt_err_n = str(kt_err_n)
        kt_err_p = str(kt_err_p)

        file = open("../outputs/fit_outputs.txt","a")
        file.write(str(i)+") "+kt+" (-"+kt_err_n+",+"+kt_err_p+") chi="+str(chi)+note+"\n")
        file.close()

        i = i+1

if __name__ == '__main__':

    working_directory = os.getcwd()
    output_directory = os.path.join(working_directory,'outputs')

    if os.path.exists(output_directory):
        pass
    else:
        os.mkdir('outputs')

    event_path = os.path.join(working_directory,'event_file')
    os.chdir(event_path)
    fit(i,n)
